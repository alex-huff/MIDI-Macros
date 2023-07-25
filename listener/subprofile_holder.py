from config.mm_config import MACROS
from log.mm_logging import logInfo


class SubprofileHolder:
    def __init__(self, profile, subprofiles):
        self.profile = profile
        self.subprofiles = subprofiles
        self.names = tuple(self.subprofiles.keys())
        self.numSubprofiles = len(self.names)
        assert self.numSubprofiles
        self.current = 0

    def cycle(self):
        if self.numSubprofiles == 1:
            return False
        if self.current == self.numSubprofiles - 1:
            self.current = 0
        else:
            self.current += 1
        return True

    def getCurrent(self):
        return self.names[self.current]

    def getCurrentMacroTree(self):
        return self.subprofiles[self.getCurrent()][MACROS]

    def setCurrent(self, subprofile):
        index = self.names.index(subprofile)
        if self.current == index:
            return False
        self.current = index
        return True

    def getNames(self):
        return self.names

    def getInfo(self):
        return {"current": self.getCurrent(), "all": self.names}

    def shutdown(self):
        for subprofile, subprofileConfig in self.subprofiles.items():
            logInfo('waiting for queued script invocations to complete', profile=self.profile, subprofile=subprofile)
            subprofileConfig[MACROS].shutdown()
