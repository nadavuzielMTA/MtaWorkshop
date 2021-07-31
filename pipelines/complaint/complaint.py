class Complaint:
    def __init__(self, mongo):
        self.mongo_complaints = mongo.complaint

    def get_complaint_by_id(self):
        self.mongo_complaints
