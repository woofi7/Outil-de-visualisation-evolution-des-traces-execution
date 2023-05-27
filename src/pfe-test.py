import inspect

def get_functions(module):
    functions = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            functions.append(obj)
    return functions

# Exemple d'utilisation avec le module logging de Python
import org.apache.log4j as logging

logging_functions = get_functions(logging)
for function in logging_functions:
    print(function.__name__)
