# This is the module file to write EC1000 xml files
from os.path import abspath
import numpy as np
import math

def fmt_crd(crd):
    return str(format(crd, '.6f'))


def write_jmp(file, crds):
    file.write('<JumpAbs>' + fmt_crd(crds[0]) + ', ' + fmt_crd(crds[1]) + '</JumpAbs>\n')


def write_mrk(file, crds):
    file.write('<MarkAbs>' + fmt_crd(crds[0]) + ', ' + fmt_crd(crds[1]) + '</MarkAbs>\n')


def write_pause(file, delay_in_seconds):
    # write_pause(file, delay_in_seconds):
    delay_in_microseconds = delay_in_seconds*10**6
    file.write("<LongDelay>{0:.0f}</LongDelay>\n".format(delay_in_microseconds))


def write_oct_rect_fill(file, pt1, pt2, hatch_spacing, scanDir='h'):
    """
    writeRectFill(file, pt1, pt2, delta, scanDir, circCntr = [0,0], R=0):
        args:
            file
            pt1
            pt2
            delta
            scanDir - "h" (x axis) or "v" (y axis) scan lines
            supports a cicular hole with last 2 arguments
    """
    f = file

    xCrd = [pt1[0], pt2[0]]
    yCrd = [pt1[1], pt2[1]]
    xCrd.sort()
    yCrd.sort()

    if scanDir == "h":
        for i, iterCrd in enumerate(np.arange(yCrd[1], yCrd[0], -hatch_spacing)):
            if i % 2 == 0:
                write_jmp(f, [xCrd[0], iterCrd])
                write_jmp(f, [xCrd[1], iterCrd])
            else:
                write_jmp(f, [xCrd[1], iterCrd])
                write_jmp(f, [xCrd[0], iterCrd])
    elif scanDir == "v":
        for i, iterCrd in enumerate(np.arange(xCrd[1], xCrd[0], -hatch_spacing)):
            if i % 2 == 0:
                write_jmp(f, [iterCrd, yCrd[1]])
                write_jmp(f, [iterCrd, yCrd[0]])
            else:
                write_jmp(f, [iterCrd, yCrd[0]])
                write_jmp(f, [iterCrd, yCrd[1]])


def write_oct_ec1000_file(filepath, x0, y0, w, h, start_delay=0.4, hs=0.2794, galvo_speed=1500):
    #  xo, yo are the top, left coordinates
    #  w, h are width and height(mm)
    #  hs = hatch spacing (mm)
    #  start_delay will wait a short time so the OCT has time to arm itself (s)
    #  galvo_speed is how fast the galvos move (mm/s)

    #open file
    fillFile = open(abspath(filepath), 'w')

    #set galvo speed and write initial delay
    # writeSpeed(fillFile, galvo_speed) #need to create this, and make sure it works

    #write the delay command
    write_pause(fillFile, start_delay)

    #write rectangle
    write_oct_rect_fill(fillFile, [x0, y0], [x0+w, y0-h], hs, 'h')

    #close file
    fillFile.close()

    return fillFile.name


def fmt_layer_file_name(layerNum):
    return str(layerNum).zfill(5)


def write_circ_fill(file, cntr, R, delta, scanDir):
    """
    def writeCircFill(file, cntr, R, space, delta, scanDir):
        args:
            file
            pt1 = [xCrd, yCrd]
            pt2 = [xCrd, yCrd]
    """
    circRight, circTop = np.add(cntr,R)
    circLeft, circBotm = np.add(cntr,-R)

    if scanDir == 'h':
        iterCrd = circTop
        while iterCrd >= circBotm:
            relIterCrdY = iterCrd - cntr[1]
            circSides = [cntr[0] - math.sqrt(R ** 2 - relIterCrdY ** 2), cntr[0] + math.sqrt(R ** 2 - relIterCrdY ** 2)]
            write_jmp(file, [circSides[1], iterCrd])
            write_mrk(file, [circSides[0], iterCrd])
            iterCrd = iterCrd - delta

    elif scanDir == 'v':
        iterCrd = circRight
        while iterCrd >= circLeft:
            relIterCrdX = iterCrd - cntr[0]
            circBotTop = [cntr[1] - math.sqrt(R ** 2 - relIterCrdX ** 2), cntr[1] + math.sqrt(R ** 2 - relIterCrdX ** 2)]
            write_jmp(file, [iterCrd, circBotTop[1]])
            write_mrk(file, [iterCrd, circBotTop[0]])
            iterCrd = iterCrd - delta


def write_circ_fill_squarely(file, cntr, R, space, delta, scanDir):
    """
    def writeCircFill(file, cntr, R, space, delta, scanDir):
        args:
            file
            pt1 = [xCrd, yCrd]
            pt2 = [xCrd, yCrd]
    """
    rectCrd1 = [cntr[0]-R-space, cntr[1]+R+space]
    rectCrd2 = [cntr[0]+R+space, cntr[1]-R-space]
    circRight, circTop = np.add(cntr,R)
    circLeft, circBotm = np.add(cntr,-R)
    xRect = [rectCrd1[0], rectCrd2[0]]
    yRect = [rectCrd1[1], rectCrd2[1]]
    xRect.sort()
    yRect.sort()

    if scanDir == 'h':
        iterCrd = yRect[1]
        while iterCrd >= yRect[0]:
            write_jmp(file, [xRect[0], iterCrd])
            if circBotm < iterCrd < circTop:
                relIterCrdY = iterCrd - cntr[1]
                markCrd = [cntr[0] - math.sqrt(R**2-relIterCrdY**2),cntr[0] + math.sqrt(R**2-relIterCrdY**2)]
                write_jmp(file, [markCrd[0], iterCrd])
                write_mrk(file, [markCrd[1], iterCrd])
            write_jmp(file, [xRect[1], iterCrd])
            iterCrd = iterCrd - delta

    elif scanDir == 'v':
        iterCrd = xRect[1]
        while iterCrd >= xRect[0]:
            write_jmp(file, [iterCrd, yRect[1]])
            if circLeft < iterCrd < circRight:
                relIterCrdX = iterCrd - cntr[0]
                markCrd = [cntr[1] - math.sqrt(R**2-relIterCrdX**2), cntr[1] + math.sqrt(R**2-relIterCrdX**2)]
                write_jmp(file, [iterCrd, markCrd[1]])
                write_mrk(file, [iterCrd, markCrd[0]])
            write_jmp(file, [iterCrd, yRect[0]])
            iterCrd = iterCrd - delta


