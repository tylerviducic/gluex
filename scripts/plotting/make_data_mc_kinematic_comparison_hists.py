import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.kinematic_cuts as kcuts
import my_library.gluex_style as gxs 
import os

ROOT.EnableImplicitMT()
os.nice(18)

particles = {
    'proton': ('p', 'p'),
    'kaon': ('km', 'kp'),
    'pion': ('pip1', 'pim1'),
    'ks_pip': ('pip2', 'pip'),
    'ks_pim': ('pim', 'pim2'),
}

kinematics = {
    'px': [(-1.5, 1.5), (-1, 1), (-0.5, 0.5), (-0.6, 0.6), (-0.6, 0.6)],
    'py': [(-1.5, 1.5), (-1, 1), (-0.5, 0.5), (-0.6, 0.6), (-0.6, 0.6)],
    'pz': [(0.1, 1.3), (1.5, 7), (0.4, 4.0), (0, 5), (0, 5)],
    'p': [(0.4, 1.9), (1.5, 7), (0.4, 4.0), (0.0, 5.0), (0.0, 5.0)],
    'theta': [(40, 70), (0, 16), (0, 25), (0, 30), (0, 30)],
    'phi': [(-180, 180), (-180, 180), (-180, 180), (-180, 180), (-180, 180)]
}

x_titles = {
    'px': 'p_{x} [GeV/c]',
    'py': 'p_{y} [GeV/c]',
    'pz': 'p_{z} [GeV/c]',
    'p': 'p [GeV/c]',
    'theta': '#theta [deg]',
    'phi': '#phi [deg]'
}

particle_labels = {
    'proton': 'Proton',
    'kaon': 'Kaon',
    'pion': 'Pion',
    'ks_pip': 'K_{S} #rightarrow #pi^{+}',
    'ks_pim': 'K_{S} #rightarrow #pi^{-}'
}



def main(channel, data_type):

    if channel == 'pipkmks':
        p_index = 0
        kstar_cut = kcuts.KSTAR_ALL_CUT_PIPKMKS
        signal_region = kcuts.F1_SIGNAL_REGION_PIPKMKS
        line_color = ROOT.kBlue
    else:
        p_index = 1
        kstar_cut = kcuts.KSTAR_ALL_CUT_PIMKPKS
        signal_region = kcuts.F1_SIGNAL_REGION_PIMKPKS
        line_color = ROOT.kRed

    if data_type == 'data':
        run_period = 'gluex1'
        marker = 20
        marker_size = 1.5
        scale_frac = 1
    else:
        run_period = 'fall'
        marker = 21
        line_color = ROOT.kBlack
        marker_size = 1.0
        scale_frac = 3

    df = tools.get_dataframe(channel, run_period, data_type)
    df = df.Filter(signal_region).Filter(kcuts.BEAM_RANGE).Filter(kcuts.T_RANGE)


    hists = []
    for i, particle in enumerate(particles):

        part = particles[particle][p_index]
        for kin in kinematics:
            xlow = kinematics[kin][i][0]
            xhigh = kinematics[kin][i][1]
            # n_bins = int((xhigh-xlow)/bin_size)

            if data_type == 'data':
                if kin == 'phi':
                    n_bins = 90
                else:
                    n_bins = 100
            else:
                if kin == 'phi':
                    n_bins = 270
                else:
                    n_bins = 300

            # print(f'particle: {particle}, kinmatic: {kin}, x_low: {xlow}, x_high: {xhigh}, n_bins: {n_bins}, column: {part}_{kin}')
            hist = df.Histo1D((f'{channel}_{particle}_{kin}_{data_type}', f'{channel}_{particle}_{kin}_{data_type}', n_bins, xlow, xhigh), f'{part}_{kin}')
            hist.SetLineColor(line_color)
            hist.SetMarkerStyle(marker)
            hist.SetMarkerColor(line_color)
            # hist.SetMarkerSize(marker_size)
            hist.GetYaxis().SetTitle('Normalized Counts')
            hist.GetYaxis().SetTitleOffset(1.55)
            hist.GetXaxis().SetTitle(particle_labels[particle] + ' ' + x_titles[kin])
            hists.append(hist)

    df.Count().GetValue()

    out_file = ROOT.TFile.Open(f'/work/halld/home/viducic/scripts/plotting/{channel}_{data_type}_kinematic_hists.root','RECREATE')

    for h in hists:
        h.GetPtr().Scale(scale_frac/h.GetPtr().Integral())
        h.GetPtr().Write()

    out_file.Close()

if __name__ == '__main__':
    main('pipkmks', 'data')
    main('pipkmks', 'signal')
    main('pimkpks', 'data')
    main('pimkpks', 'signal')