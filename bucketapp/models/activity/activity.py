import uuid


class Activity(object):
    def __init__(self, name, bucketlist_id, description, date, status, id=None):
        self.name = name
        self.description = description
        self.bucketlist_id = bucketlist_id
        self.date = date
        self.status = status
        self.id = uuid.uuid4().hex if id is None else id
