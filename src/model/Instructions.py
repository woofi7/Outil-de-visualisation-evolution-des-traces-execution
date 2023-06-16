from frameworkStrategies.StrategyLog4j import StrategyLog4j
from frameworkStrategies.StrategyLog4p import StrategyLog4p

# Instruction set to define how to parse a repo's branch data
class Instructions:
    def __init__(self, path, dates=[], frameworks=[], authors=[]):
        self.dates = dates
        self.frameworks = []
        self.frameworkStrategies=[]
        self.fileTypes = []
        print()
        for framework in frameworks:
            self.frameworkStrategies.append(self.getFrameworkStrategy(framework))
        self.paths = path
        self.authors = authors

        
    # Get the adequate framework strategy
    def getFrameworkStrategy(self, framework):
        if(framework == "log4j"):
            self.fileTypes=['.java']
            return StrategyLog4j()
        elif(framework == "log4p"):
            self.fileTypes=['.py']
            return StrategyLog4p()