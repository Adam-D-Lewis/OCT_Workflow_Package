#!/usr/bin/env python
import os

dir_path = r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\2018_10_31 Curl Part\layer_files'

for file in os.listdir(dir_path):
    if file.endswith('.xml'):
            fpath = os.path.join(dir_path, file)
            with open(fpath, 'r') as f:
                text = f.read()
            with open(fpath, 'w') as f:
                text2 = text.replace(r"<Set id='LaserPower'>255</Set>", r"<Set id='LaserPulse'>1,160,400</Set>")
                f.write(text2)
