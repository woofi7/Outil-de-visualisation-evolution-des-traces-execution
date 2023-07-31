import unittest
import json
import os
from unittest.mock import Mock
from model.LogInstructionsFileGenerators.JsonFileGenerator import JsonFileGenerator

class TestJsonFileGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = JsonFileGenerator()
        self.file_path = 'test.json'
        self.log_instructions = [Mock(), Mock()]  # Replace with actual instances if necessary

        for log in self.log_instructions:
            log.to_dict.return_value = {'data': 'test_data'}  # This is an example; replace with actual data if necessary

    def tearDown(self):
        # Clean up the created file after each test
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_createFile(self):
        # Call the method under test
        self.generator.createFile(self.log_instructions, self.file_path)

        # Assert the file has been created
        self.assertTrue(os.path.exists(self.file_path))

        # Assert the contents of the file are as expected
        with open(self.file_path, 'r') as f:
            data = json.load(f)

        expected_data = [{'data': 'test_data'}, {'data': 'test_data'}]
        self.assertEqual(data, expected_data)

if __name__ == '__main__':
    unittest.main()
