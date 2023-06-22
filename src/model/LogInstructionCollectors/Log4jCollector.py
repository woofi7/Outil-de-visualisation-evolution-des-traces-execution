from model.LogInstructionCollectors.LogInstructionCollector import LogInstructionCollector
import re
from pydriller import Repository
import traceback
from view.PopupView import PopupManager
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification
from datetime import datetime

FILE_TYPES = [".java"]

class Log4jCollector(LogInstructionCollector):
    def get_log_instructions(self, repo, from_date, to_date, path_in_directory, branch, author):
        try:
            if from_date != datetime.strptime(str(from_date), '%Y-%m-%d %H:%M:%S') or to_date != datetime.strptime(str(to_date), '%Y-%m-%d %H:%M:%S'):
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
            self.logs = {}
            # filter commits by repo, dates, file types and branch
            for commit in Repository(repo, since=from_date, to=to_date, only_modifications_with_file_types=FILE_TYPES, only_in_branch=branch).traverse_commits():
                # filter commits by authors
                if(commit.author is author or author is None):
                    self.commits.append(commit)
                    for modified_file in commit.modified_files:
                        self.logs[modified_file.filename] = []
                        # filter files by file types and paths
                        if any(modified_file.filename.endswith(ext) for ext in FILE_TYPES) and ((modified_file.old_path is not None and path_in_directory in modified_file.old_path) or (modified_file.new_path is not None and path_in_directory in modified_file.new_path)):
                            # filter logs by framework
                                self.logs[modified_file.filename] = self.getLogs(commit.hash, modified_file.filename, modified_file.source_code_before, modified_file.source_code, commit.committer_date, self.logs[modified_file.filename])
            return self.logs
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))
    
    def getLogs(self, hash, filename, before_code, after_code, date, logs):
        # print(f"HASH : {hash}")
        # print(f"FILENAME : {filename}")
        hasFramework = False
        if logs is None:
            logs = []
        if before_code is None:
            before_code = ''
        if after_code is None:
            after_code = ''
        # Check for log4j import in the before and after code
        if "import " in before_code + after_code and "log4j" in before_code + after_code:
            hasFramework = True

        if hasFramework:
            logPattern = r'\.(debug|info|warn|error|fatal)\((.*?)\);'
            beforeMatches = re.findall(logPattern, before_code)
            afterMatches = re.findall(logPattern, after_code)

            # Iterate over a copy of beforeMatches to avoid deleting items while iterating
            for beforeMatch in beforeMatches[:]:
                for afterMatch in afterMatches[:]:
                    if beforeMatch[0] == afterMatch[0] and beforeMatch[1] == afterMatch[1]:
                        afterMatches.remove(afterMatch)
                        beforeMatches.remove(beforeMatch)
                        break

            for beforeMatch in beforeMatches[:]:
                for afterMatch in afterMatches[:]:
                    if (beforeMatch[0] == afterMatch[0] and beforeMatch[1] != afterMatch[1]) or (beforeMatch[0] != afterMatch[0] and beforeMatch[1] == afterMatch[1]):
                        self.addLogs(logs, beforeMatch[0] + beforeMatch[1],  afterMatch[0] + afterMatch[1], 'modified', date, before_code, after_code, hash, filename)
                        afterMatches.remove(afterMatch)
                        beforeMatches.remove(beforeMatch)
                        break

            for beforeMatch in beforeMatches[:]:
                if len(beforeMatches) >= len(afterMatches):
                    self.addLogs(logs, beforeMatch[0] + beforeMatch[1], beforeMatch[0] + beforeMatch[1], 'deleted', date, before_code, after_code, hash, filename)
                    beforeMatches.remove(beforeMatch)

            for afterMatch in afterMatches[:]:
                modification = Modification(afterMatch[0] + afterMatch[1], date, 'added', before_code, after_code, hash, filename)
                logInstruction = LogInstruction(afterMatch[0] + afterMatch[1], [modification], date)
                logs.append(logInstruction)
                afterMatches.remove(afterMatch)
            return logs
        
    def addLogs(self, logs, instruction, newInstruction, type, date, source_code_before, source_code, hash, filename):
        for log in logs:
            if log.instruction == instruction:
                modification = Modification(newInstruction, date, type, source_code_before, source_code, hash, filename)
                log.modifications.append(modification)
                log.instruction = newInstruction