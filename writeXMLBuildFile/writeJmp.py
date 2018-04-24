from fmtCrd import *
def writeJmp(file, crds):
    file.write('<JumpAbs>' + fmtCrd(crds[0]) + ', ' + fmtCrd(crds[1]) + '</JumpAbs>\n')