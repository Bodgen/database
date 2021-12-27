from psycopg2 import Error
import model
import view
import datetime


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
                self.v.print_basket(self.m.print_basket())
            elif t_name == 'device':
                self.v.print_device(self.m.print_device())
            elif t_name == 'type':
                self.v.print_type(self.m.print_type())
            elif t_name == 'brand':
                self.v.print_brand(self.m.print_brand())

    def delete(self, table_name, value):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            k_val = self.v.valid.check_pk(value)
            count = 0
            if t_name == 'user' and k_val:
                count = self.m.find_pk_user(k_val)
            elif t_name == 'basket' and k_val:
                count = self.m.find_pk_basket(k_val)
            elif t_name == 'device' and k_val:
                count = self.m.find_pk_device(k_val)
            elif t_name == 'type' and k_val:
                count = self.m.find_pk_type(k_val)
            elif t_name == 'brand' and k_val:
                count = self.m.find_pk_brand(k_val)

            if count:
                if t_name == 'user' or t_name == 'device':
                    count_b = self.m.find_fk_basket(k_val, t_name)
                    if count_b:
                        self.v.cannot_delete()
                    else:
                        try:
                            if t_name == 'user':
                                self.m.delete_data_user(k_val)
                            elif t_name == 'device':
                                self.m.delete_data_device(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'type' or t_name == 'brand':
                    count_d = self.m.find_fk_device(k_val, t_name)
                    if count_d:
                        self.v.cannot_delete()
                    else:
                        try:
                            if t_name == 'type':
                                self.m.delete_data_type(k_val)
                            elif t_name == 'brand':
                                self.m.delete_data_brand(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                else:
                    try:
                        self.m.delete_data_basket(k_val)
                    except (Exception, Error) as _ex:
                        self.v.sql_error(_ex)
            else:
                self.v.deletion_error()

    def update_user(self, key: int, name: str, email: str):
        if self.v.valid.check_possible_keys('user', 'id', key):
            count_u = self.m.find_pk_user(key)
            u_val = self.v.valid.check_pk(key)
        if count_u and u_val:
            try:
                self.m.update_data_user(u_val, name, email)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_basket(self, key: int, device_id: int, user_id: int):
        if self.v.valid.check_possible_keys('device', 'id', device_id):
            count_d = self.m.find_pk_device(device_id)
            d_val = self.v.valid.check_pk(device_id)
        if self.v.valid.check_possible_keys('basket', 'id', key):
            count_b = self.m.find_pk_basket(key)
            b_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('user', 'id', user_id):
            count_u = self.m.find_pk_user(user_id)
            u_val = self.v.valid.check_pk(user_id)

        if count_d and count_b and count_u \
                and d_val and b_val and u_val:
            try:
                self.m.update_data_basket(b_val, d_val, u_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_device(self, key: int, price: int, type_id: int, brand_id: int, name: str):
        if self.v.valid.check_possible_keys('device', 'id', key):
            count_d = self.m.find_pk_device(key)
            d_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('type', 'id', type_id):
            count_t = self.m.find_pk_type(type_id)
            t_val = self.v.valid.check_pk(type_id)
        if self.v.valid.check_possible_keys('brand', 'id', brand_id):
            count_b = self.m.find_pk_brand(brand_id)
            b_val = self.v.valid.check_pk(brand_id)

        if count_d and count_t and count_b and \
                d_val and t_val and b_val:
            try:
                self.m.update_data_device(d_val, price, t_val, d_val, name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_type(self, key: int, name: str):
        if self.v.valid.check_possible_keys('type', 'id', key):
            count_t = self.m.find_pk_type(key)
            t_val = self.v.valid.check_pk(key)

        if count_t and t_val:
            try:
                self.m.update_data_type(t_val, name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_brand(self, key: int, name: str, type_id: int, country: str):
        if self.v.valid.check_possible_keys('brand', 'id', key):
            count_b = self.m.find_pk_brand(key)
            b_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('type', 'type_id', type_id):
            count_t = self.m.find_pk_type(type_id)
            t_val = self.v.valid.check_pk(type_id)

        if count_t and count_b\
                and b_val and t_val:
            try:
                self.m.update_data_brand(b_val, name,t_val,country)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def insert_user(self, key: int, name: str,email: str):
        if self.v.valid.check_possible_keys('user', 'id', key):
            count_u = self.m.find_pk_user(key)

        if (not count_u) and self.v.valid.check_possible_keys('user', 'id', key):
            try:
                self.m.insert_data_user(key, name, email)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_basket(self, key: int, device_id: int, user_id: int):
        if self.v.valid.check_possible_keys('device', 'id', device_id):
            count_d = self.m.find_pk_device(device_id)
            d_val = self.v.valid.check_pk(device_id)
        if self.v.valid.check_possible_keys('user', 'id', user_id):
            count_u = self.m.find_pk_user(user_id)
            u_val = self.v.valid.check_pk(user_id)
        if self.v.valid.check_possible_keys('basket', 'id', key):
            count_b = self.m.find_pk_basket(key)

        if (not count_b) and count_d and count_u and d_val and u_val \
                and self.v.valid.check_possible_keys('basket', 'id', key):
            try:
                self.m.insert_data_basket(key, d_val, u_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_device(self, key: int, price: int, type_id: int, brand_id: int,name:str):
        if self.v.valid.check_possible_keys('device', 'id', key):
            count_d = self.m.find_pk_device(key)
        if self.v.valid.check_possible_keys('type', 'id', type_id):
            count_t = self.m.find_pk_type(type_id)
            t_val = self.v.valid.check_pk(type_id)
        if self.v.valid.check_possible_keys('brand', 'id', brand_id):
            count_b = self.m.find_pk_brand(brand_id)
            b_val = self.v.valid.check_pk(brand_id)

        if (not count_d) and count_t and count_b and t_val and b_val \
                and self.v.valid.check_possible_keys('device', 'id', key):
            try:
                self.m.insert_data_device(int, price, t_val, b_val, name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_type(self, key: int, name: str):
        if self.v.valid.check_possible_keys('type', 'id', key):
            count_t = self.m.find_pk_type(key)

        if (not count_t) and self.v.valid.check_possible_keys('type', 'id', key):
            try:
                self.m.insert_data_type(key,name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_brand(self, key: int, name: str, type_id: int, country:str):
        if self.v.valid.check_possible_keys('brand', 'id', key):
            count_b = self.m.find_pk_type(key)
        if self.v.valid.check_possible_keys('type', 'id', type_id):
            count_t = self.m.find_pk_type(type_id)
            t_val = self.v.valid.check_pk(type_id)

        if (not count_b) and count_t and t_val and self.v.valid.check_possible_keys('type', 'id', key):
            try:
                self.m.insert_data_brand(key, name,t_val,country)
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

    def search_two(self):
        result = self.m.search_data_two_tables()
        self.v.print_search(result)

    def search_three(self):
        result = self.m.search_data_three_tables()
        self.v.print_search(result)

    def search_four(self):
        result = self.m.search_data_four_tables()
        self.v.print_search(result)
