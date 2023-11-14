import csv

from model.LogInstructionsFileGenerators.LogInstructionsFileGenerator import LogInstructionsFileGenerator

class CsvFileGenerator(LogInstructionsFileGenerator):

    def __init__(self):
        # Initialisation de la classe
        super().__init__()
    
    def createFile(self, log_instructions):
        path = './files/graphData.csv'
        
        data = []
        index_map = {}

        for log in log_instructions:
            index =len(index_map) + 1
            index_map[index] = index
                
            for modification in log.modifications:
                data.append({
                    'index': index_map[index],
                    'instruction': log.instruction,
                    'date': modification.date,
                    'type': modification.type,
                    'author': modification.author
                })

        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['index', 'instruction', 'date', 'type', 'author'])
            for row in data:
                writer.writerow([row['index'], row['instruction'], row['date'], row['type'], row['author']])

        return path