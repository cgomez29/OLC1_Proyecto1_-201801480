

class Analyzer():

    __instance = None

    def __new__(self):
        if not self.__instance:
            self.__instance = super(Analyzer, self).__new__(self)
        return self.__instance

    def __init__(self):
        pass


    def analyzer_java(self, content):
        return content