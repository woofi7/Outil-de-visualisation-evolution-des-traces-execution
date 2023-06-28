import re
from model.LogInstruction import LogInstruction
from model.Modification import Modification

class StrategyLog4j():
    instance = None
    
    # Singleton
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    # Function to get the logs specific to this framework
    def getLogs(self, hash, filename, beforeCode, afterCode, date, logs):
        print(f"HASH : {hash}")
        print(f"FILENAME : {filename}")
        hasFramework = False
        if logs is None:
            logs = []
        if beforeCode is None:
            beforeCode = ''
        if afterCode is None:
            afterCode = ''
        # Check for log4j import in the before and after code
        if "import " in beforeCode + afterCode and "log4j" in beforeCode + afterCode:
            hasFramework = True

        if hasFramework:
            logPattern = r'\.(debug|info|warn|error|fatal)\((.*?)\);'
            beforeMatches = re.findall(logPattern, beforeCode)
            afterMatches = re.findall(logPattern, afterCode)

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
                        self.addLogs(logs, beforeMatch[0] + beforeMatch[1],  afterMatch[0] + afterMatch[1], 'modified', date, beforeCode, afterCode, hash, filename)
                        afterMatches.remove(afterMatch)
                        beforeMatches.remove(beforeMatch)
                        break

            for beforeMatch in beforeMatches[:]:
                if len(beforeMatches) >= len(afterMatches):
                    self.addLogs(logs, beforeMatch[0] + beforeMatch[1], beforeMatch[0] + beforeMatch[1], 'deleted', date, beforeCode, afterCode, hash, filename)
                    beforeMatches.remove(beforeMatch)

            for afterMatch in afterMatches[:]:
                modification = Modification(afterMatch[0] + afterMatch[1], date, 'added', beforeCode, afterCode, hash, filename)
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
