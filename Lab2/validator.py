import datetime


class Validator:
    def __init__(self):
        self.error = ''
        self.er_flag = False

    def check_table_name(self, arg: str):
        if arg in ['user', 'basket', 'device', 'type', 'brand']:
            return arg
        else:
            self.er_flag = True
            self.error = f'table {arg} does not exist in the database'
            print(self.error)
            return False

    def check_pkey_value(self, arg: str, min_val: int, max_val: int):
        try:
            value = int(arg)
        except ValueError:
            self.er_flag = True
            self.error = f'{arg} is not correct primary key value'
            print(self.error)
            return 0
        else:
            if min_val <= value <= max_val:
                return value
            else:
                self.er_flag = True
                self.error = f'{arg} is not existing primary key value'
                print(self.error)
                return 0

    def check_pk_name(self, table_name: str, key_name: str):
        if table_name == 'user' and key_name == 'id' \
                or table_name == 'basket' and key_name == 'id' \
                or table_name == 'device' and key_name == 'id' \
                or table_name == 'type' and key_name == 'id' \
                or table_name == 'brand' and key_name == 'id':
            return key_name
        else:
            self.er_flag = True
            self.error = f'key {key_name} is not a primary key of table {table_name}'
            print(self.error)
            return False

    def check_pk(self, val, count):
        try:
            value = int(val)
        except ValueError:
            self.er_flag = True
            self.error = f'{val} is not correct primary key value'
            print(self.error)
            return 0
        else:
            if count and not count == (0,):
                return value
            else:
                return 0

    def check_key_names(self, table_name: str, key: str):
        if table_name == 'user' and key in ['id', 'name', 'email']:
            return True
        elif table_name == 'basket' and key in ['id', 'device_id', 'user_id']:
            return True
        elif table_name == 'device' and key in ['id', 'price', 'type_id', 'brand_id', 'name']:
            return True
        elif table_name == 'type' and key in ['id', 'name']:
            return True
        elif table_name == 'brand' and key in ['id', 'type_id', 'name', 'country']:
            return True
        else:
            self.er_flag = True
            self.error = f'{key} is not correct name for {table_name} table'
            print(self.error)
            return False

    def check_possible_keys(self, table_name: str, key: str, val):
        if table_name == 'basket':
            if key in ['id', 'device_id', 'user_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Product table'
                print(self.error)
                return False
        elif table_name == 'device':
            if key in ['id', 'type_id', 'brand_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key == 'name':
                return True
            elif key == 'price':
                try:
                    value = float(val)
                except TypeError:
                    self.er_flag = True
                    self.error = f'{val} is not correct date value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Order table'
                print(self.error)
                return False
        elif table_name == 'type':
            if key == 'id':
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key == 'name':
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Product table'
                print(self.error)
                return False
        elif table_name == 'brand':
            if key in ['id','type_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['name','country']:
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for user table'
                print(self.error)
                return False

        elif table_name == 'user':
            if key == 'id':
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['name', 'email']:
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for user table'
                print(self.error)
                return False
