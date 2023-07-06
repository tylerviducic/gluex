# script to calculate the flux-corrected yields from the acceptance-corrected yields

import ROOT
import pandas as pd
import matplotlib.pyplot as plt
from common_analysis_tools import *

channel = 'pipkmks'
binned_fit_results = f'/work/halld/home/viducic/data/fit_params/{channel}/cross_section_values.csv'