import scipy.optimize as opt
import matplotlib.pyplot as plt
import numpy as np
# test file

#generate sample data to test
galvo_data = [0, 0, 0, 0, 1, 2, 2, 2, 5, 6, 7, 8, 9, 2, 2, 2]
galvo_data += np.random.normal(0, 0.001, len(galvo_data))

parsed_xml_data = [0, 0, 2, 2, 5, 9, 2, 2]

nvars = len(parsed_xml_data)-2

def y_m(x, vars0):
    #x is the x value I want to get the function value at (index)
    #vars is a list of x values where segments end (except for last segment) (values increase monotonically and are all <= len(galvo_data)
    #soln_vars0 = [3, 5]
    vars = np.concatenate((vars0, [len(galvo_data)-1]))
    # vars is a list of x values where segments end (including for last segment) (values increase monotonically and are all <= len(galvo_data)
    # soln_vars = [3, 5, 7]

    #I need to find which segment I'm evaluating in (endpoints are in the segment preceeding them (not the one coming up))
    segNum = next(i+1 for i, val in enumerate(vars) if x <= val)

    #determine if flat segment or not
    if parsed_xml_data[segNum] == parsed_xml_data[segNum-1]:
        nonZeroSlope = False
        return parsed_xml_data[segNum]
    else:
        # has nonzero slope
        nonZeroSlope = True
        y0, y1 = parsed_xml_data[segNum-1:segNum+1]
        x0, x1 = vars[segNum-2:segNum]
        slope2 = (parsed_xml_data[segNum]-parsed_xml_data[segNum-1])/(vars[segNum]-vars[segNum-1])
        slope = (y1-y0)/(x1-x0)
        return slope*(x-x0) + y0

#define func
def objective_func(x):
    #x is a 2 element vector in this case
    abs_err = []
    for i, elem in enumerate(galvo_data):
        abs_err.append(abs(elem-y_m(i, x)))
    sum_abs_err = sum(abs_err)
    return sum_abs_err

def con_fun(x):
    most_con = []
    for i in range(len(x)-1):
        most_con.append(x[i+1]-x[i])
    con = np.concatenate(([x[0]-1], most_con, [len(galvo_data)-x[-1]]))
    return con

constr = {'type': 'ineq', 'fun': con_fun}
bnds = ((0, 13), (0, 13), (0, 13), (0, 13), (0, 13), (0, 13))
x0 = range(0,11,2)
ans = opt.minimize(objective_func, x0, bounds=bnds)
ab = ans.x
ab_floor = np.round(ans.x)
error = objective_func(ab_floor)

plt.figure()
plt.plot(galvo_data, label='data')
xvals = np.asarray(range(len(galvo_data)))
yvals = []
for val in xvals:
    yvals.append(y_m(val, ans.x))
plt.plot(xvals, yvals, label='fit')
plt.legend()

plt.show()
print('bye')