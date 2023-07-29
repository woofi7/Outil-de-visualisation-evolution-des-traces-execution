from model.LogInstructionCollectors.LogInstructionCollector import LogInstructionCollector
import javalang
from javalang.tree import MethodInvocation, BinaryOperation, Literal, MemberReference, ClassCreator, Cast
from pydriller import Repository, ModificationType
import traceback
from view.PopupView import PopupManager
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification

FILE_TYPES = {".java"}

class Log4jCollector(LogInstructionCollector):

    def get_log_instructions(self, repo, from_date, to_date, path_in_directory, branch, author):
            self.logs = {}
            self.deletedlogs = []
            repo_filter = Repository(repo, since=from_date, to=to_date, only_modifications_with_file_types=FILE_TYPES, only_in_branch=branch)
            file_types_set = set(FILE_TYPES)
            author_match = (lambda commit: commit.author == author) if author else (lambda _: True)
            # filter commits by repo, dates, file types and branch
            for commit in repo_filter.traverse_commits():
                # filter commits by authors
                if author_match(commit):
                    for modified_file in commit.modified_files:
                        print(f"FILE : {modified_file.filename}")
                        # filter files by file types and paths
                        if modified_file.filename.endswith(tuple(file_types_set)):
                            old_path_in_directory = modified_file.old_path and (path_in_directory in modified_file.old_path)
                            new_path_in_directory = modified_file.new_path and (path_in_directory in modified_file.new_path)
                            if old_path_in_directory or new_path_in_directory:
                            # filter logs by framework
                                if modified_file.change_type == ModificationType.RENAME and modified_file.old_path in self.logs:
                                    self.logs[modified_file.new_path] =  self.logs.get(modified_file.old_path)
                                    self.logs.pop(modified_file.old_path)
                                elif modified_file.change_type == ModificationType.DELETE and modified_file.old_path in self.logs:
                                    self.logs.pop(modified_file.old_path)
                                else:
                                    if modified_file.new_path not in self.logs:
                                        self.logs[modified_file.new_path] = []
                                    logs, deletedlogs = self.getLogs(commit.hash, modified_file.filename, modified_file.source_code_before, modified_file.source_code, commit.committer_date, self.logs.get(modified_file.new_path), modified_file.change_type)
                                    if deletedlogs is not None:
                                        self.deletedlogs.append(deletedlogs)
                                    self.logs[modified_file.new_path] = logs     
                                
                       
            return self.logs, self.deletedlogs
    
    def getLogs(self, hash, filename, before_code, after_code, date, logs, modification_type):
        if before_code is None:
            before_code = ''
        if after_code is None:
            after_code = ''
        # Check for log4j import in the after code
        if ("import " in after_code) and "log4j" in after_code:
            logPattern = {'debug', 'info', 'warn', 'error', 'fatal'}
            afterMatches = []
            afterParse = self.parse_java_code(after_code)

            for _, node in afterParse:
                if isinstance(node, MethodInvocation) and node.member in logPattern:
                    afterMatches.append(self.get_Log_Instruction(node, date, before_code, after_code, hash, filename, modification_type))

            logs_dict = {log.level + log.instruction: log for log in logs}
            for afterMatch in afterMatches:
                log_key = afterMatch.level + afterMatch.instruction
                if log_key in logs_dict:
                    log = logs_dict[log_key]
                    afterMatch.modifications = log.modifications
                    logs.remove(log)

            for afterMatch in afterMatches:
                log_key = afterMatch.level + afterMatch.instruction
                if log_key in logs_dict:
                    log = logs_dict[log_key]
                    if afterMatch.level != log.level or afterMatch.instruction != log.instruction:
                        modification = Modification(afterMatch.level, afterMatch.instruction, date, modification_type, before_code, after_code, hash, filename)
                        afterMatch.modifications = log.modifications
                        afterMatch.modifications.append(modification)
                        logs.remove(log)

            for log in logs:
                modification = Modification(log.level, log.instruction, date, 'ModificationType.DELETE', before_code, after_code, hash, filename, author)
                log.modifications.append(modification)

            return afterMatches, logs
        else:
            for log in logs:
                modification = Modification(log.level, log.instruction, date, 'ModificationType.DELETE', before_code, after_code, hash, filename)
                log.modifications.append(modification)
            return [], logs
      

    def parse_java_code(self, code):
        return javalang.parse.parse(code)
    
    def get_Log_Instruction(self, node, date, before_code, after_code, hash, filename, type, author):
        instruction = self.get_instruction(node.arguments)
        modification = Modification(node.member, instruction, date, type, before_code, after_code, hash, filename, author)
        return LogInstruction(node.member, instruction, [modification], date)

    def get_instruction(self, arguments):
        final_argument = ''
        for index, argument in enumerate(arguments):
          if index > 0:
              final_argument = final_argument + ', '
          final_argument = final_argument + self.get_node_arguments(argument, '')
        return final_argument
    
    def get_node_arguments(self, node, final_argument):

        if isinstance(node, BinaryOperation):
            final_argument = final_argument + self.get_node_arguments(node.operandl, '') + node.operator + self.get_node_arguments(node.operandr, '')
        elif isinstance(node, MethodInvocation):
            final_argument = final_argument+ node.member + "(" + self.get_instruction(node.arguments) + ")"   
        elif isinstance(node, MemberReference):
            final_argument = final_argument + node.member
        elif isinstance(node, Literal):
            final_argument = final_argument + node.value
        elif isinstance(node, ClassCreator):
                final_argument = final_argument + 'new ' + node.type.name+'(' + self.get_instruction(node.arguments)+')'
        elif isinstance(node, Cast):
                final_argument = final_argument + self.get_instruction(node.expression)
        return final_argument