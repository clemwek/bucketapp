import uuid


class Bucketlist(object):
    def __init__(self, name, user_id, id=None):
        self.name = name
        self.user_id = user_id
        self.id = uuid.uuid4().hex if id is None else id
        self.activities = {}
