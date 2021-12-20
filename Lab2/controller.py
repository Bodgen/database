from psycopg2 import Error
import model
import view
import datetime
import time


class Controller:
    def __init__(self):
        self.v = view.View()
        self.m = model.Model()

    def print(self, table_name):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'user':
                self.v.print_user(self.m.print_users())
            elif t_name == 'basket':
                self.v.print_basket(self.m.print_baskets())
            elif t_name == 'device':
                self.v.print_device(self.m.print_devices())
            elif t_name == 'type':
                self.v.print_type(self.m.print_types())
            elif t_name == 'brand':
                self.v.print_brand(self.m.print_brands())

    def delete(self, table_name, key_name, value):
        t_name = self.v.valid.check_table_name(table_name)
        k_name = self.v.valid.check_pk_name(table_name, key_name)
        if t_name and k_name:
            count = self.m.find(t_name, k_name, value)
            k_val = self.v.valid.check_pk(value, count)
            if k_val:
                if t_name == 'device' or t_name == 'user':
                    if t_name == 'device':
                        count_b = self.m.find('basket', 'device_id', value)[0]
                    if t_name == 'user':
                        count_b = self.m.find('basket', 'user_id', value)[0]
                    if count_b:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'brand' or t_name == 'type':
                    if t_name == 'brand':
                        count_b = self.m.find('device', 'brand_id', value)[0]
                    if t_name == 'type':
                        count_t = self.m.find('device', 'id_type', value)[0]
                    if count_b or count_t:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'brand':
                    count_t = self.m.find('type', 'type_id', value)[0]
                    if count_t:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)

                else:
                    try:
                        self.m.delete_data(table_name, key_name, k_val)
                    except (Exception, Error) as _ex:
                        self.v.sql_error(_ex)
            else:
                self.v.deletion_error()

    def update_basket(self, key: int, device_id: int, user_id: int):
        if self.v.valid.check_possible_keys('basket', 'id', key):
            count_b = self.m.find('basket', 'id', key)
            b_val = self.v.valid.check_pk(key, count_b)
        if self.v.valid.check_possible_keys('device', 'id', device_id):
            count_d = self.m.find('device', 'id', device_id)
            d_val = self.v.valid.check_pk(device_id, count_d)
        if self.v.valid.check_possible_keys('user', 'id', user_id):
            count_u = self.m.find('user', 'id', user_id)
            u_val = self.v.valid.check_pk(user_id, count_u)

        if b_val and d_val and u_val:
            try:
                self.m.update_data_basket(b_val, d_val, u_val, )
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_device(self, key: int, price: int, type_id: int, brand_id: int, name: str):
        if self.v.valid.check_possible_keys('device', 'id', key):
            count_d = self.m.find('device', 'id', key)
            d_val = self.v.valid.check_pk(key, count_d)
        if self.v.valid.check_possible_keys('type', 'id', type_id):
            count_t = self.m.find('type', 'id', type_id)
            t_val = self.v.valid.check_pk(type_id, count_t)

        if self.v.valid.check_possible_keys('brand', 'id', brand_id):
            count_b = self.m.find('brand', 'id', brand_id)
            b_val = self.v.valid.check_pk(brand_id, count_b)

        if d_val and t_val and b_val and self.v.valid.check_possible_keys('device', 'price', price):
            try:
                self.m.update_data_device(d_val, price, t_val, b_val, name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_type(self, key: int, name: str):
        if self.v.valid.check_possible_keys('type', 'id', key):
            count_t = self.m.find('type', 'id', key)
            t_val = self.v.valid.check_pk(key, count_t)

        if t_val and self.v.valid.check_possible_keys('type', 'name', name):
            try:
                self.m.update_data_type(t_val, name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_brand(self, key: int, type_id: int, name: str, country: str):
        if self.v.valid.check_possible_keys('brand', 'id', key):
            count_b = self.m.find('brand', 'id', key)
            b_val = self.v.valid.check_pk(key, count_b)

        if self.v.valid.check_possible_keys('type', 'id', type_id):
            count_t = self.m.find('type', 'id', type_id)
            t_val = self.v.valid.check_pk(type_id, count_t)

        if b_val and t_val and self.v.valid.check_possible_keys('brand', 'name', name):
            try:
                self.m.update_data_brand(b_val, type_id, name, country)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_user(self, key: str, name: str, email: str):
        if self.v.valid.check_possible_keys('user', 'id', key):
            count_u = self.m.find('user', 'id', int(key))
            u_val = self.v.valid.check_pk(key, count_u)
        if u_val:
            try:
                self.m.update_data_user(u_val, name, email)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def insert_user(self, key: str, name: str, email: str):
        if self.v.valid.check_possible_keys('user', 'id', key):
            count_u = self.m.find('user', 'id', int(key))[0]
        if (not count_u or count_u == (0,)) and self.v.valid.check_possible_keys('user', 'id', key):
            try:
                self.m.insert_data_user(int(key), name, email)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_basket(self, key: int, device_id: int, user_id: int):
        if self.v.valid.check_possible_keys('basket', 'id', key):
            count_b = self.m.find('basket', 'id', key)[0]

        if self.v.valid.check_possible_keys('device', 'id', device_id):
            count_bd = self.m.find('device', 'id', device_id)
            bd_val = self.v.valid.check_pk(device_id, count_bd)

        if self.v.valid.check_possible_keys('user', 'id', user_id):
            count_bu = self.m.find('user', 'id', user_id)
            bu_val = self.v.valid.check_pk(user_id, count_bu)

        if (not count_b or count_b == (0,)) and bu_val and bd_val \
                and self.v.valid.check_possible_keys('basket', 'id', key):
            try:
                self.m.insert_data_basket(int(key), bd_val, bu_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_device(self, key: str, price: int, type_id: int, brand_id: int, name: str):
        if self.v.valid.check_possible_keys('device', 'id', key):
            count_d = self.m.find('device', 'id', int(key))[0]

        if self.v.valid.check_possible_keys('type', 'id', type_id):
            count_dt = self.m.find('type', 'id', type_id)
            dt_val = self.v.valid.check_pk(type_id, count_dt)

        if self.v.valid.check_possible_keys('brand', 'id', brand_id):
            count_db = self.m.find('brand', 'id', brand_id)
            db_val = self.v.valid.check_pk(brand_id, count_db)

        if (not count_d or count_d == (0,)) and dt_val and db_val and self.v.valid.check_possible_keys('device', 'id',
                                                                                                       key):
            try:
                self.m.insert_data_device(int(key), price, dt_val, db_val, name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_type(self, key: str, name: str):
        if self.v.valid.check_possible_keys('type', 'id', key):
            count_t = self.m.find('type', 'id', int(key))[0]
        if (not count_t or count_t == (0,)) and self.v.valid.check_possible_keys('type', 'id', key):
            try:
                self.m.insert_data_type(int(key), name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_brand(self, key: str, type_id: int, name: str, country: str):
        if self.v.valid.check_possible_keys('brand', 'id', key):
            count_b = self.m.find('brand', 'id', int(key))[0]

        if self.v.valid.check_possible_keys('type', 'id', type_id):
            count_bt = self.m.find('type', 'id', type_id)
            bt_val = self.v.valid.check_pk(type_id, count_bt)

        if (not count_b or count_b == (0,)) and bt_val and self.v.valid.check_possible_keys('brand', 'id', key):
            try:
                self.m.insert_data_brand(int(key), bt_val, name, country)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def generate(self, table_name: str, n: int):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'user':
                self.m.user_data_generator(n)
            elif t_name == 'basket':
                self.m.basket_data_generator(n)
            elif t_name == 'device':
                self.m.device_data_generator(n)
            elif t_name == 'type':
                self.m.type_data_generator(n)
            elif t_name == 'brand':
                self.m.brand_data_generator(n)

    def search_two(self, table1_name: str, table2_name: str, table1_key: str, table2_key: str, search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and t2_n \
                and self.v.valid.check_key_names(t2_n, table2_key):
            start_time = time.time()
            result = self.m.search_data_two_tables(table1_name, table2_name, table1_key, table2_key,
                                                   search)
            self.v.print_time(start_time)

            self.v.print_search(result)

    def search_three(self, table1_name: str, table2_name: str, table3_name: str,
                     table1_key: str, table2_key: str, table3_key: str, table13_key: str,
                     search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        t3_n = self.v.valid.check_table_name(table3_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and self.v.valid.check_key_names(t1_n, table13_key) \
                and t2_n and self.v.valid.check_key_names(t2_n, table2_key) \
                and t3_n and self.v.valid.check_key_names(t3_n, table3_key) \
                and self.v.valid.check_key_names(t3_n, table13_key):
            start_time = time.time()
            result = self.m.search_data_three_tables(table1_name, table2_name, table3_name,
                                                     table1_key, table2_key, table3_key, table13_key,
                                                     search)
            self.v.print_time(start_time)
            self.v.print_search(result)

    def search_four(self, table1_name: str, table2_name: str, table3_name: str, table4_name: str,
                    table1_key: str, table2_key: str, table3_key: str, table13_key: str,
                    table4_key: str, table24_key: str,
                    search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        t3_n = self.v.valid.check_table_name(table3_name)
        t4_n = self.v.valid.check_table_name(table2_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and self.v.valid.check_key_names(t1_n, table13_key) \
                and t2_n and self.v.valid.check_key_names(t2_n, table2_key) \
                and self.v.valid.check_key_names(t2_n, table24_key) \
                and t3_n and self.v.valid.check_key_names(t3_n, table3_key) \
                and self.v.valid.check_key_names(t3_n, table13_key) \
                and t4_n and self.v.valid.check_key_names(t4_n, table4_key) \
                and self.v.valid.check_key_names(t4_n, table24_key):
            start_time = time.time()
            result = self.m.search_data_all_tables(table1_name, table2_name, table3_name, table4_name,
                                                   table1_key, table2_key, table3_key, table13_key,
                                                   table4_key, table24_key,
                                                   search)
            self.v.print_time(start_time)
            self.v.print_search(result)
