import scipy.optimize as opt
import matplotlib.pyplot as plt
import numpy as np
# test file

#generate sample data to test
data = [0, 0, 0, 0, 1, 2, 2, 2]

def y_m(x,a,b):
    if 0<=x<a:
        ans = 0
    elif a<=x<b:
        ans = 2/(b-a)*(x-a)
    elif b<=x<=7:
        ans = 2
    return ans

#define func
def objective_func(x):
    #x is a 2 element vector in this case
    a, b = x[0], x[1]
    abs_err = []
    for i, elem in enumerate(data):
        abs_err.append(abs(elem-y_m(i, a, b)))
    sum_abs_err = sum(abs_err)
    return sum_abs_err

def con_fun(x):
    a, b =x[0], x[1]
    return b-a

objective_func([2,3])

constr = {'type': 'ineq', 'fun': con_fun}
bnds = ((0, 7), (0, 7))
ans = opt.minimize(objective_func, (0, 1), bounds=bnds, constraints=constr)

a = ans.x[0]
b = ans.x[1]

plt.figure()
plt.plot(data, label='data')
xvals = np.asarray(range(len(data)))
yvals = []
for val in xvals:
    yvals.append(y_m(val, a, b))
plt.plot(xvals, yvals, label='fit')
plt.legend()
plt.show()
print('bye')