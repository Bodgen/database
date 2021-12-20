import datetime
from typing import Union, List, Tuple, Any

import psycopg2 as ps


class Model:
    def __init__(self):
        self.conn = None
        try:
            self.conn = ps.connect(
                database="Lab1",
                user='postgres',
                password="qwerty123",
                host='127.0.0.1',
                port="5432",
            )
        except(Exception, ps.DatabaseError) as error:
            print("[INFO] Error while working with Postgresql", error)

    def request(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return True
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def get(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return cursor.fetchall()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def get_el(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return cursor.fetchone()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def count(self, table_name: str):
        return self.get_el(f"select count(*) from public.\"{table_name}\"")

    def find(self, table_name: str, key_name: str, key_value: int):
        return self.get_el(f"select count(*) from public.\"{table_name}\" where {key_name}={key_value}")

    def max(self, table_name: str, key_name: str):
        return self.get_el(f"select max({key_name}) from public.\"{table_name}\"")

    def min(self, table_name: str, key_name: str):
        return self.get_el(f"select min({key_name}) from public.\"{table_name}\"")

    def print_users(self) -> None:
        return self.get(f"SELECT * FROM public.\"user\"")

    def print_baskets(self) -> None:
        return self.get(f"SELECT * FROM public.\"basket\"")

    def print_devices(self) -> None:
        return self.get(f"SELECT * FROM public.\"device\"")

    def print_types(self) -> None:
        return self.get(f"SELECT * FROM public.\"type\"")

    def print_brands(self) -> None:
        return self.get(f"SELECT * FROM public.\"brand\"")

    def delete_data(self, table_name: str, key_name: str, key_value) -> None:
        self.request(f"DELETE FROM public.\"{table_name}\" WHERE {key_name}={key_value};")

    def update_data_basket(self, key_value: int, user_id: int, device_id: int) -> None:
        self.request(f"UPDATE public.\"basket\" SET user_id=\'{user_id}\', device_id={device_id} "
                     f"WHERE id={key_value};")

    def update_data_device(self, key_value: int, price: int, type_id: int, brand_id: int, name: str) -> None:
        self.request(f"UPDATE public.\"device\" SET price=\'{price}\', type_id={type_id}, "
                     f"brand_id=\'{brand_id}\',name =\'{name}\' WHERE id={key_value};")

    def update_data_type(self, key_value: int, name: str) -> None:
        self.request(f"UPDATE public.\"type\" SET name=\'{name}\' WHERE id={key_value};")

    def update_data_brand(self, key_value: int, type_id: int, name: str, country: str) -> None:
        self.request(
            f"UPDATE public.\"brand\" SET type_id = \'{type_id}\', name=\'{name}\',country=\'{country}\' WHERE id={key_value};")

    def update_data_user(self, key_value: int, name: str, email: str) -> None:
        self.request(f"UPDATE public.\"user\" SET name=\'{name}\', "
                     f"email=\'{email}\' WHERE id={key_value};")

    def insert_data_basket(self, id: int, device_id: int, user_id: int) -> None:
        self.request(f"insert into public.\"basket\" (id,device_id,user_id) "
                     f"VALUES ({id}, \'{device_id}\', \'{user_id}\');")

    def insert_data_device(self, id: int, price: int, type_id: int, brand_id: int, name: str) -> None:
        self.request(f"insert into public.\"device\" (id, price, type_id,brand_id,name ) "
                     f"VALUES ({id}, \'{price}\', {type_id}, \'{brand_id}\',\'{name}\');")

    def insert_data_type(self, id: int, name: str) -> None:
        self.request(f"insert into public.\"type\" (id, name) "
                     f"VALUES ({id}, \'{name}\');")

    def insert_data_brand(self, id: int, type_id: int, name: str, country: str) -> None:
        self.request(f"insert into public.\"brand\" (id,type_id, name,country) "
                     f"VALUES ({id}, \'{type_id}\', \'{name}\', \'{country}\');")

    def insert_data_user(self, id: int, name: str, email: str) -> None:
        self.request(f"insert into public.\"user\" (id,name,email) "
                     f"VALUES ({id}, \'{name}\', \'{email}\');")

    def user_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"user\""
                         "select (SELECT MAX(id)+1 FROM public.\"user\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), ''), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''); ")

    def basket_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"basket\" select (SELECT (MAX(id)+1) FROM public.\"basket\"), "
                         "(SELECT id FROM public.\"device\" LIMIT 1 OFFSET (round(random() * "
                         "((SELECT COUNT(id) FROM public.\"device\")-1)))),"
                         "(SELECT id FROM public.\"user\" LIMIT 1 OFFSET "
                         "(round(random() * ((SELECT COUNT(id) FROM public.\"user\")-1))));")

    def device_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"device\" select (SELECT MAX(id)+1 FROM public.\"device\"), "
                         "FLOOR(RANDOM()*(100000-1)+1),"
                         "(SELECT id FROM public.\"type\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.\"type\")-1)))), "
                         "(SELECT id FROM public.\"brand\" LIMIT 1 OFFSET "
                         "(round(random() * ((SELECT COUNT(id) FROM public.\"brand\")-1)))),"
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), '')  ;")

    def type_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"type\" select (SELECT MAX(id)+1 FROM public.\"type\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), ''); ")

    def brand_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"brand\" select (SELECT MAX(id)+1 FROM public.\"brand\"), "
                         "(SELECT id FROM public.\"type\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.\"type\")-1)))), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer)\
                          FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), ''),"
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), ''); ")

    def search_data_two_tables(self, table1_name: str, table2_name: str, table1_key, table2_key,
                               search: str):
        return self.get(f"select * from public.\"{table1_name}\" as one inner join public.\"{table2_name}\" as two "
                        f"on one.\"{table1_key}\"=two.\"{table2_key}\" "
                        f"where {search}")

    def search_data_three_tables(self, table1_name: str, table2_name: str, table3_name: str,
                                 table1_key, table2_key, table3_key, table13_key,
                                 search: str):
        return self.get(f"select * from public.\"{table1_name}\" as one inner join public.\"{table2_name}\" as two "
                        f"on one.\"{table1_key}\"=two.\"{table2_key}\" inner join public.\"{table3_name}\" as three "
                        f"on three.\"{table3_key}\"=one.\"{table13_key}\""
                        f"where {search}")

    def search_data_all_tables(self, table1_name: str, table2_name: str, table3_name: str, table4_name: str,
                               table1_key, table2_key, table3_key, table13_key,
                               table4_key, table24_key,
                               search: str):
        return self.get(f"select * from public.\"{table1_name}\" as one inner join public.\"{table2_name}\" as two "
                        f"on one.\"{table1_key}\"=two.\"{table2_key}\" inner join public.\"{table3_name}\" as three "
                        f"on three.\"{table3_key}\"=one.\"{table13_key}\" inner join public.\"{table4_name}\" as four "
                        f"on four.\"{table4_key}\"=two.\"{table24_key}\""
                        f"where {search}")
