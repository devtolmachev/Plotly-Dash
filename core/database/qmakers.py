from typing import Collection

from utils.exceptions import NotImplementedMethod


class BaseQM:

    def create(self):
        raise NotImplementedMethod

    def delete(self):
        raise NotImplementedMethod

    def select(self):
        raise NotImplementedMethod

    def update(self):
        raise NotImplementedMethod


class QMaker(BaseQM):

    @staticmethod
    def create(table_name: str, *,
               columns: Collection,
               values: Collection,
               if_not_ex: bool = True,
               **kwargs):
        """
        Формирует запрос CREATE, подразумевается что будет создаваться таблица
        """

        where = []
        for key, value in kwargs.items():
            if not where:
                where.append(f'WHERE {key} {value}')
            else:
                where.append(f'AND {key} {value}')

        columns_ = f"({', '.join(columns)})"
        values_ = f"""('{"', '".join(values)}')"""
        main_word = (f'CREATE TABLE IF NOT EXISTS {table_name}'
                     if if_not_ex is True else f'CREATE TABLE {table_name}')

        query = f"{main_word}{columns_} VALUES{values_} {' '.join(where)};"

        return query

    @staticmethod
    def update(table_name: str, *,
               column: str,
               value: str,
               **kwargs):
        """
        Формирует запрос UPDATE в Базу Данных
        """

        where = []
        for key_d, value_d in kwargs.items():
            if not where:
                where.append(f'WHERE {key_d} {value_d}')
            else:
                where.append(f'AND {key_d} {value_d}')

        main_word = f"UPDATE {table_name}"
        what_update = f"SET {column} = ('{value}')"

        query = f"{main_word} {what_update} {' '.join(where)};"

        return query

    @staticmethod
    def delete(table: str, **kwargs):
        where = []
        for key_d, value_d in kwargs.items():
            if not where:
                where.append(f'WHERE {key_d} {value_d}')
            else:
                where.append(f'AND {key_d} {value_d}')

        main_word = f"DELETE FROM {table}"
        query = f"{main_word} {' '.join(where)};"
        return query

    @staticmethod
    def select(table_name: str, *,
               columns: Collection,
               **kwargs):
        where = []
        for key_d, value_d in kwargs.items():
            if not where:
                where.append(f'WHERE {key_d} {value_d}')
            else:
                where.append(f'AND {key_d} {value_d}')

        columns_ = f"({', '.join(columns)})" if len(columns) > 1 else columns
        main_word = f"SELECT {columns_}"
        query = f"{main_word} FROM {table_name} {' '.join(where)};"
        return query

# qm = QMaker()
# create = qm.create('users', columns=['id', 'name'], values=['555', 'Daniil'])
# update = qm.update('users', column='status', value='Admin', id=f"LIKE '789%'")
# delete = qm.delete('users', last_online=F"LIKE '201%'")
# select = qm.select('users', columns=['id', 'name', 'email', 'phone'],
#                    balance=f"LIKE '100000%'")
# print(create)
# print(update)
# print(delete)
# print(select)
