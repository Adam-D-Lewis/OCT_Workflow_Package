import writeEC1000file as EC

with open(r'./thang.xml', 'w+') as f:
    EC.write_rotating_square(f, 90, [-1, 1], [1, -1], hs=0.1)