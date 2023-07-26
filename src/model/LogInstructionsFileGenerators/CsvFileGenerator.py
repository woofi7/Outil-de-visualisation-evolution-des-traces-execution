import csv

from model.LogInstructionsFileGenerators.LogInstructionsFileGenerator import LogInstructionsFileGenerator

class CsvFileGenerator(LogInstructionsFileGenerator):

    def __init__(self):
        # Initialisation de la classe
        super().__init__()
    
    def createFile(self, log_instructions):
        path = '../csv/data.csv'

        data = []
        index_map = {}

        for log in log_instructions:
            index_map[log.instruction] = len(index_map) + 1
                
            for modification in log.modifications:
                data.append({
                    'index': index_map[log.instruction],
                    'instruction': log.instruction,
                    'date': modification.date,
                    'type': modification.type
                })

        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['index', 'instruction', 'date', 'type'])
            for row in data:
                writer.writerow([row['index'], row['instruction'], row['date'], row['type']])

        return path