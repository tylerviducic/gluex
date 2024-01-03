
import ROOT
import sys
sys.path.append('/work/halld/home/viducic/')

import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.gluex_style as gluex_style
import my_library.kinematic_cuts as cuts


#module load python/3.9.5
# module load gcc/10.2.0
# source /apps/root/6.28.06/root-6.28.06-gcc10.2.0/bin/thisroot.csh


ROOT.EnableImplicitMT()

# TODO: start debugging this script to vary kinematic cuts using RDataFrame .Vary() method 

channel = 'pipkmks'
df = tools.get_dataframe(channel, 'gluex1', 'data', filtered=False)

# print the version of ROOT this script is using
print('ROOT version: ', ROOT.gROOT.GetVersion())