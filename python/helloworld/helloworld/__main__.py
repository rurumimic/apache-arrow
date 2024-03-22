import functools
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

DEST_DIR = "out"
MAX_WORKERS = 3


def task(index: int, table: pa.Table) -> Tuple[int, str]:
    year = table["years"][index].as_py()
    month = table["months"][index].as_py()
    day = table["days"][index].as_py()
    
    # Some computation
    if index == 0:
        groups = table.group_by("years").aggregate([("months", "count"), ("days", "count")])
        filter = pc.equal(groups["days_count"], 2)
        filtered = groups.filter(filter)
        print(f"=== Computation ===\n{filtered}\n===================")

    return (index, f"{year}.{month}.{day}")


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


def main():
    # Arrow
    years = pa.array([1990, 2000, 1995, 2000, 1995], type=pa.int16())
    months = pa.array([1, 3, 5, 7, 1], type=pa.int8())
    days = pa.array([1, 12, 17, 23, 28], type=pa.int8())

    birthdays_table = pa.table([years, months, days], names=["years", "months", "days"])

    # parquet
    dest_path = f"{DEST_DIR}/birthdays.parquet"
    pq.write_table(birthdays_table, dest_path)

    # Multi-threading
    futures = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for i in range(len(birthdays_table)):
            future = submit_future(executor, task, i, birthdays_table)
            future.cancel()
            futures.append(future)

    for future in as_completed(futures):
        if future.cancelled():
            print("[Main] Task was cancelled")
        else:
            index, birthday = future.result()
            print(f"[Main] Task {index}: {birthday}")


if __name__ == "__main__":
    main()

