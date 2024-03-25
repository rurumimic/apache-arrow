# Python Arrow

- [docs](https://arrow.apache.org/docs/python/index.html)

## Install

Python 3.10

### pyenv

```bash
pip virtualenv 3.10.z arrow
pyenv activate arrow
```

```bash
pip install -U pip setuptools wheel
```

### pyarrow

```bash
pip install pyarrow
```

## Read Parquet

```py
import pyarrow.parquet as pq
pq.read_table('birthdays.parquet')
```

```py
pyarrow.Table
years: int16 not null
months: int8 not null
days: int8 not null
----
years: [[1990,2000,1995,2000,1995]]
months: [[1,3,5,7,1]]
days: [[1,12,17,23,28]]
```

