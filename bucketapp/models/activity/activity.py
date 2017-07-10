class Activity(object):
    def __init__(self, name, bucketlist_id, description, date, status):
        self.name = name
        self.description = description
        self.bucketlist_id = bucketlist_id
        self.date = date
        self.status = status
