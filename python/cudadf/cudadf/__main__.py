import functools
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

import cudf
import pyarrow as pa
import pyarrow.compute as pc
# import pyarrow.cuda as cuda
import pyarrow.parquet as pq
from pyarrow import fs

DEST_DIR = "."
MAX_WORKERS = 3
DUMMY_FILE = f"{DEST_DIR}/birthdays.parquet"

JAVA_HOME = os.environ.get("JAVA_HOME")
HADOOP_HOME = os.environ.get("HADOOP_HOME")


def env():
    CLASSPATH = subprocess.check_output(
        f"{HADOOP_HOME}/bin/hadoop classpath --glob", shell=True
    ).decode("utf-8")

    os.environ["CLASSPATH"] = CLASSPATH


def hdfs_cmd(s: str):
    return subprocess.run(f"{HADOOP_HOME}/bin/hdfs dfs {s}", shell=True)


def display_parquet(hdfs, path):
    print(cudf.read_parquet(path))


def dummy_file(hdfs, path):
    # Arrow
    years = pa.array([1990, 2000, 1995, 2000, 1995], type=pa.int16())
    months = pa.array([1, 3, 5, 7, 1], type=pa.int8())
    days = pa.array([1, 12, 17, 23, 28], type=pa.int8())

    table = pa.table([years, months, days], names=["years", "months", "days"])

    # parquet
    pq.write_table(table, path)
    pq.write_table(table, path, filesystem=hdfs)


def task(
    index: int, table: cudf.DataFrame, hdfs: fs.HadoopFileSystem
) -> Tuple[int, str, str]:
    year = table["years"][index]
    month = table["months"][index]
    day = table["days"][index]

    # Some computation
    if index == 0:
        groups = table.groupby("years").agg({'months': ['count'], 'days': ['count', 'max']})
        filtered = groups[groups[('days', 'count')] >= 2]
        print(f"=== Computation ===\n{filtered}\n===================")

    df = cudf.DataFrame({'years': [year], 'months': [month], 'days': [day]})

    # Write to HDFS
    dest = f"{DEST_DIR}/output/{index}.parquet"
    # pq.write_table(result, dest, filesystem=hdfs)
    df.to_parquet(dest)

    return (index, f"{year}.{month}.{day}.", dest)


def callback(future, args):
    index = args[0]

    if future.cancelled():
        print(f"[Callback] Task {index} was cancelled")
        return

    if future.done():
        print(f"[Callback] Task {index} is done")
        return


def submit_future(executor, func, *args, **kwargs):
    future = executor.submit(func, *args, **kwargs)
    future.add_done_callback(functools.partial(callback, args=args))
    return future


def main(hdfs: fs.HadoopFileSystem, input: str) -> List[str]:
    table = cudf.read_parquet(input)

    # Multi-threading
    futures = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for i in range(len(table)):
            future = submit_future(executor, task, i, table, hdfs)
            future.cancel()
            futures.append(future)

    results = []
    for future in as_completed(futures):
        if future.cancelled():
            print("[Main] Task was cancelled")
        else:
            index, birthday, output = future.result()
            print(f"[Main] Task {index}: {birthday} -> {output}")
            results.append(output)

    return results





if __name__ == "__main__":
    # init
    # env()
    # hdfs = fs.HadoopFileSystem("default", 0, user="vscode")
    dummy_file(None, DUMMY_FILE)

    # main
    results = main(None, DUMMY_FILE)

    # just check the first file
    print("\n=== Display ===")
    for f in results:
        print(f"\n=== {f} ===")
        display_parquet(None, f)
        break
