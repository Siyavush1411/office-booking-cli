import sqlite3
from typing import Type
from typing import Any


class Migration:
    def __init__(self, cls: list):
        self.cls = cls

    def migrate(self):
        conn = sqlite3.connect("booking.db")
        c = conn.cursor()
        for cls in self.cls:
            table_name = self._get_class_name(cls)
            fields = cls.__annotations__.items()
            self._create_table(c, table_name, cls.foreign_keys)
            self._check_commits(c, table_name, dict(fields))
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

    def _create_table(
        self, c: sqlite3.Cursor, table_name: str, foreign_keys: dict = {}
    ):
        columns = ["id integer primary key autoincrement"]
        columns += [f"{field} integer" for field in foreign_keys.keys()]
        fk_str = ForeignKeyBase()._add_foreign_keys(foreign_keys)
        if fk_str:
            columns.append(fk_str.strip())
        c.execute(
            f"""
            create table if not exists {table_name} (
                {", ".join(columns)}
            );
            """
        )

    def _add_column(
        self, c: sqlite3.Cursor, table_name: str, field_name: str, field_type: str
    ):
        c.execute(
            f"""
            alter table {table_name}
            add column {field_name} {field_type};
            """
        )

    def __get_table_schema__(self, c: sqlite3.Cursor, table_name: str):
        c.execute(f"select * from {table_name} limit 1")
        schema = [name[0] for name in c.description]
        return schema

    def _check_commits(self, c: sqlite3.Cursor, table_name: str, model_schema: dict):
        current_schema = self.__get_table_schema__(c, table_name)
        for field, field_type in model_schema.items():
            if field not in current_schema:
                print(field, self._map_type(field_type), "-----", current_schema)
                self._add_column(
                    c,
                    table_name=table_name,
                    field_name=field,
                    field_type=self._map_type(field_type),
                )
        for field in current_schema:
            if field not in model_schema:
                self._delete_column(c, table_name, field)

    def _delete_column(self, c: sqlite3.Cursor, table_name: str, field_name: str):
        c.execute(
            f"""
            alter table {table_name}
            drop column {field_name};
            """
        )


class ForeignKeyBase:
    def _add_foreign_keys(self, foreign_keys: dict) -> str:
        result = ""
        for field, (ref_table, ref_field) in foreign_keys.items():
            result += f"foreign key ({field}) references {ref_table}({ref_field})"
        return result
