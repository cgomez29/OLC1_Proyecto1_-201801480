from colorama import Fore, Style

class Pila:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def inspeccionar(self):
        return self.items[len(self.items)-1]

    def tamano(self):
        return len(self.items)

    def printPila(self):
        print(Fore.MAGENTA + str(self.items) + Style.RESET_ALL)