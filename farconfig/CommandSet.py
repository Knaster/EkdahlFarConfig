from commandparser import Derivedcommanditem, Derivedcommandlist
#from commanddefinitions import defaultCommandType, CommandID

class CommandSet:
#    commandID = None
#    indexingChild = None

    def __init__(self):
        self.CommandItem = Derivedcommanditem
        self.CommandList = Derivedcommandlist

        self.fromVer = 0
        self.toVer = 99999999999999

        #self.commandTypes = defaultCommandType

        #self.shortCommands: dict = {}
        #self.longCommands: dict = {}

        #self.shortID: dict = {}
        #self.longID: dict = {}

        self.commands = []

        self.loadingStage = 0
        self.ready = False

    def postInit(self):
        #self.shortID = {v: k for k, v in self.shortCommands.items()}
        #self.longID = {v: k for k, v in self.longCommands.items()}
        pass