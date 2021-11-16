import os

class CacheHelper:
    function_directory = ''
    cache = dict()
    cacheDisabled = False
    def __init__(self, function_directory):
        self.cacheDisabled = (os.environ.get("CacheEnabled") == "false")
        self.function_directory = function_directory

    def get_file(self, file):
        path = f"{self.function_directory}{file}"
        if self.cacheDisabled or path not in self.cache:
            with open(path, 'r') as f:
                self.cache[path] = f.read()
        return self.cache[path]
