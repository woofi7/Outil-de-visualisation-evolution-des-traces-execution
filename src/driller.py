from pydriller import Repository

openstack = 'https://github.com/openstack/openstack'
devstack = 'https://github.com/openstack/devstack'
log4j = 'https://github.com/DIL8654/Log4J-example-with-java'

def printLogLines(modifiedFile):
    if ('.java' in modifiedFile.filename):
        print(modifiedFile.filename)
        if any(level in modifiedFile.source_code for level in ['.fatal', '.error', '.warn', '.info', '.debug', '.trace']):
            print(modifiedFile.methods)

for commit in Repository(devstack, only_in_branch='master').traverse_commits():
    for file in commit.modified_files:
        printLogLines(file)