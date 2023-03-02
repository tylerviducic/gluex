# draws binned pion masses

import ROOT

histogram_array = []

# file_name = '/w/halld-scifs17exp/home/viducic/selector_output/pi0_2018_full.root'
#file_name = '/w/halld-scifs17exp/home/viducic/selector_output/pi0_premakoff.root'
file_name = '/work/halld/home/mfarrell/pi0_2017_2.root'

c1 = ROOT.TCanvas("c1")
c1.Divide(5, 2, 0.01, 0.01)

hist_file = ROOT.TFile.Open(file_name, "READ") 

for i in range(12, 144, 12):
    if i < 100:
        histo_name = 'BinnedPionMass_0.0{}'.format(i)
        histogram_array.append(hist_file.Get(histo_name))
    else:
        histo_name = 'BinnedPionMass_0.{}'.format(i)
        histogram_array.append(hist_file.Get(histo_name))

for x in range(len(histogram_array)):
    c1.cd(x + 1)
    histogram_array[x].Draw()