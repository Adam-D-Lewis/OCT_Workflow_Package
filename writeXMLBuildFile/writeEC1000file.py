# This is the module file to write EC1000 xml files
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import time
from os.path import abspath
import numpy as np
import math
from scipy.optimize import minimize
import xml.etree.ElementTree as ET
from os import path
import numpy as np
from Pipe_And_Filter_Autosection.classes.OCTEC1000 import OCTEC1000 as oct_ec

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


def write_circ_fill_squarely(file, cntr, R, space, delta=.2794, scanDir='h'):
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
        file.write("<!-- Change Laser Power to "+str(int(laserPowerNum)/4)+" percent -->\n")
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

def write_rotating_square(file, angle_deg, pt1, pt2, hs=0.2794):
    if angle_deg < 0:
        raise("angle out of bounds")
    angle_deg = angle_deg % 360
    angle_rad = angle_deg*math.pi/180
    x_bnds = sorted([pt1[0], pt2[0]])
    y_bnds = sorted([pt1[1], pt2[1]])
    bottom = y_bnds[0]
    top = y_bnds[1]
    left = x_bnds[0]
    right = x_bnds[1]

    m = angle_to_slope(angle_deg) #slope

    if 90 < angle_deg <= 180:
        #start at top, left
        offset = abs(hs/math.cos(angle_rad)/2)
        b1 = return_b_from_point_slope(left, top-offset, m)
        b2 = b1
        i = 0
        while True:
            i += 1
            b_old = b2
            if angle_deg == 90:
                b2 = b2-hs*abs(1/math.sin(angle_rad))
            else:
                b2 = b2-hs*abs(1/math.cos(angle_rad))
            if square_line_intersection(bottom, left, right, top, m, b2) == []:
                break
        b2 = b_old

        # diff = b2 - b1
        # ans = minimize(obj_func, 0.01*b1, args=(m, diff, left, top, right, bottom))
        # b1 = ans.x[0]/0.01
        # b2 = b1 + diff

        # now I have b1, b2, and m
        # b_vals = np.arange(b1, b2 - m * hs / 2, -m * hs)
        b_vals = np.linspace(b1, b2, i)
        intersecting_points = [square_line_intersection(bottom, left, right, top, m, b) for b in b_vals]
        [pair.sort(key=lambda pair: pair[0]) for pair in intersecting_points]
    elif 180 < angle_deg <= 270:
        #start at top, right
        offset = abs(hs/math.sin(angle_rad)/2)
        if m == math.inf:
            #now b1 is the x value
            b1 = right-hs/2
        else:
            b1 = return_b_from_point_slope(right - offset, top, m)
        b2 = b1
        i = 0
        while True:
            i += 1
            b_old = b2
            if angle_deg == 270:
                b2 = b2-hs*abs(1/math.sin(angle_rad))
            else:
                b2 = b2-hs*abs(1/math.cos(angle_rad))
            if square_line_intersection(bottom, left, right, top, m, b2) == []:
                break
        b2 = b_old

        # now I have b1, b2, and m
        b_vals = np.linspace(b1, b2, i)
        intersecting_points = [square_line_intersection(bottom, left, right, top, m, b) for b in b_vals]
        [pair.sort(key=lambda pair: pair[1], reverse=True) for pair in intersecting_points]
    elif 270 < angle_deg < 360 or angle_deg == 0:
        #start at bottom, right
        # offset = abs(hs/math.sin(angle_rad)/2)
        offset = abs(hs/math.cos(angle_rad)/2)
        b1 = return_b_from_point_slope(right, bottom+offset, m)
        b2 = b1
        i = 0
        while True:
            i += 1
            b_old = b2
            b2 = b2+hs*abs(1/math.cos(angle_rad))
            if square_line_intersection(bottom, left, right, top, m, b2) == []:
                break
        b2 = b_old

        # now I have b1, b2, and m
        b_vals = np.linspace(b1, b2, i)
        intersecting_points = [square_line_intersection(bottom, left, right, top, m, b) for b in b_vals]
        [pair.sort(key=lambda pair: pair[0], reverse=True) for pair in intersecting_points]
    elif 0 < angle_deg <= 90:
        #start at bottom, left
        offset = abs(hs/math.sin(angle_rad)/2)
        if m == math.inf:
            #now b1 is the x value
            b1 = left+hs/2
        else:
            b1 = return_b_from_point_slope(left+offset, bottom, m)
        b2 = b1
        i = 0
        while True:
            i += 1
            b_old = b2
            if angle_deg == 90:
                b2 = b2+hs*abs(1/math.sin(angle_rad))
            else:
                b2 = b2+hs*abs(1/math.cos(angle_rad))
            if square_line_intersection(bottom, left, right, top, m, b2) == []:
                break
        b2 = b_old

        # now I have b1, b2, and m
        b_vals = np.linspace(b1, b2, i)
        intersecting_points = [square_line_intersection(bottom, left, right, top, m, b) for b in b_vals]
        [pair.sort(key=lambda pair: pair[0], reverse=True) for pair in intersecting_points]
    else:
        raise("angle_out of bounds")

    for i, b in enumerate(b_vals[:-1]):
        thing = dist_of_parallel_lines(m, b_vals[i], b_vals[i + 1])
        if not (hs - 1E-6 < thing < hs + 1E-6):
            print(thing)
            raise ("error in hatch spacing of lines!")

    #write mark and jumps
    for i, pair in enumerate(intersecting_points):
        write_jmp(file, pair[0])
        write_mrk(file, pair[1])


