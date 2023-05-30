class Modification:
    def __init__(self, commit_hash, date, type) :
        self.commit_hash = commit_hash
        self.date = date
        self.type = type
    
    def get_commit_hash(self):
        return self.commit_hash
    
    def get_date(self):
        return self.date