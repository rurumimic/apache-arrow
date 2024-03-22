# Hello World

```bash
cargo new helloworld
cargo add arrow -F prettyprint
cargo add parquet
```

## Run

```bash
cargo run
```

Result:

```bash
+-------+--------+------+
| years | months | days |
+-------+--------+------+
| 1990  | 1      | 1    |
| 2000  | 3      | 12   |
| 1995  | 5      | 17   |
| 2000  | 7      | 23   |
| 1995  | 1      | 28   |
+-------+--------+------+
+-------+--------+------+
| years | months | days |
+-------+--------+------+
| 2000  | 3      | 12   |
| 2000  | 7      | 23   |
+-------+--------+------+
Task 0: 1990.1.1.
Task 1: 2000.3.12.
Task 2: 1995.5.17.
Task 3: 2000.7.23.
Task 4: 1995.1.28.
```

