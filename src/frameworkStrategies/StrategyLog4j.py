import re

class StrategyLog4j():
    instance = None
    
    # Singleton
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    # Function to get the logs specific to this framework
    def getLogs(self, beforeCode, afterCode):
        hasFramework = False
        logs = {}
        deletedLogs = []
        untouchedLogs = []
        modifiedLogs = []
        addedLogs = []

        # Check for log4j import in the before and after code
        if "import " in beforeCode + afterCode and "log4j" in beforeCode + afterCode:
            hasFramework = True

        if hasFramework:
            logPattern = r'\.(debug|info|warn|error|fatal)\((.*?)\);'
            beforeMatches = re.findall(logPattern, beforeCode)
            afterMatches = re.findall(logPattern, afterCode)

            for beforeMatch in beforeMatches:
                for afterMatch in afterMatches:
                    if beforeMatch[0] == afterMatch[0] and beforeMatch[1] == afterMatch[1]:
                        untouchedLogs.append(beforeMatch[0] + beforeMatch[1])
                        afterMatches.remove(afterMatch)
                        beforeMatches.remove(beforeMatch)
                        break
                    
            for beforeMatch in beforeMatches:
                for afterMatch in afterMatches:
                    if (beforeMatch[0] == afterMatch[0] and beforeMatch[1] != afterMatch[1]) or (beforeMatch[0] != afterMatch[0] and beforeMatch[1] == afterMatch[1]):
                        modifiedLogs.append([beforeMatch[0] + beforeMatch[1], afterMatch[0] + afterMatch[1]])
                        afterMatches.remove(afterMatch)
                        beforeMatches.remove(beforeMatch)
                        break
                    
            for beforeMatch in beforeMatches:
                    if len(beforeMatches) > len(afterMatches):
                        deletedLogs.append(beforeMatch[0] + beforeMatch[1])
                        beforeMatches.remove(beforeMatch)
                        
            for afterMatch in afterMatches:
                    addedLogs.append(afterMatch[0] + afterMatch[1])
                    afterMatches.remove(afterMatch)

            logs["deletedLogs"] = deletedLogs
            logs["untouchedLogs"] = untouchedLogs
            logs["modifiedLogs"] = modifiedLogs
            logs["addedLogs"] = addedLogs

        return logs

# De chatgpt
    # def getLogs(self, beforeCode, afterCode):
    #     hasFramework = False
    #     logs = {}
    #     deletedLogs = []
    #     untouchedLogs = []
    #     modifiedLogs = []
    #     addedLogs = []

    #     # Check for log4j import in the before and after code
    #     if "import " in beforeCode + afterCode and "log4j" in beforeCode + afterCode:
    #         hasFramework = True

    #     if hasFramework:
    #         logPattern = r'\.(debug|info|warn|error|fatal)\((.*?)\);'
    #         beforeMatches = re.findall(logPattern, beforeCode)
    #         afterMatches = re.findall(logPattern, afterCode)

    #         for beforeMatch in beforeMatches:
    #             if beforeMatch in afterMatches:
    #                 untouchedLogs.append(beforeMatch[0] + beforeMatch[1])
    #                 afterMatches.remove(beforeMatch)
    #             else:
    #                 modifiedLogs.append([beforeMatch[0] + beforeMatch[1], None])

    #         for afterMatch in afterMatches:
    #             addedLogs.append(afterMatch[0] + afterMatch[1])

    #         logs["deletedLogs"] = deletedLogs
    #         logs["untouchedLogs"] = untouchedLogs
    #         logs["modifiedLogs"] = modifiedLogs
    #         logs["addedLogs"] = addedLogs

    #     return logs

    
    def getDeletedLogs(beforeMatches, afterMatches):
        
        return
    
    def getUntouchedLogs(beforeMatches, afterMatches):
        return
    
    def getModifiedLogs(beforeMatches, afterMatches):
        return
    
    def getAddedLogs(beforeMatches, afterMatches):
        return