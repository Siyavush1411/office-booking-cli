import sqlite3


class BaseModel:
    db_path = "booking.db"
    foreign_keys = {}

    def add(self):
        fields = [f for f in self.__annotations__.keys() if f != "id"]
        values = [getattr(self, f) for f in fields]

        placeholders_str = ", ".join("?" for _ in fields)

        sql = f"""
            insert into {self.__class__.__name__.lower()}
            ({', '.join(fields)}) values ({placeholders_str})
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(sql, values)
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def get(cls, field: str, value: any):
        conn = sqlite3.connect(cls.db_path)
        cursor = conn.execute(f"select * from {cls.__name__.lower()} where {field}=?", (value,))
        row = cursor.fetchone()
        column_names = [name[0] for name in cursor.description]
        conn.close()
        if row:
            data = {name: value for name, value in zip(column_names, row)}
            id_value = data.pop("id", None)
            obj = cls(**data)
            obj.id = id_value
            return obj
        return None

    @classmethod
    def get_all(cls):
        conn = sqlite3.connect(cls.db_path)
        cursor = conn.execute(f"select * from {cls.__name__.lower()}")
        rows = cursor.fetchall()
        column_names = [name[0] for name in cursor.description]
        conn.close()
        objects: list[cls] = []
        for row in rows:
            data = {name: value for name, value in zip(column_names, row)}
            id_value = data.pop("id", None)
            obj = cls(**data)
            obj.id = id_value
            objects.append(obj)
        return objects

    @classmethod
    def update(cls, id: int, **kwargs):
        fields = list(kwargs.keys())
        values = list(kwargs.values())
        set_clauses = [f"{field} = ?" for field in fields]
        sql = f"""
            update {cls.__name__.lower()}
            set {', '.join(set_clauses)}
            where id = ?
        """
        conn = sqlite3.connect(cls.db_path)
        conn.execute(sql, values + [id])
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, id: int):
        sql = f"delete from {cls.__name__.lower()} where id = ?"
        conn = sqlite3.connect(cls.db_path)
        conn.execute(sql, (id,))
        conn.commit()
        conn.close()
