from model.LogInstructionCollectors.LogInstructionCollector import LogInstructionCollector
import javalang
from javalang.tree import MethodInvocation, BinaryOperation, Literal, MemberReference, ClassCreator, Cast
from pydriller import Repository
import traceback
from view.PopupView import PopupManager
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification

FILE_TYPES = {".java"}

class Log4jCollector(LogInstructionCollector):

    def get_log_instructions(self, repo, from_date, to_date, path_in_directory, branch, author):
        try:
            self.logs = {}
            # filter commits by repo, dates, file types and branch
            for commit in Repository(repo, since=from_date, to=to_date, only_modifications_with_file_types=FILE_TYPES, only_in_branch=branch).traverse_commits():
                # filter commits by authors
                if(commit.author is author or author == ''):
                    for modified_file in commit.modified_files:
                        # filter files by file types and paths
                        if modified_file.filename.endswith(tuple(FILE_TYPES)) and ((modified_file.old_path is not None and path_in_directory in modified_file.old_path) or (modified_file.new_path is not None and path_in_directory in modified_file.new_path)):
                            # filter logs by framework
                            if modified_file.filename not in self.logs:
                                self.logs[modified_file.filename] = []
                            modification = self.getLogs(commit.hash, modified_file.filename, modified_file.source_code_before, modified_file.source_code, commit.committer_date, self.logs[modified_file.filename], modified_file.change_type)
                            if len(modification) > 0:
                                self.logs[modified_file.filename] = modification
            return self.logs
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))
    
    def getLogs(self, hash, filename, before_code, after_code, date, logs, type):
        # print(f"HASH : {hash}")
        # print(f"FILENAME : {filename}")
        if before_code is None:
            before_code = ''
        if after_code is None:
            after_code = ''
        # Check for log4j import in the before and after code
        
        if ("import " in before_code or after_code) and "log4j" in (before_code + after_code):
         
            logPattern = {'debug','info','warn','error','fatal'}
            beforeMatches = []
            afterMatches = []
            try:
                beforeParse = self.parse_java_code(before_code)
                afterParse = self.parse_java_code(after_code)
             
                for _, node in beforeParse:
                    if isinstance(node, MethodInvocation) and node.member in logPattern:
                        beforeMatches.append(self.get_Log_Instruction(node, date, before_code, after_code, hash, filename, type))
                    
                for _, node in afterParse:
                    if isinstance(node, MethodInvocation) and node.member in logPattern:
                        afterMatches.append(self.get_Log_Instruction(node, date, before_code, after_code, hash, filename, type))
                    
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
                
                return afterMatches
            except Exception as e:
                traceback.print_exc()
        return logs

    def parse_java_code(self, code):
        return javalang.parse.parse(code)
    
    def get_Log_Instruction(self, node, date, before_code, after_code, hash, filename, type):
        instruction = self.get_instruction(node.arguments)
        modification = Modification(node.member, instruction, date, type, before_code, after_code, hash, filename)
        return LogInstruction(node.member, instruction, [modification], date)

    def get_instruction(self, arguments):
        final_argument = ''
        for argument in arguments:
          final_argument = final_argument + self.get_node_arguments(argument, '')
        return final_argument
    
    def get_node_arguments(self, node, final_argument):
        if isinstance(node, BinaryOperation):
            final_argument = final_argument + self.get_node_arguments(node.operandl, '') + node.operator + self.get_node_arguments(node.operandr, '')
        elif isinstance(node, MethodInvocation):
            final_argument = final_argument+ node.member + "(" + self.get_arguments(node.arguments) + ")"   
        elif isinstance(node, MemberReference):
            final_argument = final_argument + ", "+ node.member
        elif isinstance(node, Literal):
            final_argument = final_argument + node.value
        return final_argument

    def get_arguments(self, arguments):
        final_argument = ''
        for argument in arguments:
            if isinstance(argument, ClassCreator):
                for arg in argument.arguments:
                    final_argument = final_argument + self.get_node_arguments(arg, '')
            elif isinstance(argument, MemberReference):
                    final_argument = final_argument + self.get_node_arguments(argument, '')
            elif isinstance(argument, Cast):
                    final_argument = final_argument + self.get_arguments(argument.expression)
            else:
                final_argument = final_argument + " "+argument.value
        return final_argument