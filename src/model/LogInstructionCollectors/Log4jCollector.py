from model.LogInstructionCollectors.LogInstructionCollector import LogInstructionCollector
import javalang
from javalang.tree import MethodInvocation, BinaryOperation, Literal, MemberReference, ClassCreator, Cast
from pydriller import Repository, ModificationType
import git
import os
from git import Repo, Diff
from datetime import datetime, timezone, timedelta
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification

FILE_TYPES = {".java"}

class Log4jCollector(LogInstructionCollector):

 

    def get_log_instructions(self, repo_path, from_date, to_date, path_in_directory, branch, author):
        self.logs = {}
        self.deletedlogs = []

        # Open the Git repository using GitPython
        repo = Repo(repo_path)

        # Get the specified branch
        branch_ref = repo.refs[branch]
        
        # Traverse the commits in the specified date range and branch
        for commit in repo.iter_commits(rev=branch_ref, since=from_date, until=to_date, reverse=True):
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

    def getLogs(self, hash, filename, before_code, after_code, date, logs, type, author):
        if before_code is None:
            before_code = ''
        if after_code is None:
            after_code = ''
        # Check for log4j import in the before and after code
        
        if ("import " in after_code) and "log4j" in  after_code:
            logPattern = {'debug','info','warn','error','fatal'}
            afterMatches = []
            afterParse = self.parse_java_code(after_code)
                    
            for _, node in afterParse:
                if isinstance(node, MethodInvocation) and node.member in logPattern:
                    afterMatches.append(self.get_Log_Instruction(node, date, before_code, after_code, hash, filename, type, author))
                
            for afterMatch in afterMatches:
                for index, log in enumerate (logs):
                    if (afterMatch.level == log.level and afterMatch.instruction == log.instruction) and len(logs) > 0:
                        afterMatch.modifications = logs[index].modifications
                        logs.remove(logs[index])
                        break
                    elif ((afterMatch.level != log.level and afterMatch.instruction == log.instruction) or (afterMatch.level == log.level and afterMatch.instruction != log.instruction)) and len(logs) > 0:
                        modification = Modification(afterMatch.level, afterMatch.instruction, date, 'ModificationType.MODIFY', before_code, after_code, hash, filename, author)
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
        try:
            return javalang.parse.parse(code)
        except javalang.parser.JavaSyntaxError:
            return []
    
    def get_Log_Instruction(self, node, date, before_code, after_code, hash, filename, type, author):
        instruction = self.get_instruction(node.arguments)
        modification = Modification(node.member, instruction, date, 'ModificationType.ADD', before_code, after_code, hash, filename, author)
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