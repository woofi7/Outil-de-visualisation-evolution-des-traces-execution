from frameworkStrategies.Strategy import Strategy

class StrategyLog4j(Strategy):
    instance = None
    
    # Singleton
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    # Function to get the logs specific to this framework
    def getLogs(self):
        # TODO
        return