from model.LogInstructionCollectors.LogInstructionCollector import LogInstructionCollector
import re
from pydriller import Repository
from pydriller import ModificationType
import traceback
import ast
import astor
from ast import Expr, While, FunctionDef, BinOp
from view.PopupView import PopupManager
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification
from datetime import datetime

FILE_TYPES = [".py"]

class Log4pCollector(LogInstructionCollector):
    def get_log_instructions(self, repo, from_date, to_date, path_in_directory, branch, author):
            self.logs = {}
            self.deletedlogs = []
            # filter commits by repo, dates, file types and branch
            for commit in Repository(repo, since=from_date, to=to_date, only_modifications_with_file_types=FILE_TYPES, only_in_branch=branch).traverse_commits():
                # filter commits by authors
                if(commit.author is author or author == ''):
                    for modified_file in commit.modified_files:
                        # filter files by file types and paths
                        if modified_file.filename.endswith(tuple(FILE_TYPES)) and ((modified_file.old_path is not None and path_in_directory in modified_file.old_path) or (modified_file.new_path is not None and path_in_directory in modified_file.new_path)):
                            # filter logs by framework
                            if modified_file.change_type == ModificationType.RENAME:
                                tmp = self.logs[modified_file.old_path]
                                self.logs[modified_file.new_path] = tmp
                                self.logs[modified_file.old_path] =[]
                            elif modified_file.change_type == ModificationType.DELETE:
                                self.logs[modified_file.old_path] = []
                            else:
                                if modified_file.new_path not in self.logs:
                                    self.logs[modified_file.new_path] = []
                                logs, deletedlogs = self.getLogs(commit.hash, modified_file.filename, modified_file.source_code_before, modified_file.source_code, commit.committer_date, self.logs[modified_file.new_path], modified_file.change_type)
                                if deletedlogs is not None:
                                    self.deletedlogs.append(deletedlogs)
                                self.logs[modified_file.new_path] = logs
                                
                            
            return self.logs, self.deletedlogs

       # Function to get the logs specific to this framework
    def getLogs(self, hash, filename, before_code, after_code, date, logs, type):
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
            self.get_log_instructions_by_commit(beforeParse, beforeMatches, date, before_code, after_code, hash, filename, type)
            self.get_log_instructions_by_commit(afterParse, afterMatches, date, before_code, after_code, hash, filename, type)

            
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
                            modification = Modification(afterMatch.level, afterMatch.instruction, date, type, before_code, after_code, hash, filename)
                            afterMatch.modifications = logs[index].modifications
                            afterMatch.modifications.append(modification)
                            logs.remove(logs[index])
                            beforeMatches.remove(beforeMatches[index])
                            break
            for log in logs:
                    modification = Modification(log.level, log.instruction, date, 'deleted', before_code, after_code, hash, filename)
                    log.modifications.append(modification)
            print(f"AFTER MATCHES : {afterParse}")
            return afterMatches, logs
            
        else:    
            for log in logs:
                    modification = Modification(log.level, log.instruction, date, 'deleted', before_code, after_code, hash, filename)
                    log.modifications.append(modification)
            return [], logs
        

    def parse_python_code(self, code):
            tree = ast.parse(code)
            return tree
        
    def get_log_instructions_by_commit(self,parseList, matcheslist, date, before_code, after_code, hash, filename, type):
        logPattern = ['debug','info','warn','error', 'fatal']
        if parseList is not None:
            
            for node in parseList.body:
                    if isinstance(node, Expr) and hasattr(node, 'value') and hasattr(node.value, 'func') and hasattr(node.value.func, 'attr') and node.value.func.attr in logPattern:
                        modification = Modification(node.value.func.attr, self.getArguments(node.value.args),date, type, before_code, after_code, hash, filename)
                        matcheslist.append(LogInstruction(node.value.func.attr, self.getArguments(node.value.args), [modification], date))
                    elif isinstance(node, FunctionDef):
                        self.get_log_instructions_by_commit(node, matcheslist, date, before_code, after_code, hash, filename, type)
                    elif isinstance(node, While):
                        self.get_log_instructions_by_commit(node, matcheslist, date, before_code, after_code, hash, filename, type)
    def getArguments(self, arg_list):
        arguments = ''
        for arg in arg_list:
             arguments = arguments+ astor.to_source(arg).strip()  
        return arguments

    