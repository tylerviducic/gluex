# script to get the integrated acceptance for the binned e and t

import ROOT
import pandas as pd
import numpy as np
from common_analysis_tools import *

channel = 'pipkmks'

for e in range(7, 11):
    for t in range(1, 8):
        continue 