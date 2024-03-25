# Cuda DF

## Run

```bash
python -m cudadf
```

Result:

```bash
[Callback] Task 3 was cancelled
[Callback] Task 4 was cancelled
[Callback] Task 1 is done
[Callback] Task 2 is done
=== Computation ===
      months  days    
       count count max
years                 
1995       2     2  28
2000       2     2  23
===================
[Callback] Task 0 is done
[Main] Task was cancelled
[Main] Task 2: 1995.5.17. -> ./output/2.parquet
[Main] Task 1: 2000.3.12. -> ./output/1.parquet
[Main] Task was cancelled
[Main] Task 0: 1990.1.1. -> ./output/0.parquet

=== Display ===

=== ./output/2.parquet ===
   years  months  days
0   1995       5    17
```
