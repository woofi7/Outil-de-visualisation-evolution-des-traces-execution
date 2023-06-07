from frameworkStrategies.StrategyLog4j import StrategyLog4j
from frameworkStrategies.StrategyLog4p import StrategyLog4p

# Instruction set to define how to parse a repo's branch data
class Instructions:
    def __init__(self, dates=[], frameworks=[], fileTypes=[], paths=[], authors=[]):
        self.dates = dates
        self.frameworks = []
        for framework in frameworks:
            self.frameworkStrategies.append(self.getFrameworkStrategy(framework))
        self.fileTypes = fileTypes
        self.paths = paths
        self.authors = authors
        
    # Get the adequate framework strategy
    def getFrameworkStrategy(framework):
        if(framework == "log4j"):
            return StrategyLog4j()
        elif(framework == "log4p"):
            return StrategyLog4p()