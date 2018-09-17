from Pipe_And_Filter_Autosection.classes.GalvoData import GalvoData as GD
import numpy as np
import pickle as pk

neg100neg100_filepath = r'./m_b_vars/neg100neg100.2d_dbl'
pos100pos100_fileopath = r'./m_b_vars/pos100pos100.2d_dbl'

neg_gd = GD(neg100neg100_filepath, 3, 50000)
pos_gd = GD(pos100pos100_fileopath, 3, 50000)

neg_100_x = np.mean(neg_gd.x_data)
neg_100_y = np.mean(neg_gd.y_data)

pos_100_x = np.mean(pos_gd.x_data)
pos_100_y = np.mean(pos_gd.y_data)

m_x = (pos_100_x - neg_100_x)/200
b_x = pos_100_x - m_x*100

m_y = (pos_100_y - neg_100_y)/200
b_y = pos_100_y - m_y*100

for str in ['m_x', 'b_x', 'm_y', 'b_y']:
    print(str + " is: {}".format(eval(str)))

with open(r'./m_b_vars/m_b.pickle', 'wb') as f:
    pk.dump([m_x, b_x, m_y, b_y], f)

