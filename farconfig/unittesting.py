import unittest

from commandparser import Derivedcommanditem
from CommandSets import CommandSetModular

outFile = None

class DummySerial():
    def write(self, data):
#        outFile.write(data + "\n")
        pass

dummySerial = DummySerial()

stageFiles = ["ver.txt", "help,nop.txt", "ls:m:r:i,nop.txt", "ls:c:r:i,nop.txt", "requestallresponse.txt"]

if __name__ == "__main__":
    commandSet = CommandSetModular()

    currentStage = 0

#    outFile = open("./testdata/requestallcommands.txt" , 'w', encoding="utf-8")

    for currentStage in range(0, len(stageFiles)):
        with open('./testdata/' + stageFiles[currentStage] , 'r', encoding="utf-8") as file:
            for line in file:
                line = line.rstrip("\n")
                commandItem = Derivedcommanditem(line)
                commandSet.processMessages(commandItem, commandSet, None, None, dummySerial)

        if (commandSet.loadingStage != (currentStage + 1)):
            pass

#    outFile.close()

    #unittest.main()