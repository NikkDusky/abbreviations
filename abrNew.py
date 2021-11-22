from pynput.keyboard import Listener
from pyperclip import copy
import keyboard

abbrevFile = "abbreviations.txt"
autocompleteKey = "Key.tab"
dotInsteadTwoSpaces = True
oneMoreBackspaceOnAutoComplete = True

class Writer():
    def __init__(self) -> None:
        self.text = ""
        self.nowListen = True
        self.keySpaceCount = 0
        self.abbreviations = {}
        try:
            self.fileOpen()
        except FileNotFoundError:
            print(f"Файл {abbrevFile} не найден.")
            self.createAbrFile()
            self.fileOpen()
        self.keyListen()

    def createAbrFile(self) -> None:
        with open(abbrevFile, 'w', encoding="utf8") as f:
            print(f"Файл {abbrevFile} создан, заполни его следуя шаблону:")
            print("\tсокращение_твой любой длинный текст.\n")
            f.write("прив_Привет, как дела?")

    def fileOpen(self) -> None:
        with open(abbrevFile, 'r', encoding="utf8") as f:
            print(f"Файл {abbrevFile} найден, текущие сокращения:\n")
            _ = 0
            for line in f.readlines():
                if line.strip():
                    _ += 1
                    line = (line.replace("\n", "")).split("_")
                    print(f"{_}) {line[0]}_{line[1]}")
                    self.abbreviations[f"{line[0]}"] = f"{line[1]}"

    def backspacePresser(self) -> None:
        if oneMoreBackspaceOnAutoComplete:
            backspacesCount = len(self.text) + 1
        else:
            backspacesCount = len(self.text)
        for _ in range(backspacesCount):
            keyboard.press_and_release("backspace")

    def checkSpaces(self) -> None:
        self.keySpaceCount += 1
        if self.keySpaceCount == 2:
            keyboard.press_and_release("backspace")
            keyboard.press_and_release("backspace")
            copy(".")
            keyboard.press_and_release("ctrl+v")
            self.keySpaceCount = 0

    def checkReplace(self, checkedText: str) -> None:
        if checkedText in self.abbreviations.keys():
            self.backspacePresser()
            stringToPaste = self.abbreviations[self.text]
            copy(stringToPaste.rstrip())
            keyboard.press_and_release('ctrl+v')

    def onPress(self, key) -> None:
        strKey = str(key).replace("'", "")
        if not strKey.startswith("Key.") and self.nowListen:
            self.text += strKey
            self.keySpaceCount = 0

        if strKey == "Key.backspace":
            self.nowListen = True
            self.text = self.text[:-1]

        elif strKey == "Key.space":
            self.nowListen = True
            self.text = ""
            if dotInsteadTwoSpaces:
                self.checkSpaces()

        elif strKey == autocompleteKey:
            self.nowListen = False
            self.checkReplace(self.text)
            self.text = ""

    def keyListen(self) -> None:
        with Listener(on_press=self.onPress) as listen:
            listen.join()

if __name__ == '__main__':
    print("Программа использует буфер обмена для вставки, используй с осторожностью.\n")
    Writer()