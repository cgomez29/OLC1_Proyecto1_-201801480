class AnalyzerRMT():
    __instance = None

    def __new__(self):
        if not self.__instance:
            self.__instance = super(AnalyzerRMT, self).__new__(self)
        return self.__instance


    def __init__(self):
        self.row = 0
        self.column = 0
        self.counter = 0 
        self.arrayError = []
        self.arrayToken = []

        self.signos = {"PARENTESISA": '(', "PARENTESISC": ')', "CORCHETEA": '[', "CORCHETEC": ']',
                        "SUMA": '+', "RESTA": '-', "MULTIPLICACION": '*', "DIVICION": '/'}


    def analizar(self, content):
        pass