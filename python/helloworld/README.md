# Hello World

## Run

```bash
python -m helloworld
```

Result:

```bash
2024-03-25 02:59:04 WARN  NativeCodeLoader:60 - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
[Callback] Task 3 was cancelled
[Callback] Task 4 was cancelled
=== Computation ===
pyarrow.Table
years: int16
months_count: int64
days_count: int64
----
years: [[2000,1995]]
months_count: [[2,2]]
days_count: [[2,2]]
===================
[Callback] Task 2 is done
[Callback] Task 0 is done
[Callback] Task 1 is done
[Main] Task 0: 1990.1.1. -> ./output/0.parquet
[Main] Task was cancelled
[Main] Task 2: 1995.5.17. -> ./output/2.parquet
[Main] Task 1: 2000.3.12. -> ./output/1.parquet
[Main] Task was cancelled

=== Display ===

=== ./output/0.parquet ===
pyarrow.Table
years: int16
months: int8
days: int8
----
years: [[1990]]
months: [[1]]
days: [[1]]
```

### HDFS

Attach to `namenode`:

```bash

docker exec -it apache-arrow_devcontainer-namenode-1 bash
```

```bash
hdfs dfs -ls -R /

drwxr-xr-x   - vscode supergroup          0 2024-03-25 02:59 /user
drwxr-xr-x   - vscode supergroup          0 2024-03-25 02:59 /user/vscode
-rw-r--r--   3 vscode supergroup       1247 2024-03-25 02:59 /user/vscode/birthdays.parquet
drwxr-xr-x   - vscode supergroup          0 2024-03-25 02:59 /user/vscode/output
-rw-r--r--   3 vscode supergroup       1207 2024-03-25 02:59 /user/vscode/output/0.parquet
-rw-r--r--   3 vscode supergroup       1207 2024-03-25 02:59 /user/vscode/output/1.parquet
-rw-r--r--   3 vscode supergroup       1207 2024-03-25 02:59 /user/vscode/output/2.parquet
```
