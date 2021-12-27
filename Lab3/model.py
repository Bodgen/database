import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, select, and_
from sqlalchemy.orm import relationship
from db import Orders, Session, engine


def recreate_database():
    Orders.metadata.drop_all(engine)
    Orders.metadata.create_all(engine)


class User(Orders):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    baskets = relationship("Basket")

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return "{:>10}{:>30}{:>30}" \
            .format(self.id, self.name, self.email)


class Basket(Orders):
    __tablename__ = 'basket'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('device.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, id, device_id, user_id):
        self.id = id
        self.device_id = device_id
        self.user_id = user_id

    def __repr__(self):
        return "{:>10}{:>15}{:>10}" \
            .format(self.id, self.device_id, self.user_id)


class Device(Orders):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    type_id = Column(Integer, ForeignKey('type.id'))
    brand_id = Column(Integer, ForeignKey('brand.id'))
    name = Column(String)
    baskets = relationship("Basket")

    def __init__(self, id, price, type_id, brand_id, name):
        self.id = id
        self.price = price
        self.type_id = type_id
        self.brand_id = brand_id
        self.name = name

    def __repr__(self):
        return "{:>10}{:>15}{:>10}{:>15}{:>25}" \
            .format(self.id, self.price, self.type_id, self.brand_id, self.name)


class Type(Orders):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    devices = relationship('Device')

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "{:>10}{:>35}" \
            .format(self.id, self.name)


class Brand(Orders):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type_id = Column(Integer, ForeignKey('type.id'))
    country = Column(String)
    devices = relationship('Device')

    def __init__(self, id, name, type_id, country):
        self.id = id
        self.name = name
        self.type_id = type_id
        self.country = country

    def __repr__(self):
        return "{:>10}{:>35}{:>10}{:>35}" \
            .format(self.id, self.name, self.type_id, self.country)


class Model:
    def __init__(self):
        self.session = Session()
        self.connection = engine.connect()

    def find_pk_basket(self, key_value: int):
        return self.session.query(Basket).filter_by(id=key_value).first()

    def find_fk_basket(self, key_value: int, table_name: str):
        if table_name == "device":
            return self.session.query(Device).filter_by(id=key_value).first()
        if table_name == "user":
            return self.session.query(User).filter_by(id=key_value).first()

    def find_pk_device(self, key_value: int):
        return self.session.query(Device).filter_by(id=key_value).first()

    def find_fk_device(self, key_value: int, table_name: str):
        if table_name == "type":
            return self.session.query(Type).filter_by(id=key_value).first()
        if table_name == "brand":
            return self.session.query(Brand).filter_by(id=key_value).first()

    def find_pk_user(self, key_value: int):
        return self.session.query(User).filter_by(id=key_value).first()

    def find_pk_type(self, key_value: int):
        return self.session.query(Type).filter_by(id=key_value).first()

    def find_pk_brand(self, key_value: int):
        return self.session.query(Brand).filter_by(id=key_value).first()

    def find_fk_brand(self, key_value: int):
        return self.session.query(Type).filter_by(type_id=key_value).first()

    def print_users(self):
        return self.session.query(User).order_by(User.id.asc()).all()

    def print_basket(self):
        return self.session.query(Basket).order_by(Basket.id.asc()).all()

    def print_device(self):
        return self.session.query(Device).order_by(Device.id.asc()).all()

    def print_type(self):
        return self.session.query(Type).order_by(Type.id.asc()).all()

    def print_brand(self):
        return self.session.query(Brand).order_by(Brand.id.asc()).all()

    def delete_data_user(self, id) -> None:
        self.session.query(User).filter_by(id=id).delete()
        self.session.commit()

    def delete_data_basket(self, id) -> None:
        self.session.query(Basket).filter_by(id=id).delete()
        self.session.commit()

    def delete_data_device(self, id) -> None:
        self.session.query(Device).filter_by(id=id).delete()
        self.session.commit()

    def delete_data_type(self, id) -> None:
        self.session.query(Type).filter_by(id=id).delete()
        self.session.commit()

    def delete_data_brand(self, id) -> None:
        self.session.query(Brand).filter_by(id=id).delete()
        self.session.commit()

    def update_data_user(self, id: int, name: str, email: str) -> None:
        self.session.query(User).filter_by(id=id) \
            .update({User.name: name, User.email: email})
        self.session.commit()

    def update_data_basket(self, id: int, device_id: int, user_id: int) -> None:
        self.session.query(Basket).filter_by(id=id) \
            .update({Basket.device_id: device_id, Basket.user_id: user_id})
        self.session.commit()

    def update_data_device(self, id: int, price: int, type_id: int, brand_id: int, name: str) -> None:
        self.session.query(Device).filter_by(id=id) \
            .update({Device.price: price, Device.type_id: type_id, Device.brand_id: brand_id, Device.name: name})
        self.session.commit()

    def update_data_type(self, id: int, name: str) -> None:
        self.session.query(Type).filter_by(id=id) \
            .update({Type.name: name})
        self.session.commit()

    def update_data_brand(self, id: int, name: str, type_id: int, country: str) -> None:
        self.session.query(Brand).filter_by(id=id) \
            .update({Brand.name: name, Brand.type_id: type_id, Brand.country: country})
        self.session.commit()

    def insert_data_user(self, id: int, name: str, email: str) -> None:
        user = User(id=id, name=name, email=email)
        self.session.add(user)
        self.session.commit()

    def insert_data_basket(self, id: int, device_id: int, user_id: int) -> None:
        basket = Basket(id=id, device_id=device_id, user_id=user_id)
        self.session.add(basket)
        self.session.commit()

    def insert_data_device(self, id: int, price: int, type_id: int, brand_id: int, name: str) -> None:
        device = Device(id=id, price=price, type_id=type_id, brand_id=brand_id, name=name)
        self.session.add(device)
        self.session.commit()

    def insert_data_type(self, id: int, name: str) -> None:
        types = Type(id=id, name=name)
        self.session.add(types)
        self.session.commit()

    def insert_data_brand(self, id: int, name: str, type_id: int, country: str) -> None:
        brand = Brand(id=id, name=name, type_id=type_id, country=country)
        self.session.add(brand)
        self.session.commit()

    def user_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"user\""
                                    "select (SELECT MAX(id)+1 FROM public.\"user\"), "
                                    "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                                    "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), ''), "
                                    "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                                    "FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''); ")

    def basket_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"basket\" select (SELECT (MAX(id)+1) FROM public.\"basket\"), "
                                    "(SELECT id FROM public.\"device\" LIMIT 1 OFFSET (round(random() * "
                                    "((SELECT COUNT(id) FROM public.\"device\")-1)))),"
                                    "(SELECT id FROM public.\"user\" LIMIT 1 OFFSET "
                                    "(round(random() * ((SELECT COUNT(id) FROM public.\"user\")-1))));")

    def device_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"device\" select (SELECT MAX(id)+1 FROM public.\"device\"), "
                                    "FLOOR(RANDOM()*(100000-1)+1),"
                                    "(SELECT id FROM public.\"type\" LIMIT 1 OFFSET "
                                    "(round(random() *((SELECT COUNT(id) FROM public.\"type\")-1)))), "
                                    "(SELECT id FROM public.\"brand\" LIMIT 1 OFFSET "
                                    "(round(random() * ((SELECT COUNT(id) FROM public.\"brand\")-1)))),"
                                    "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                                    "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), '')  ;")

    def type_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"type\" select (SELECT MAX(id)+1 FROM public.\"type\"), "
                                    "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                                    "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), ''); ")

    def brand_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"brand\" select (SELECT MAX(id)+1 FROM public.\"brand\"), "
                                    "(SELECT id FROM public.\"type\" LIMIT 1 OFFSET "
                                    "(round(random() *((SELECT COUNT(id) FROM public.\"type\")-1)))), "
                                    "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer)\
                                     FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), ''),"
                                    "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                                    "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), ''); ")

    def search_data_two_tables(self):
        return self.session.query(User) \
            .join(Basket) \
            .filter(and_(
            User.id.between(0, 5),
            Basket.id.between(0, 5)
        )) \
            .all()

    def search_data_three_tables(self):
        return self.session.query(User) \
            .join(Basket).join(Device) \
            .filter(and_(
            User.id.between(0, 5),
            Basket.device_id.between(0, 5),
            Device.id.between(0, 5)
        )) \
            .all()

    def search_data_four_tables(self):
        return self.session.query(User) \
            .join(Basket).join(Device).join(Brand) \
            .filter(and_(
            User.id.between(0, 5),
            Basket.device_id.between(0, 5),
            Device.price.between(0, 2500),
            Brand.id.between(0, 5)
        )) \
            .all()
