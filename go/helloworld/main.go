package main

import (
	"context"
	"os"

	"fmt"
	"sync"

	"github.com/apache/arrow/go/v15/arrow"
	"github.com/apache/arrow/go/v15/arrow/array"
	"github.com/apache/arrow/go/v15/arrow/compute"
	"github.com/apache/arrow/go/v15/arrow/memory"
	"github.com/apache/arrow/go/v15/parquet"
	"github.com/apache/arrow/go/v15/parquet/pqarrow"
)

var wg sync.WaitGroup

func TaskTable(index int, table arrow.Table) {
	defer wg.Done()

	year := table.Column(0).Data().Chunks()[0].(*array.Int16).Value(index)
	month := table.Column(1).Data().Chunks()[0].(*array.Int8).Value(index)
	day := table.Column(2).Data().Chunks()[0].(*array.Int8).Value(index)

	fmt.Printf("Task %d: %d.%d.%d.\n", index, year, month, day)
}

func TaskRecord(index int, record arrow.Record) {
	defer wg.Done()

	year := record.Column(0).(*array.Int16).Value(index)
	month := record.Column(1).(*array.Int8).Value(index)
	day := record.Column(2).(*array.Int8).Value(index)

	fmt.Printf("Task %d: %d.%d.%d.\n", index, year, month, day)

	if index == 0 {

		ctx := context.Background()
		allocator := memory.NewGoAllocator()
		mb := array.NewBooleanBuilder(allocator)
		defer mb.Release()

		for i := 0; i < int(record.NumRows()); i++ {
			if record.Column(0).(*array.Int16).Value(i) == 2000 {
				mb.Append(true)
			} else {
				mb.Append(false)
			}
		}

		mask := mb.NewArray()

		filtered, err := compute.FilterRecordBatch(ctx, record, mask, compute.DefaultFilterOptions())
		if err != nil {
			panic(err)
		}

		fmt.Println(filtered)

	}
}

func DisplayTable(table arrow.Table) {
	fmt.Println(table.Schema())
	fmt.Println("Number of Rows: ", table.NumRows())

	tr := array.NewTableReader(table, table.NumRows())
	defer tr.Release()

	n := 0

	for tr.Next() {
		rec := tr.Record()
		for i, col := range rec.Columns() {
			fmt.Printf("[%d][%q]: %v\n", n, rec.ColumnName(i), col)
		}
		n++
	}
}

func WriteTable(table arrow.Table) {
	file, err := os.Create("out/birthday.parquet")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	schema := table.Schema()

	writerProps := parquet.NewWriterProperties(parquet.WithMaxRowGroupLength(100))
	writer, err := pqarrow.NewFileWriter(schema, file, writerProps, pqarrow.DefaultWriterProps())
	if err != nil {
		panic(err)
	}

	defer writer.Close()

	err = writer.WriteTable(table, 1024)
	if err != nil {
		panic(err)
	}
}

func main() {
	allocator := memory.NewGoAllocator()

	fields := []arrow.Field{
		{Name: "years", Type: arrow.PrimitiveTypes.Int16},
		{Name: "months", Type: arrow.PrimitiveTypes.Int8},
		{Name: "days", Type: arrow.PrimitiveTypes.Int8},
	}

	schema := arrow.NewSchema(fields, nil)

	rb := array.NewRecordBuilder(allocator, schema)
	defer rb.Release()

	rb.Field(0).(*array.Int16Builder).AppendValues([]int16{1990, 2000, 1995, 2000, 1995}, nil)
	rb.Field(1).(*array.Int8Builder).AppendValues([]int8{1, 3, 5, 7, 1}, nil)
	rb.Field(2).(*array.Int8Builder).AppendValues([]int8{1, 12, 17, 23, 28}, nil)

	record := rb.NewRecord()
	defer record.Release()

	table := array.NewTableFromRecords(schema, []arrow.Record{record})
	defer table.Release()

	DisplayTable(table)
	WriteTable(table)

	for i := 0; i < int(record.NumRows()); i++ {
		wg.Add(1)
		go TaskRecord(i, record)
	}
	wg.Wait()

}
