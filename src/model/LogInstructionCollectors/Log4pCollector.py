from model.LogInstructionCollectors.LogInstructionCollector import LogInstructionCollector
import re
from pydriller import Repository
from pydriller import ModificationType
import traceback
import ast
from ast import Expr, While
from view.PopupView import PopupManager
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification
from datetime import datetime

FILE_TYPES = [".py"]

class Log4pCollector(LogInstructionCollector):
    def get_log_instructions(self, repo, from_date, to_date, path_in_directory, branch, author):
        try:
            if from_date != datetime.strptime(str(from_date), '%Y-%m-%d %H:%M:%S') or to_date != datetime.strptime(str(to_date), '%Y-%m-%d %H:%M:%S'):
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
            self.logs = {}
            self.commits = []
            # filter commits by repo, dates, file types and branch
            for commit in Repository(repo, since=from_date, to=to_date, only_modifications_with_file_types=FILE_TYPES, only_in_branch=branch).traverse_commits():
                # filter commits by authors
                if(commit.author is author or author == ''):
                    self.commits.append(commit)
                    for modified_file in commit.modified_files:
                        if modified_file.filename not in self.logs:
                            self.logs[modified_file.filename] = []
                        # filter files by file types and paths
                        if any(modified_file.filename.endswith(ext) for ext in FILE_TYPES) and ((modified_file.old_path is not None and path_in_directory in modified_file.old_path) or (modified_file.new_path is not None and path_in_directory in modified_file.new_path)):
                            # filter logs by framework
                            self.logs[modified_file.filename] = self.getLogs(commit.hash, modified_file.filename, modified_file.source_code_before, modified_file.source_code, commit.committer_date, self.logs[modified_file.filename], modified_file.change_type)
            return self.logs
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

       # Function to get the logs specific to this framework
    def getLogs(self, hash, filename, before_code, after_code, date, logs, type):
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
        if "import " in before_code + after_code and "log4p" in before_code + after_code:
            hasFramework = True
        
        if hasFramework:
            logPattern = ['debug','info','warn','error', 'fatal']
            beforeMatches = []
            afterMatches = []
            beforeParse = self.parse_python_code(before_code)
            afterParse = self.parse_python_code(after_code)
            i=0
            for node in beforeParse.body:
                if isinstance(node, Expr) and node.value.func.attr in logPattern:
                    beforeMatches.append(LogInstruction(node.value.func.attr, node.value.args[0].value, [], date, i))
                    i=i+1
                if isinstance(node, While):
                    for whileNode in node.body:
                        if isinstance(whileNode, Expr) and whileNode.value.func.attr in logPattern:
                            beforeMatches.append(LogInstruction(whileNode.value.func.attr, whileNode.value.args[0].value, [], date, i))
                            i=i+1

            i=0        
            for node in afterParse.body:
                if isinstance(node, Expr) and node.value.func.attr in logPattern:
                    afterMatches.append(LogInstruction(node.value.func.attr, node.value.args[0].value, [], date, i))
                    i=i+1
                if isinstance(node, While):
                    for whileNode in node.body:
                        if isinstance(whileNode, Expr) and whileNode.value.func.attr in logPattern:
                            afterMatches.append(LogInstruction(whileNode.value.func.attr, whileNode.value.args[0].value, [], date, i))
                            i=i+1
            print(len(afterMatches))
            if(type is ModificationType.ADD):
                for beforeMatch in beforeMatches:
                    for afterMatch in afterMatches:
                        if beforeMatch.level == afterMatch.level and beforeMatch.instruction == afterMatch.instruction:
                            afterMatches.remove(afterMatch)
                            beforeMatches.remove(beforeMatch)

                for newLog in afterMatches:
                    logs.insert(newLog.index, newLog)

            if(type is ModificationType.MODIFY):
                for index, beforeMatch in enumerate(beforeMatches):
                    if (beforeMatch.level == afterMatches[index].level and beforeMatch.instruction != afterMatches[index].instruction) or (beforeMatch.level != afterMatches[index].level and beforeMatch.instruction == afterMatches[index].instruction):
                        modification= Modification(date, type, beforeMatch, afterMatches[index], hash, filename)
                        logs[index].modifications.append(modification)
                        logs[index].level = afterMatches[index].level
                        logs[index].instruction = afterMatches[index].instruction
                        break
                if(type is ModificationType.DELETE):
                    for index, beforeMatch in enumerate(beforeMatches):
                        if (beforeMatch.level == afterMatches[index].level and beforeMatch.instruction != afterMatches[index].instruction) or (beforeMatch.level != afterMatches[index].level and beforeMatch.instruction == afterMatches[index].instruction):
                            logs.remove(index)
                            break
            return logs
            
            

            return logs
        
    def addLogs(self, logs, instruction, newInstruction, type, date, source_code_before, source_code, hash, filename):
        for log in logs:
            if log.instruction == instruction:
                modification = Modification(newInstruction, date, type, source_code_before, source_code, hash, filename)
                log.modifications.append(modification)
                log.instruction = newInstruction

    def parse_python_code(self, code):
        try:
            tree = ast.parse(code)
            return tree
        except Exception as e:
            print(e)
            return None
        
    