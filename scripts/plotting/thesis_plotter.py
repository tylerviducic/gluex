# barebones script for plotting things for things for thesis 

import ROOT
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

data_file = '/work/halld/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_bestX2_2017.root'
file_treename = 'pipkmks__B4_M16'

df = ROOT.RDataFrame(file_treename, data_file)
print("maybe i should do this in a notebook...")