import csv

from model.LogInstructionsFileGenerators.LogInstructionsFileGenerator import LogInstructionsFileGenerator

class CsvFileGenerator(LogInstructionsFileGenerator):

    def __init__(self):
        # Initialisation de la classe
        super().__init__()
    
    # TODO
    def createFile(self, log_instructions):
        path = '../csv/data.csv'
        
        datesByIndex = {}
        i = 0
        
        for filePath in log_instructions:
            fileLogs = log_instructions[filePath]
            for log in fileLogs:
                i += 1
                datesByIndex[i] = []
                for modifiction in log.modifications:
                    datesByIndex[i].append(modifiction.date)
        
        # datesByIndex = {1: ["2021-01-01", "2022-03-16", "2022-05-29", "2022-06-26"], 
        #          2: ["2021-02-01", "2022-07-27", "2022-05-29"],
        #          3: ["2021-03-01", "2022-07-01", "2022-07-22", "2022-08-09"], 
        #          4: ["2022-09-15"]}

        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Index', 'Date'])
            for index, date_list in datesByIndex.items():
                for date in date_list:
                    writer.writerow([index, date])
                    
        return path