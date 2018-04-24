from fmtCrd import fmtCrd
def writeMrk(file, crds):
    file.write('<MarkAbs>' + fmtCrd(crds[0]) + ', ' + fmtCrd(crds[1]) + '</MarkAbs>\n')