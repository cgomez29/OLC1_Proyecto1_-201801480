class AnalyzerHTML():
    __instance = None

    def __new__(self):
        if not self.__instance:
            self.__instance = super(AnalyzerHTML, self).__new__(self)
        return self.__instance

    def __init__(self):
        self.row = 0
        self.column = 0
        self.counter = 0
        self.arrayErrores = []
        self.arrayTokens = []


    def analizar(self, content):
        self.arrayTokens = []
        self.arrayErrores = []
        self.row = 1
        self.column = 1
        self.counter = 0
        while self.counter < len(content):
            symbol = content[self.counter]