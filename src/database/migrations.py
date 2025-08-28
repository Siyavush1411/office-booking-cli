import sqlite3
from typing import Type
from typing import Any

from src.database.database import init_db


class Migration:
    def __init__(self, cls: list):
        self.cls = cls

    def migrate(self):
        init_db()
        conn = sqlite3.connect("booking.db")
        c = conn.cursor()
        for cls in self.cls:
            table_name = self._get_class_name(cls)
            fields = cls.__annotations__.items()
            self._create_table(c, table_name)
            for field_name, field_type in fields:
                if not self._check_table_field(c, table_name, field_name):
                    self._add_column(
                        c, table_name, field_name, self._map_type(field_type)
                    )
        conn.commit()

    def _get_class_name(self, cls: Type) -> str:
        return cls.__name__.lower()

    def _map_type(self, py_type: type[Any]) -> str:
        type_mapping = {
            int: "INTEGER",
            str: "TEXT",
            float: "REAL",
            bool: "BOOLEAN",
            type(None): "NULL",
        }
        return type_mapping.get(py_type, "TEXT")

    def _check_table_field(
            self, c: sqlite3.Cursor, table_name: str, field_name: str
            ):
        c.execute(f"pragma table_info({table_name});")
        columns = [row[1] for row in c.fetchall()]
        if field_name in columns:
            return True
        return False

    def _create_table(self, c: sqlite3.Cursor, table_name: str):
        c.execute(
            f"""
            create table if not exists {table_name} (
                id integer primary key autoincrement
            );
            """
        )

    def _add_column(
            self, c: sqlite3.Cursor, table_name: str, field_name: str,
            field_type: str
            ):
        c.execute(
            f"""
            alter table {table_name}
            add column {field_name} {field_type};
            """
        )