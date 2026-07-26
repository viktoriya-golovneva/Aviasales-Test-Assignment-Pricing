import duckdb
from pathlib import Path

_PROJECT_ROOT = Path(__file__).parent
_DATA_DIR = _PROJECT_ROOT / "data"
_DB_PATH = _PROJECT_ROOT / "aviasales.duckdb"

_TABLES = {
    "task_2_costs":       "task_2_costs.csv",
    "task_2_installs":   "task_2_installs.csv",
    "task_2_purchases":  "task_2_purchases.csv",
    "task_3_data":       "task_3_data.csv"
}


def get_con() -> duckdb.DuckDBPyConnection:
    for path in [_DB_PATH, _DB_PATH.with_suffix(".duckdb.wal")]:
        if path.exists():
            path.unlink()

    con = duckdb.connect(str(_DB_PATH))

    print("Setting up database tables...")
    for table_name, filename in _TABLES.items():
        csv_path = _DATA_DIR / filename
        con.execute(
            f"CREATE TABLE {table_name} AS "
            f"SELECT * FROM read_csv_auto('{csv_path.as_posix()}')"
        )
    print("Done. All tables are ready.")

    return con
