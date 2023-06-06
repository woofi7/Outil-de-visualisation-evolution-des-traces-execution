class Instructions:
    def __init__(self, dates=[], frameworks=[], fileTypes=[], paths=[], authors=[]):
        self.dates = dates
        self.frameworks = []
        for framework in frameworks:
            self.frameworks.append(...(framework))
        self.fileTypes = fileTypes
        self.paths = paths
        self.authors = authors