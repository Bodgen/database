from psycopg2 import Error
import controller as con
import sys

c = con.Controller()

try:
    command = sys.argv[1]
except IndexError:
    c.v.no_command()
else:
    if command == 'print_table':
        try:
            name = sys.argv[2]
        except IndexError:
            c.v.argument_error()
        else:
            c.print(name)

    elif command == 'delete_record':
        try:
            args = {"title": sys.argv[2], "key": sys.argv[3], "val": sys.argv[4]}
        except IndexError:
            c.v.argument_error()
        else:
            c.delete(args["title"], args["key"], args["val"])

    elif command == 'update_record':
        try:
            args = {"title": sys.argv[2], "key": sys.argv[3]}
            if args["title"] == 'user':
                args["name"], args["email"] = \
                    sys.argv[4], sys.argv[5]
            elif args["title"] == 'basket':
                args["device_id"], args["user_id"] = \
                    sys.argv[4], sys.argv[5]
            elif args["title"] == 'device':
                args["price"], args["type_id"], args["brand_id"], args["name"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
            elif args["title"] == 'type':
                args["name"] = \
                    sys.argv[4]
            elif args["title"] == 'brand':
                args["type_id"], args["name"], args["country"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            else:
                c.v.wrong_table()
        except IndexError:
            c.v.argument_error()
        else:
            if args["title"] == 'user':
                c.update_user(args["key"], args["name"], args["email"])
            elif args["title"] == 'basket':
                c.update_basket(args["key"], args["device_id"], args["user_id"])
            elif args["title"] == 'device':
                c.update_device(args["key"], args["price"], args["type_id"], args["brand_id"], args["name"])
            elif args["title"] == 'type':
                c.update_type(args["key"], args["name"])
            elif args["title"] == 'brand':
                c.update_brand(args["key"], args["type_id"], args["name"], args["country"])

    elif command == 'insert_record':
        try:
            args = {"title": sys.argv[2], "key": sys.argv[3]}
        except IndexError:
            c.v.argument_error()
        else:
            if args["title"] == 'user':
                args["name"], args["email"] = \
                    sys.argv[4], sys.argv[5]
            elif args["title"] == 'basket':
                args["device_id"], args["user_id"] = \
                    sys.argv[4], sys.argv[5]
            elif args["title"] == 'device':
                args["price"], args["type_id"], args["brand_id"], args["name"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
            elif args["title"] == 'type':
                args["name"] = \
                    sys.argv[4]
            elif args["title"] == 'brand':
                args["type_id"], args["name"], args["country"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            else:
                c.v.wrong_table()
            if args["title"] == 'user':
                c.insert_user(args["key"], args["name"], args["email"])
            elif args["title"] == 'basket':
                c.insert_basket(args["key"], args["device_id"], args["user_id"])
            elif args["title"] == 'device':
                c.insert_device(args["key"], args["price"], args["type_id"], args["brand_id"], args["name"])
            elif args["title"] == 'type':
                c.insert_type(args["key"], args["name"])
            elif args["title"] == 'brand':
                c.insert_brand(args["key"], args["type_id"], args["name"], args["country"])

    elif command == 'generate_randomly':
        try:
            args = {"title": sys.argv[2], "n": int(sys.argv[3])}
        except (IndexError, Exception):
            print(Exception, IndexError)
        else:
            c.generate(args["title"], args["n"])

    elif command == 'search_records':
        if len(sys.argv) in [6, 9, 12]:
            search_num = c.v.get_search_num()
            try:
                search_num = int(search_num)
            except ValueError:
                c.v.invalid_search_num()
            else:
                if search_num > 0:
                    if len(sys.argv) == 6:
                        args = {"table1_name": sys.argv[2], "table2_name": sys.argv[3],
                                "key1_name": sys.argv[4], "key2_name": sys.argv[5]}
                        c.search_two(args["table1_name"], args["table2_name"], args["key1_name"], args["key2_name"],
                                     c.v.proceed_search(search_num))
                    elif len(sys.argv) == 9:
                        args = {"table1_name": sys.argv[2], "table2_name": sys.argv[3], "table3_name": sys.argv[4],
                                "key1_name": sys.argv[5], "key2_name": sys.argv[6], "key3_name": sys.argv[7],
                                "key13_name": sys.argv[8]}
                        c.search_three(args["table1_name"], args["table2_name"], args["table3_name"],
                                       args["key1_name"], args["key2_name"], args["key3_name"], args["key13_name"],
                                       c.v.proceed_search(search_num))
                    elif len(sys.argv) == 12:
                        args = {"table1_name": sys.argv[2], "table2_name": sys.argv[3], "table3_name": sys.argv[4],
                                "table4_name": sys.argv[5],
                                "key1_name": sys.argv[6], "key2_name": sys.argv[7], "key3_name": sys.argv[8],
                                "key13_name": sys.argv[9], "key4_name": sys.argv[10], "key24_name": sys.argv[11]}
                        c.search_four(args["table1_name"], args["table2_name"], args["table3_name"],
                                      args["table4_name"],
                                      args["key1_name"], args["key2_name"], args["key3_name"], args["key13_name"],
                                      args["key4_name"], args["key24_name"], c.v.proceed_search(search_num))
                else:
                    c.v.invalid_search_num()
        else:
            c.v.argument_error()

    elif command == 'help':
        c.v.print_help()
    else:
        c.v.wrong_command()
