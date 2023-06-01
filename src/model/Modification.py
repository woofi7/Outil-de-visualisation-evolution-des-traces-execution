class Modification:
    def __init__(self, commit, date, type) :
        self.commit = commit
        self.date = date
        self.type = type
    
    def get_commit_hash(self):
        return self.commit
    
    def get_date(self):
        return self.date