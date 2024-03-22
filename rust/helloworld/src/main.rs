use std::path::Path;
use std::sync::{Arc, Mutex};
use std::{fs, thread};

use arrow::array::{BooleanArray, Int16Array, Int8Array};
use arrow::compute::{self};
use arrow::datatypes::{DataType, Field, Schema};
use arrow::record_batch::RecordBatch;
use arrow::util::pretty::print_batches;
use parquet::arrow::ArrowWriter;
use parquet::file::properties::WriterProperties;

struct Result {
    index: i16,
    birthday: String,
}

fn task(index: i16, record: RecordBatch) -> Result {
    let year = record
        .column(0)
        .as_any()
        .downcast_ref::<Int16Array>()
        .unwrap()
        .value(index as usize);
    let month = record
        .column(1)
        .as_any()
        .downcast_ref::<Int8Array>()
        .unwrap()
        .value(index as usize);
    let day = record
        .column(2)
        .as_any()
        .downcast_ref::<Int8Array>()
        .unwrap()
        .value(index as usize);

    if index == 0 {
        let mut conditions = vec![false; record.num_rows() as usize];

        for i in 0..record.num_rows() {
            let y = record
                .column(0)
                .as_any()
                .downcast_ref::<Int16Array>()
                .unwrap()
                .value(i);
            if y == 2000 {
                conditions[i] = true;
            }
        }

        let mask = BooleanArray::from(conditions);
        if let Ok(filtered) = compute::filter_record_batch(&record, &mask) {
            print_batches(&[filtered]).expect("Error printing RecordBatch");
        } else {
            panic!("Error filtering RecordBatch");
        }
    }

    Result {
        index,
        birthday: format!("{}.{}.{}.", year, month, day),
    }
}

fn main() {
    let years: Int16Array = Int16Array::from(vec![1990, 2000, 1995, 2000, 1995]);
    let months: Int8Array = Int8Array::from(vec![1, 3, 5, 7, 1]);
    let days: Int8Array = Int8Array::from(vec![1, 12, 17, 23, 28]);

    let schema = Schema::new(vec![
        Field::new("years", DataType::Int16, false),
        Field::new("months", DataType::Int8, false),
        Field::new("days", DataType::Int8, false),
    ]);

    let record_batch = RecordBatch::try_new(
        Arc::new(schema),
        vec![Arc::new(years), Arc::new(months), Arc::new(days)],
    )
    .expect("Error creating RecordBatch");

    print_batches(&[record_batch.clone()]).expect("Error printing RecordBatch");

    // Write a Parquet file
    let path = Path::new("birthdays.parquet");
    let file = fs::File::create(&path).expect("Error creating file");
    let record_schema = record_batch.schema();
    let props = WriterProperties::builder().build();
    let mut writer =
        ArrowWriter::try_new(file, record_schema, Some(props)).expect("Error creating ArrowWriter");
    writer
        .write(&record_batch)
        .expect("Error writing RecordBatch");
    writer.close().expect("Error closing writer");

    // Multi-threaded task execution
    let rows = record_batch.num_rows() as i16;

    let data = Arc::new(Mutex::new(Vec::new()));
    let mut handles = vec![];

    for i in 0..rows {
        let data = Arc::clone(&data);
        let rec = record_batch.clone();

        let handle = thread::spawn(move || {
            let mut data = data.lock().unwrap();
            let result = task(i, rec);
            data.push(result);
        });

        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    for result in data.lock().unwrap().iter() {
        println!("Task {}: {}", result.index, result.birthday);
    }
}
