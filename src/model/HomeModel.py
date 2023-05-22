from pydriller import Repository
from PyQt6.QtCore import QDate, Qt
from datetime import datetime

SEARCHED_STRING = "LOG4J"

class HomeModel:
    def getCommits(self, repoUrl, from_date, to_date):
        result = []  # Initialize an empty list to store the result
        from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
        to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')
        dt1 = datetime(from_date_obj.year, from_date_obj.month, from_date_obj.day)
        dt2 = datetime(to_date_obj.year, to_date_obj.month, to_date_obj.day)
        for commit in Repository(repoUrl, since=dt1, to=dt2).traverse_commits():
            # Traverse through the commits in the repository
            for modification in commit.modified_files:
                # Iterate over the modified files in each commit
                if modification.source_code is not None:
                    # Check if the source code is available for the modified file
                    # if SEARCHED_STRING in modification.source_code:
                    # Uncomment the above line if you want to filter commits based on a specific string in the source code
                    result.append([commit.hash[:7], modification.filename, modification.added_lines, modification.deleted_lines])
                    # Append commit information to the result list
        return result  # Return the list of commits that match the criteria
