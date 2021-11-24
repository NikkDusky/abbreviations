import configparser
from os import path
from sys import stdout

import keyboard
from loguru import logger
from pyperclip import copy
from pynput.keyboard import Listener

abbrevFile = "abbreviations.txt"

config = {
    "handlers": [
        {"sink": stdout, "format": "[<light-cyan>{time:YYYY-MM-DD HH:mm:ss}</light-cyan>] [<level>{level}</level>] <level>{message}</level>"},
        {"sink": "debug.log", "diagnose": True, "compression": "zip", "encoding": "utf8", "rotation": "10 MB", "format": "[<cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan>] [<level>{level}</level>] {message}"},
                ]
        }

logger.configure(**config)

@logger.catch()
class Writer():
    def __init__(self) -> None:
        self.text = ""
        self.nowListen = False
        self.keySpaceCount = 0
        self.abbreviations = {}
        self.cfg = "abrSettings.ini"
        self.config = configparser.ConfigParser()
        self.checkConfig()

        try:
            self.fileOpen()
        except FileNotFoundError:
            print(f"Файл {abbrevFile} не найден.")
            self.createAbrFile()
            self.fileOpen()
        self.keyListen()

    def checkConfig(self) -> None:
        if not path.isfile(self.cfg):
            self.createConfig()
            self.getConfig()
        else:
            self.getConfig()

    def createConfig(self, START_KEY="!", MORE_BACKSPACES_ON_AUTOCOMPLETE=1, HOW_MORE_BACKSPACES=2) -> None:
        self.config.add_section("settings")
        self.config.set("settings", "START_KEY", f"{START_KEY}")
        self.config.set("settings", "MORE_BACKSPACES_ON_AUTOCOMPLETE", f"{MORE_BACKSPACES_ON_AUTOCOMPLETE}")
        self.config.set("settings", "HOW_MORE_BACKSPACES", f"{HOW_MORE_BACKSPACES}")

        with open(self.cfg, "w") as config_file:
            self.config.write(config_file)
        print("Файл с настройками создан.")

    def getConfig(self) -> None:
        self.config.read(self.cfg)
        self.START_KEY = self.config.get("settings", "START_KEY")
        self.MORE_BACKSPACES_ON_AUTOCOMPLETE = int(self.config.get("settings", "MORE_BACKSPACES_ON_AUTOCOMPLETE"))
        self.HOW_MORE_BACKSPACES = int(self.config.get("settings", "HOW_MORE_BACKSPACES"))
        print("Настройки из файла получены.")

    def createAbrFile(self) -> None:
        with open(abbrevFile, 'w', encoding="utf8") as f:
            print(f"Файл {abbrevFile} создан.")
            print("\nЗаполни файл следуюя шаблону:\n")
            print("\tсокращение_твой любой длинный текст.\n")
            f.write("прив_Привет, как дела? ")

    def fileOpen(self) -> None:
        with open(abbrevFile, 'r', encoding="utf8") as f:
            print(f"Файл {abbrevFile} найден.")
            print("\nТекущие скоращения:\n")
            _ = 0
            for line in f.readlines():
                if line.strip():
                    _ += 1
                    line = (line.replace("\n", "")).split("_")
                    print(f"\t{_}) {line[0]}_{line[1]}")
                    self.abbreviations[f"{line[0]}"] = f"{line[1]}"

    def backspacePresser(self) -> None:
        if self.MORE_BACKSPACES_ON_AUTOCOMPLETE:
            backspacesCount = len(self.text) + self.HOW_MORE_BACKSPACES
        else:
            backspacesCount = len(self.text)
        for _ in range(backspacesCount):
            keyboard.press_and_release("backspace")

    def checkReplace(self, checkedText: str) -> None:
        if checkedText in self.abbreviations.keys():
            self.backspacePresser()
            stringToPaste = self.abbreviations[self.text]
            copy(stringToPaste)
            keyboard.press_and_release('ctrl+v')
            self.keySpaceCount = 0

    def onPress(self, key) -> None:
        strKey = str(key).replace("'", "")
        if not strKey.startswith("Key.") and self.nowListen:
            self.text += strKey

        if strKey == self.START_KEY:
            self.nowListen = True
            self.text = ""

        elif strKey == "Key.space":
            self.nowListen = False
            self.checkReplace(self.text)
            self.text = ""

        elif strKey == "Key.backspace":
            self.text = self.text[:-1]

    def keyListen(self) -> None:
        with Listener(on_press=self.onPress) as listen:
            listen.join()

if __name__ == '__main__':
    Writer()