import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.kinematic_cuts as kcuts
import os

ROOT.EnableImplicitMT()
os.nice(18)

channel = 'pipkmks'
data_type = 'data'

particles = {
    'proton': ('p', 'p'),
    'kaon': ('km', 'kp'),
    'pion': ('pip1', 'pim1'),
    'ks_pip': ('pip2', 'pip'),
    'ks_pim': ('pim', 'pim2'),
}

if channel == 'pipkmks':
    p_index = 0
    kstar_cut = kcuts.KSTAR_ALL_CUT_PIPKMKS
    signal_region = kcuts.F1_SIGNAL_REGION_PIPKMKS
else:
    p_index = 1
    kstar_cut = kcuts.KSTAR_ALL_CUT_PIMKPKS
    signal_region = kcuts.F1_SIGNAL_REGION_PIMKPKS

kinematics = {
    'px': [(-1.5, 1.5), (-1, 1), (-0.5, 0.5), (-0.6, 0.6), (-0.6, 0.6)],
    'py': [(-1.5, 1.5), (-1, 1), (-0.5, 0.5), (-0.6, 0.6), (-0.6, 0.6)],
    'pz': [(0.1, 1.3), (1.5, 7), (0.4, 4.0), (0, 5), (0, 5)],
    'p': [(0.4, 1.9), (1.5, 7), (0.4, 4.0), (0.0, 5.0), (0.0, 5.0)],
    'theta': [(40, 70), (0, 16), (0, 25), (0, 30), (0, 30)],
    'phi': [(-180, 180), (-180, 180), (-180, 180), (-180, 180), (-180, 180)]
}

if data_type == 'data':
    run_period = 'gluex1'
else:
    run_period = 'fall'

df = tools.get_dataframe(channel, run_period, data_type)
df = df.Filter(kstar_cut).Filter(signal_region).Filter(kcuts.BEAM_RANGE).Filter(kcuts.T_RANGE)


hists = []
for i, particle in enumerate(particles):

    part = particles[particle][p_index]
    for kin in kinematics:
        xlow = kinematics[kin][i][0]
        xhigh = kinematics[kin][i][1]
        # n_bins = int((xhigh-xlow)/bin_size)

        if data_type == 'data':
            if kin == 'phi':
                n_bins = 45
            else:
                n_bins = 100
        else:
            if kin == 'phi':
                n_bins = 180
            else:
                n_bins = 1000

        # print(f'particle: {particle}, kinmatic: {kin}, x_low: {xlow}, x_high: {xhigh}, n_bins: {n_bins}, column: {part}_{kin}')
        hist = df.Histo1D((f'{channel}_{particle}_{kin}_{data_type}', f'{channel}_{particle}_{kin}_{data_type}', n_bins, xlow, xhigh), f'{part}_{kin}')
        hists.append(hist)

df.Count().GetValue()

out_file = ROOT.TFile.Open(f'/work/halld/home/viducic/scripts/plotting/{channel}_{data_type}_kinematic_hists.root','RECREATE')

for h in hists:
    h.GetPtr().Write()

out_file.Close()