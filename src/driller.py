import sys
from pydriller import Repository

openstack = 'https://github.com/openstack/openstack'
devstack = 'https://github.com/openstack/devstack'
log4j = 'https://github.com/DIL8654/Log4J-example-with-java'

# for commit in Repository(devstack, only_in_branch='master', only_modifications_with_file_types=['.java', '.py']).traverse_commits():
#     for file in commit.modified_files:
#         if('.java' in file.filename or '.py' in file.filename):
#             print(file.filename)
#             for line in file.diff_parsed["added", "deleted"]:
#                 if '.debug' in line.value or '.info' in line.value or '.error' in line.value or '.warning' in line.value:
#                     print(line.value)

for commit in Repository(devstack, only_in_branch='master', only_modifications_with_file_types=['.py']).traverse_commits():
    for file in commit.modified_files:
        if('.py' in file.filename):
            print(file.filename)