def write_circ_outline(file, cntr, R, numSeg):
    write_jmp(file, [cntr[0], cntr[1]+R])
    for i in range(1, numSeg+1):
        theta = 2*math.pi*i/numSeg
        xCrd = R*math.sin(theta)+cntr[0]
        yCrd = R*math.cos(theta)+cntr[1]
        write_mrk(file, [xCrd, yCrd])

def write_comment(file, commentStr, long=0):
    xml_reserved_chars = set("<>&'%\"")
    if any((c in xml_reserved_chars) for c in commentStr):
        raise IOError('Comment String contains an xml_reserved character and may cause problems.')
    if long == 0:
        file.write("<!-- " + commentStr + " -->\n")
    else:
        file.write("<!-- __________" + commentStr + "__________ -->\n")


def write_ftr(file):
    # deprecated?
    footer = r"""<ApplicationEvent>100, 345</ApplicationEvent><EndJob></EndJob>
</Data>"""
    file.write(footer)
    
    
def write_hdr(file):
    # deprecated?
    header = r"""<Data type='JobData' rev='2.0'>
<BeginJob></BeginJob>
"""
    file.write(header)
    
def write_laser_power(file, percentPower, comment=1):
    laserPowerNum = 4*percentPower #Perform conversion to EC1000 power (400 = 100%)
    if comment == 1:
        file.write("<!-- Change Laser Power to "+str(int(laserPowerNum)/4)+"% -->\n")
    file.write("<Set id='LaserPulse'>1," + str(int(laserPowerNum)) + ",400</Set>\n")


def write_pulse(file, pulse_duration_in_seconds):
    #writePulse(file, percentPower, pulse_duration_in_seconds):
    pulse_duration_in_microseconds = pulse_duration_in_seconds*10**6
    file.write("<LaserFire>2,{0:.0f}</LaserFire>\n".format(pulse_duration_in_microseconds))


def write_rect_fill(file, pt1, pt2, hatch_spacing, scanDir, circCntr = [0, 0], R=0):
    """
    writeRectFill(file, pt1, pt2, delta, scanDir, circCntr = [0,0], R=0):
        args:
            file
            pt1
            pt2
            delta
            scanDir - "h" (x axis) or "v" (y axis) scan lines
            supports a cicular hole with last 2 arguments
    """
    f = file
    circRight, circTop = np.add(circCntr, R)
    circLeft, circBotm = np.add(circCntr, -R)

    xCrd = [pt1[0], pt2[0]]
    yCrd = [pt1[1], pt2[1]]
    xCrd.sort()
    yCrd.sort()

    if scanDir == "h":
        iterCrd = yCrd[1]
        while iterCrd >= yCrd[0]:
            write_jmp(f, [xCrd[0], iterCrd])
            if circBotm < iterCrd < circTop:
                relIterCrdY = iterCrd - circCntr[1]
                mrkCrd = [circCntr[0] - math.sqrt(R**2 - relIterCrdY**2), circCntr[0] + math.sqrt(R**2 - relIterCrdY**2)]
                write_mrk(f,[mrkCrd[0], iterCrd])
                write_jmp(f,[mrkCrd[1], iterCrd])
            write_mrk(f, [xCrd[1], iterCrd])
            iterCrd = iterCrd - hatch_spacing
    elif scanDir == "v":
        iterCrd = xCrd[1]
        while iterCrd >= xCrd[0]:
            write_jmp(f, [iterCrd, yCrd[1]])
            if circLeft < iterCrd < circRight:
                relIterCrdX = iterCrd - circCntr[0]
                mrkCrd = [circCntr[1] - math.sqrt(R**2 - relIterCrdX**2), circCntr[1] + math.sqrt(R**2 - relIterCrdX**2)]
                write_mrk(f, [iterCrd, mrkCrd[1]])
                write_jmp(f, [iterCrd, mrkCrd[0]])
            write_mrk(f, [iterCrd, yCrd[0]])
            iterCrd = iterCrd - hatch_spacing


def write_rect_outline(file, pt1, pt2):
    """
    def writeRectOL(file, pt1, pt2):
        args:
            file
            pt1 = [xCrd, yCrd]
            pt2 = [xCrd, yCrd]
    """
    xCrd = [pt1[0], pt2[0]]
    yCrd = [pt1[1], pt2[1]]
    xCrd.sort()
    yCrd.sort()

    write_jmp(file, [xCrd[0], yCrd[1]])
    write_mrk(file, [xCrd[0], yCrd[0]])
    write_mrk(file, [xCrd[1], yCrd[0]])
    write_mrk(file, [xCrd[1], yCrd[1]])
    write_mrk(file, [xCrd[0], yCrd[1]])

