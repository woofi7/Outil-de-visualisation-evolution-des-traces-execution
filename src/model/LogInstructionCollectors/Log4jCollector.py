from model.LogInstructionCollectors.LogInstructionCollector import LogInstructionCollector
import javalang
from javalang.tree import MethodInvocation, BinaryOperation, Literal, MemberReference, ClassCreator, Cast
from pydriller import Repository, ModificationType
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification

FILE_TYPES = {".java"}

class Log4jCollector(LogInstructionCollector):

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
                                if modified_file.old_path not in self.logs:
                                    self.logs[modified_file.old_path] = []
                                tmp = self.logs[modified_file.old_path]
                                self.logs[modified_file.new_path] = tmp
                                self.logs[modified_file.old_path] =[]
                            elif modified_file.change_type == ModificationType.DELETE:
                                self.logs[modified_file.old_path] = []
                            else:
                                if modified_file.new_path not in self.logs:
                                    self.logs[modified_file.new_path] = []
                                logs, deletedlogs = self.getLogs(commit.hash, modified_file.filename, modified_file.source_code_before, modified_file.source_code, commit.committer_date, self.logs[modified_file.new_path], modified_file.change_type, commit.author.name)
                                if deletedlogs is not None:
                                    self.deletedlogs.append(deletedlogs)
                                self.logs[modified_file.new_path] = logs
                        
            # Combine logs and deletedLogs
            logs = []
            for filePath in self.logs:
                fileLogs = self.logs[filePath]
                for log in fileLogs:
                    logs.append(log)
            for deleted in self.deletedlogs:
                if deleted is not []:
                    for log in deleted:
                        logs.append(log)
            
            # Add modifications from deletedLogs duplicates to logs 
            i = 0
            j = 0
            iToDelete = []
            jToDelete = []
            for i in range(len(logs)):
                for j in range(len(logs)):
                    if i == j:
                        break
                    if logs[i].instruction == logs[j].instruction and logs[i].level == logs[j].level:
                        if logs[j].modifications[0].type == 'ModificationType.DELETE':
                            logs[i].modifications.extend(logs[j].modifications)
                            jToDelete.append(j)
                        else:
                            logs[j].modifications.extend(logs[i].modifications)
                            iToDelete.append(i)
            # Clean logs that are duplications
            for i in iToDelete:
                del logs[i]
            for j in jToDelete:
                del logs[j]
                                
                            
            return logs
    
    def getLogs(self, hash, filename, before_code, after_code, date, logs, type, author):
        # print(f"HASH : {hash}")
        # print(f"FILENAME : {filename}")
        if before_code is None:
            before_code = ''
        if after_code is None:
            after_code = ''
        # Check for log4j import in the before and after code
        
        if ("import " in after_code) and "log4j" in  after_code:
            logPattern = {'debug','info','warn','error','fatal'}
            beforeMatches = []
            afterMatches = []
            #beforeParse = self.parse_java_code(before_code)
            afterParse = self.parse_java_code(after_code)
            #for _, node in beforeParse:
            #    if isinstance(node, MethodInvocation) and node.member in logPattern:
            #        beforeMatches.append(self.get_Log_Instruction(node, date, before_code, after_code, hash, filename, type))
                    
            for _, node in afterParse:
                if isinstance(node, MethodInvocation) and node.member in logPattern:
                    afterMatches.append(self.get_Log_Instruction(node, date, before_code, after_code, hash, filename, type, author))
                
            #if(len(beforeMatches) != len(logs)):
            #    return afterMatches, logs
                
            for afterMatch in afterMatches:
                for index, log in enumerate (logs):
                    if (afterMatch.level == log.level and afterMatch.instruction == log.instruction) and len(logs) > 0:
                        afterMatch.modifications = logs[index].modifications
                        logs.remove(logs[index])
                        break
            for afterMatch in afterMatches:
                for index, log in enumerate (logs):
                    if ((afterMatch.level != log.level and afterMatch.instruction == log.instruction) or (afterMatch.level == log.level and afterMatch.instruction != log.instruction)) and len(logs) > 0:
                        modification = Modification(afterMatch.level, afterMatch.instruction, date, type, before_code, after_code, hash, filename, author)
                        afterMatch.modifications = logs[index].modifications
                        afterMatch.modifications.append(modification)
                        logs.remove(logs[index])
                        break

            for log in logs:
                modification = Modification(log.level, log.instruction, date, 'ModificationType.DELETE', before_code, after_code, hash, filename, author)
                log.modifications.append(modification)

            return afterMatches, logs
        else:
            for log in logs:
                    modification = Modification(log.level, log.instruction, date, 'ModificationType.DELETE', before_code, after_code, hash, filename, author)
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