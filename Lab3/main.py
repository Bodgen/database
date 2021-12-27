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
            args = {"name": sys.argv[2], "val": sys.argv[3]}
        except IndexError:
            c.v.argument_error()
        else:
            c.delete(args["name"], args["val"])

    elif command == 'update_record':
        try:
            args = {"title": sys.argv[2], "key": sys.argv[3]}
            if args["title"] == 'user':
                args["name"], args["email"] = sys.argv[4], sys.argv[5]
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
                args['name'], args['type_id'], args['country'] = \
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
                c.update_device(args["key"], args["price"], args["type_id"], args["device_id"], args["name"])
            elif args["title"] == 'type':
                c.update_type(args["key"], args["name"])
            elif args["title"] == 'brand':
                c.update_brand(args["key"], args["name"], args["type_id"], args["country"])

    elif command == 'insert_record':
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
                args["name"], args['type_id'], args['country'] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            else:
                c.v.wrong_table()
        except IndexError:
            c.v.argument_error()
        else:
            if args["title"] == 'user':
                c.insert_user(args["key"], args["name"], args["email"])
            elif args["title"] == 'basket':
                c.insert_basket(args["key"], args["device_id"], args["user_id"])
            elif args["title"] == 'device':
                c.insert_device(args["key"], args["price"], args["type_id"], args["brand_id"],args['name'])
            elif args["title"] == 'type':
                c.insert_type(args["key"], args["name"])
            elif args["title"] == 'brand':
                c.insert_brand(args["key"], args["name"], args["type_id"],args['country'])

    elif command == 'test':
        print(not c.m.find_product(13))
    elif command == 'generate_randomly':
        try:
            args = {"name": sys.argv[2], "n": int(sys.argv[3])}
        except (IndexError, Exception):
            print(Exception, IndexError)
        else:
            c.generate(args["name"], args["n"])

    elif command == 'search_records':
        while True:
            search_num = c.v.get_search_num()
            try:
                search_num = int(search_num)
            except ValueError:
                c.v.invalid_search_num()
            else:
                if search_num in [2, 3, 4]:
                    break
                else:
                    c.v.invalid_search_num()
        if search_num == 2:
            c.search_two()
        elif search_num == 3:
            c.search_three()
        elif search_num == 4:
            c.search_four()

    elif command == 'help':
        c.v.print_help()
    else:
        c.v.wrong_command()
