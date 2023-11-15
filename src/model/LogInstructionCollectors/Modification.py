from dateutil.parser import parse

class Modification:
    def __init__(self, level, instruction, date, type, beforeCode, afterCode, hash, filename, summary, author, branch):
        self.level = level
        self.instruction = instruction
        self.date = date
        self.type = type
        self.beforeCode = beforeCode
        self.afterCode = afterCode
        self.hash = hash
        self.filename = filename
        self.summary = summary
        self.author = author
        self.branch = branch

    def get_commit_hash(self):
        return self.hash

    def get_date(self):
        return self.date

    def to_dict(self):
        return {
            'level': self.level,
            'instruction': self.instruction,
            'date': self.date.isoformat(),
            'type': self.type,
            'beforeCode': self.beforeCode,
            'afterCode': self.afterCode,
            'hash': self.hash,
            'filename': self.filename,
            'summary': self.summary,
            'author': self.author,
            'branch': self.branch
        }

    @staticmethod
    def from_dict(d):
        return Modification(d['level'], d['instruction'], parse(d['date']), d['type'], d['beforeCode'], d['afterCode'], d['hash'], d['filename'],d['summary'], d['author'], d['branch'])
