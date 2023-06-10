from frameworkStrategies.StrategyLog4j import StrategyLog4j
from frameworkStrategies.StrategyLog4p import StrategyLog4p

# Instruction set to define how to parse a repo's branch data
class Instructions:
    def __init__(self, path, dates=[], frameworks=[], fileTypes=[], authors=[]):
        self.dates = dates
        self.frameworks = []
        self.frameworkStrategies=[]
        for framework in frameworks:
            self.frameworkStrategies.append(self.getFrameworkStrategy(framework))
        self.fileTypes = fileTypes
        self.paths = path
        self.authors = authors

        
    # Get the adequate framework strategy
    def getFrameworkStrategy(self, framework):
        if(framework == "log4j"):
            return StrategyLog4j()
        elif(framework == "log4p"):
            return StrategyLog4p()