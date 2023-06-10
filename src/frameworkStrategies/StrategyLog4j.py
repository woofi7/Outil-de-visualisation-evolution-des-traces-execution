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
    def getLogs(self, beforeCode, afterCode, date, logs):
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
                        self.addLogs(logs, beforeMatch[0] + beforeMatch[1],  afterMatch[0] + afterMatch[1], 'modified', date)
                        afterMatches.remove(afterMatch)
                        beforeMatches.remove(beforeMatch)
                        break

            for beforeMatch in beforeMatches[:]:
                if len(beforeMatches) >= len(afterMatches):
                    self.addLogs(logs, beforeMatch[0] + beforeMatch[1], beforeMatch[0] + beforeMatch[1], 'deleted', date)
                    beforeMatches.remove(beforeMatch)

            for afterMatch in afterMatches[:]:
                modification = Modification(afterMatch[0] + afterMatch[1], date, 'added')
                logInstruction = LogInstruction(afterMatch[0] + afterMatch[1], [modification], date)
                logs.append(logInstruction)
                afterMatches.remove(afterMatch)
            
            

            return logs
        
    def addLogs(logs, instruction, newInstruction, type, date):
        for log in logs:
            if log.instruction == instruction:
                modification = Modification(newInstruction, date, type)
                log.modifications.append(modification)
                log.instruction = newInstruction
