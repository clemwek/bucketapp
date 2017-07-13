import uuid


class User(object):
    def __init__(self, name, email, password, id=None):
        self.id = uuid.uuid4().hex if id is None else id
        self.name = name
        self.email = email
        self.password = password
