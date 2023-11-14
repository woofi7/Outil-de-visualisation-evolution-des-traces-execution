from model.LogInstructionCollectors.LogInstructionCollector import LogInstructionCollector
from pydriller import Repository
from pydriller import ModificationType
from git import Repo, Diff
import git
import ast
import astor
from ast import Expr, While, FunctionDef
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification
from model.ReposManager import ReposManager

FILE_TYPES = [".py"]

class Log4pCollector(LogInstructionCollector):
    def get_log_instructions(self, repo_path, path_in_directory, branch, author):
        self.logs = {}
        self.deletedlogs = []

        repo, branch_ref = ReposManager.get_repo_branch(self, repo_path, branch)
        
        # Traverse the commits in the specified date range and branch
        for commit in repo.iter_commits(rev=branch_ref, reverse=True):
            # Filter commits by authors
            if author == '' or commit.author.name == author:
                # Get the parent commit to calculate diffs
                parent_commit = commit.parents[0] if commit.parents else None

                # Get the diffs for the commit
                if parent_commit:
                    diffs = parent_commit.diff(commit)
                else:
                    diffs = []
            

                # Filter diffs by file types and paths
                for diff in diffs:
                    if diff.change_type == 'R':  # Renamed file
                        if diff.a_path not in self.logs:
                            self.logs[diff.a_path] = []
                        tmp = self.logs[diff.a_path]
                        self.logs[diff.b_path] = tmp
                        self.logs[diff.a_path] = []
                    elif diff.change_type == 'D':  # Deleted file
                        self.logs[diff.a_path] = []
                    else:
                        if diff.b_path not in self.logs:
                            self.logs[diff.b_path] = []
                        before_code = self.getCode(diff.a_blob)
                        after_code = self.getCode(diff.b_blob)
                        logs, deletedlogs = self.getLogs(commit.hexsha, diff.b_path, before_code, after_code, commit.committed_datetime, self.logs[diff.b_path], diff.change_type, commit.author.name)
                        if deletedlogs is not None:
                            self.deletedlogs.append(deletedlogs)
                        self.logs[diff.b_path] = logs

        # Combine logs and deletedLogs
        logs = []
        for filePath in self.logs:
            fileLogs = self.logs[filePath]
            for log in fileLogs:
                logs.append(log)
        for deleted in self.deletedlogs:
            if deleted != []:
                for log in deleted:
                    logs.append(log)

        return logs

    def getCode(self, code):
        if code is None:
            return ''
        else:
            try:
                return code.data_stream.read().decode()
            except UnicodeDecodeError:
                return ''

       # Function to get the logs specific to this framework
    def getLogs(self, hash, filename, before_code, after_code, date, logs, type, author):
        # print(f"HASH : {hash}")
        # print(f"FILENAME : {filename}")
        if before_code is None:
            before_code = ''
        if after_code is None:
            after_code = ''
        
        if "import " in after_code and "log4p" in after_code:
            beforeMatches = []
            afterMatches = []
            beforeParse = self.parse_python_code(before_code)
            afterParse = self.parse_python_code(after_code)
            self.get_log_instructions_by_commit(beforeParse, beforeMatches, date, before_code, after_code, hash, filename, type, author)
            self.get_log_instructions_by_commit(afterParse, afterMatches, date, before_code, after_code, hash, filename, type, author)

            
            for afterMatch in afterMatches:
                    for index, beforMatch in enumerate (beforeMatches):
                        if (afterMatch.level == beforMatch.level and afterMatch.instruction == beforMatch.instruction) and len(logs) > 0:
                            afterMatch.modifications = logs[index].modifications
                            logs.remove(logs[index])
                            beforeMatches.remove(beforeMatches[index])
                            break
            
            for afterMatch in afterMatches:
                for index, beforMatch in enumerate (beforeMatches):
                        if ((afterMatch.level != beforMatch.level and afterMatch.instruction == beforMatch.instruction) or (afterMatch.level == beforMatch.level and afterMatch.instruction != beforMatch.instruction)) and len(logs) > 0:
                            modification = Modification(afterMatch.level, afterMatch.instruction, date, type, before_code, after_code, hash, filename, author)
                            afterMatch.modifications = logs[index].modifications
                            afterMatch.modifications.append(modification)
                            logs.remove(logs[index])
                            beforeMatches.remove(beforeMatches[index])
                            break
            for log in logs:
                    modification = Modification(log.level, log.instruction, date, 'deleted', before_code, after_code, hash, filename, author)
                    log.modifications.append(modification)
            print(f"AFTER MATCHES : {afterParse}")
            return afterMatches, logs
            
        else:    
            for log in logs:
                    modification = Modification(log.level, log.instruction, date, 'deleted', before_code, after_code, hash, filename, author)
                    log.modifications.append(modification)
            return [], logs
        

    def parse_python_code(self, code):
            tree = ast.parse(code)
            return tree
        
    def get_log_instructions_by_commit(self,parseList, matcheslist, date, before_code, after_code, hash, filename, type, author):
        logPattern = ['debug','info','warn','error', 'fatal']
        if parseList is not None:
            
            for node in parseList.body:
                    if isinstance(node, Expr) and hasattr(node, 'value') and hasattr(node.value, 'func') and hasattr(node.value.func, 'attr') and node.value.func.attr in logPattern:
                        modification = Modification(node.value.func.attr, self.getArguments(node.value.args),date, type, before_code, after_code, hash, filename, author)
                        matcheslist.append(LogInstruction(node.value.func.attr, self.getArguments(node.value.args), [modification], date))
                    elif isinstance(node, FunctionDef):
                        self.get_log_instructions_by_commit(node, matcheslist, date, before_code, after_code, hash, filename, type, author)
                    elif isinstance(node, While):
                        self.get_log_instructions_by_commit(node, matcheslist, date, before_code, after_code, hash, filename, type, author)
    def getArguments(self, arg_list):
        arguments = ''
        for arg in arg_list:
             arguments = arguments+ astor.to_source(arg).strip()  
        return arguments

    