class Bucketlist(object):
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.activities = {}