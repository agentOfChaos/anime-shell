import copy


class CommandFilter:

    specials = {"verbatim" : ["letteralmente"],
                "capital" : ["maiuscolo"],
                "back" : ["back"],
                "panic" : ["panico"],
                "ctrl" : ["control"]}

    terminators = ["esegui", "execute", "run", "engage", "engaged", "eseguì", "engagé"]

    def __init__(self, language, aliasfile="config/aliases.txt"):
        self.language = language
        self.aliasfile = aliasfile
        self.aliases = {}
        self.keyorder = []
        self.stack = []
        self.loadAliases()

    def wordsmatch(self, candidate, stone):
        if len(candidate) < len(stone):
            return False
        for step in range(len(stone)):
            if candidate[step] != stone[step]:
                return False
        return True

    def isSpecialKey(self, candidate):
        for k, v in self.specials.items():
            if candidate in v:
                return k
        return None

    def asciiControl(self, word):
        letter = word.lower()[0]
        if letter == "c":
            return chr(3)
        elif letter == "d":
            return chr(4)
        else:
            return chr(7)

    def parseWords(self, words):
        nomnom = copy.copy(words)
        output = ""
        while len(nomnom) > 0:
            found = False
            for key in self.keyorder:
                if len(nomnom) == 0:
                    return output.rstrip(), False
                if self.wordsmatch(nomnom, self.splitwords(key)):
                    for i in range(self.countwords(key)): nomnom.pop(0)
                    modifier = ""
                    if len(self.stack) > 0: modifier = self.stack.pop()
                    if modifier == "verbatim":
                        output += key + " "
                    elif modifier == "capital":
                        output += key.title() + " "
                    elif modifier == "ctrl":
                        output += self.asciiControl(key) + " "
                    elif modifier == "":
                        special = self.isSpecialKey(key)
                        if special is not None:
                            if special == "back":
                                output = output[:len(output) - 1]
                            elif special == "panic":
                                return "panic", True
                            else:
                                self.stack.append(special)
                        elif key in self.terminators:
                            return output, True
                        else:
                            output += self.aliases[key]
                    found = True
                    break
            if not found:
                modifier = ""
                if len(self.stack) > 0: modifier = self.stack.pop()
                if modifier == "capital":
                    output += nomnom.pop(0).title() + " "
                elif modifier == "ctrl":
                    output += self.asciiControl(nomnom.pop(0)) + " "
                elif modifier != "":
                    self.stack.append(modifier)
                else:
                    output += nomnom.pop(0) + " "

        return output.rstrip(), False

    def filter(self, text):
        return self.parseWords(text.lower().split(" "))

    def countwords(self, string):
        return len(string.split(" "))

    def splitwords(self, string):
        return string.split(" ")

    def loadAliases(self):
        try:
            afile = open(self.aliasfile, "r")
            lines = afile.read().split("\n")
            afile.close()
            for line in lines:
                if len(line.strip()) > 0:
                    key, val = line.split("=")
                    if key not in self.aliases.keys():
                        self.aliases[key] = val
                        self.keyorder.append(key)
            for k, v in self.specials.items():
                self.keyorder.extend(v)
            for t in self.terminators:
                self.keyorder.append(t)
            self.keyorder.sort(key=self.countwords, reverse=True)
        except IOError:
            print("no aliasfile")