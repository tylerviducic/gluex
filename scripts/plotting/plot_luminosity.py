# script to plot the luminosity from my method in common analysis tools 

import ROOT
from common_analysis_tools import *
import matplotlib.pyplot as plt

beam_center = []
lumis = []

for i in range(7, 11):
    lumi = get_luminosity_gluex_1(i - 0.5, i + 0.5)
    beam_center.append(i)
    lumis.append(lumi)

plt.plot(beam_center, lumis)
plt.xlabel('Beam center (GeV)')
plt.ylabel('Luminosity (nb^-1)')
plt.title('Luminosity vs. beam center')
plt.savefig('/work/halld/home/viducic/plots/cross_section/luminosity_vs_beam_center.png')