def obj_func(vars, m, diff, x1, y1, x2, y2):
    # m, diff, x1, y1, x2, y2 = p[0], p[1], p[2], p[3], p[4], p[5]

    #x1,y1 corresponds to first line (m,b1), x2,y2 corresponds to second line (m, b2)
    b1 = vars/0.01
    b2 = b1 + diff
    d1 = perp_dist_of_line_and_point(m, b1, x1, y1)
    d2 = perp_dist_of_line_and_point(m, b2, x2, y2)
    ret_val = (d1 - d2)**2*1E6
    return ret_val

def angle_to_slope(angle_deg):
#returns None if slope is infinite
    if angle_deg < 0:
        raise("Don't let this number be less than 0")
    angle_deg = angle_deg % 360
    if 0<=angle_deg<=180:
        angle_deg = 180 - angle_deg
    elif 180<angle_deg<360:
        angle_deg = 360+180-angle_deg

    if angle_deg == 90 or angle_deg == 270:
        return math.inf
    elif angle_deg == 180 or angle_deg == 0:
        return 0
    else:
        angle_rad = angle_deg*math.pi/180
        slope = math.tan(angle_rad)
        return slope

def return_b_from_point_slope(x, y, m):
    #y = mx+b
    return y-m*x

def perp_dist_of_line_and_point(m, b, x, y):
    p1 = np.asarray([0, b])
    p2 = np.asarray([1, m+b])
    p3 = np.asarray([x, y])
    return np.abs(np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1))

def dist_of_parallel_lines(m, b1, b2):
    if m != math.inf:
        return perp_dist_of_line_and_point(m, b1, 0, b2)
    else:
        return abs(b2-b1)

def square_line_intersection(bottom, left, right, top, m, b):
    #to input a vertical line, submit math.inf to m, and the value of x at b
    # x = left
    # x = right
    # y = bottom
    # y = top
    # y = m*x + b

    # initialize
    x_intersect = []
    y_intersect = []

    #takes care of vertical lines
    if m == math.inf:
        if left<=b<=right:
            y = [bottom, top]
            x = [b, b]
            intersecting_points_list = list(zip(x, y))
            return intersecting_points_list
        else:
            return []

    # takes care of horizontal lines
    if m == 0:
        #takes care of horizontal lines (m=0)
        if bottom<=b<=top:
            y = [b, b]
            x = [left, right]
            intersecting_points_list = list(zip(x, y))
            return intersecting_points_list
        else:
            return []

    #takes care of non-horizontal and non-vertical lines
    #Find intersections
    #left y = m*left + b
    y = m*left+b
    x = left
    y_intersect.append(y)
    x_intersect.append(x)
    #right
    y = m*right+b
    x = right
    y_intersect.append(y)
    x_intersect.append(x)
    #top, top = m*x + b
    y = top
    x = (top-b)/m
    y_intersect.append(y)
    x_intersect.append(x)
    #bottom
    y = bottom
    x = (bottom-b)/m
    y_intersect.append(y)
    x_intersect.append(x)

    #check if they are within the square
    x_intersect = [float(e) for e in x_intersect]
    y_intersect = [float(e) for e in y_intersect]
    intersecting_points_list = [(x,y) for x,y in zip(x_intersect, y_intersect) if (left<=x<=right and bottom<=y<=top)]
    #get rid of any duplicates by forming a set and then casting to a list so the all method works below
    intersecting_points_list = {x for x in intersecting_points_list}

    if not intersecting_points_list:
        return []
    elif len(intersecting_points_list) != 2:
        raise("Error in Intersection Algorithm")

    return list(intersecting_points_list)

def plot_xml(xml_filepath):
    oct_ec.plot_xml(xml_filepath)
