# plot k* cuts in bins of t in postange plots
import ROOT

filename = '/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/pipkmks_flat_result_2018_spring.root'
data_file = ROOT.TFile(filename, 'READ')


width = 'wide'
beam = 8

t_low =  ['0.1', '0.2', '0.3', '0.4'] # ['0.1', '0.15',
t_med = ['0.65', '0.9']
t_high = ['1.4', '1.9']#, '1.7', '1.9']

cuts = ['kstar_plus_cut', 'kstar_zero_cut', 'kstar_all_cut']
color_dict = {
    'kstar_all_cut': 2,
    'kstar_plus_cut': 4,
    'kstar_zero_cut': 1
}

c1 = ROOT.TCanvas()
c1.Divide(2,4)

hist_array = []
for t in t_low:
    for cut in cuts:
        hist_name = f'pipkmks_beam_{beam}_t_{t}_{cut}_{width}'
        hist = data_file.Get(hist_name)
        hist.SetLineColor(color_dict[cut])
        hist_array.append(hist)
        
for t in t_med:
    for cut in cuts:
        hist_name = f'pipkmks_beam_{beam}_t_{t}_{cut}_{width}'
        hist = data_file.Get(hist_name)
        hist.SetLineColor(color_dict[cut])
        hist_array.append(hist)

for t in t_high:
    for cut in cuts:
        hist_name = f'pipkmks_beam_{beam}_t_{t}_{cut}_{width}'
        hist = data_file.Get(hist_name)
        hist.SetLineColor(color_dict[cut])
        hist_array.append(hist)

for i in range(len(hist_array)):
    c1.cd((int)(i/3+1))
    hist_array[i].Draw("same")

c1.Update()