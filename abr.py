from pynput.keyboard import Key, Listener
from pyperclip import copy
import keyboard

abbrevFile = "abbreviations.txt"

class FastWriter():
    def __init__(self) -> None:
        self.abbreviations = {}
        try:
            self.fileOpen()
        except FileNotFoundError:
            print(f"Файл {abbrevFile} не найден.")
            self.createFile()
            self.fileOpen()
        self.keysListener()

    def createFile(self) -> None:
        with open(abbrevFile, 'w', encoding="utf8") as f:
            print(f"Файл {abbrevFile} создан, заполни его следуя шаблону:")
            print("\tсокращение_твой любой длинный текст.\n")
            f.write("прив_Привет, как дела?")

    def fileOpen(self) -> None:
        with open(abbrevFile, 'r', encoding="utf8") as f:
            print(f"Файл {abbrevFile} найден, текущие сокращения:\n")
            counter = 0
            for line in f.readlines():
                if line.strip():
                    counter += 1
                    line = (line.replace("\n", "")).split("_")
                    print(f"{counter}) {line[0]}_{line[1]}")
                    self.abbreviations[f"{line[0]}"] = f"{line[1]}"

    def onPress(self, key) -> None:
        key_str = str(key).replace('\'', '')

        if key_str == self.keyStart:
            self.typed_keys = []
            self.listening = True

        if self.listening:
            if key_str.isalpha():
                self.typed_keys.append(key_str)

            if key == self.keyEnd:
                keyWord = ""
                keyWord = keyWord.join(self.typed_keys)
                if keyWord != "":
                    if keyWord in self.abbreviations.keys():
                        backspaceCounter = 0
                        while backspaceCounter < (len(keyWord)+2):
                            keyboard.press_and_release("backspace")
                            backspaceCounter += 1
                        copy(self.abbreviations[keyWord])
                        keyboard.press_and_release('ctrl + v')
                        self.listening = False

    def keysListener(self) -> None:
        self.keyStart = '!'
        self.keyEnd = Key.space
        self.listening = True
        self.typed_keys = []
        with Listener(on_press=self.onPress) as listener:
            listener.join()

if __name__ == '__main__':
    print("ВНИМАНИЕ! Программа использует буффер обмена! При вводе сокращений, могут потеряться твои CTRL+C. Будь осторожнее.\n")
    FastWriter()