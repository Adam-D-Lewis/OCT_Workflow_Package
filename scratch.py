from write_scan_param_file_with_offset_data import write_scan_param_file_with_offset_data
import writeEC1000file as EC

crd_set = [[[-25, -10.35], [25, -23.05]],
           [[-25, 6.35], [25, -6.35]],
           [[-25, 23.05], [25, 10.35]],
           [[-41.7, 25], [-29, -25]],
           [[29, 25], [41.7, -25]]]

# (filepath, x0, y0, w, h, start_delay=0.4, hs=0.2794, galvo_speed=1500):

for i, crds in enumerate(crd_set):
    filename = r'./scan_param_bar{}.txt'.format(i+1)

    crd1 = crds[0]
    crd2 = crds[1]

    # x1, y1 = crd1
    # x2, y2 = crd2
    # w = abs(x2-x1)
    # h = abs(y2 - y1)

    write_scan_param_file_with_offset_data(filename, crd1, crd2)

# EC.write_oct_ec1000_file(filename, w, h, start_delay=0.7, hs=0.03,)