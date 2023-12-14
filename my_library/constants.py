"""
this file contains constants and fit parameters used throughout the analysis
"""


## KSHORT FIT PARAMETERS ##

KSHORT_FIT_WIDTH = 0.01035
KSHORT_FIT_MEAN = 0.4971

## KKPI BRANCHING FRACTION ##

F1_KKPI_BRANCHING_FRACTION = 0.091
F1_KKPI_BRANCHING_FRACTION_ERROR = 0.004

## PI- K+ KS FIT PARAMETERS ##

F1_PIMKPKS_VOIGHT_SIGMA = 0.01138
F1_PIMKPKS_VOIGHT_SIGMA_ERROR = 0.0002604619596671496
F1_PIMKPKS_ACCEPTANCE_CORRECTED_VOIGHT_SIGMA = 0.0104626
F1_PIMKPKS_ACCEPTANCE_CORRECTED_VOIGHT_SIGMA_ERROR = 0.0004433

F1_PIMKPKS_VOIGHT_MEAN = 1.2857
F1_PIMKPKS_VOIGHT_MEAN_ERROR = 0.0003337361295636665
F1_PIMKPKS_ACCEPTANCE_CORRECTED_VOIGHT_MEAN = 1.2844
F1_PIMKPKS_ACCEPTANCE_CORRECTED_VOIGHT_MEAN_ERROR = 0.0004577578618949474

F1_PIMKPKS_VOIGHT_WIDTH = 0.02683
F1_PIMKPKS_VOIGHT_WIDTH_ERROR = 0.0016326819246298974
F1_PIMKPKS_ACCEPTANCE_CORRECTED_VOIGHT_WIDTH = 0.028369
F1_PIMKPKS_ACCEPTANCE_CORRECTED_VOIGHT_WIDTH_ERROR = 0.004577578618949474

## PI+ K- KS FIT PARAMETERS ##

F1_PIPKMKS_VOIGHT_SIGMA = 0.01138
F1_PIPKMKS_VOIGHT_SIGMA_ERROR = 0.0002604619596671496
F1_PIPKMKS_ACCEPTANCE_CORRECTED_VOIGHT_SIGMA = 0.0102287
F1_PIPKMKS_ACCEPTANCE_CORRECTED_VOIGHT_SIGMA_ERROR = 0.000273588

F1_PIPKMKS_VOIGHT_MEAN = 1.281
F1_PIPKMKS_VOIGHT_MEAN_ERROR = 0.0004587873563844935
F1_PIPKMKS_ACCEPTANCE_CORRECTED_VOIGHT_MEAN = 1.2787
F1_PIPKMKS_ACCEPTANCE_CORRECTED_VOIGHT_MEAN_ERROR = 0.0005084747325606598

F1_PIPKMKS_VOIGHT_WIDTH = 0.03001
F1_PIPKMKS_VOIGHT_WIDTH_ERROR = 0.002460215118252382
F1_PIPKMKS_ACCETPANCE_CORRECTED_VOIGHT_WIDTH = 0.02631
F1_PIPKMKS_ACCETPANCE_CORRECTED_VOIGHT_WIDTH_ERROR = 0.002782548323692978

# COLORBLIND HEX CODES #
COLORBLIND_HEX_DICT = { 
    'blue': '#0173B2',
    'orange': '#DE8F05',
    'green': '#029E73',
    'red': '#D55E00',
    'purple': '#CC78BC',
    'brown': '#CA9161',
    'pink': '#FBAFE4',
    'gray': '#949494',
    'yellow': '#ECE133',
    'cyan': '#56B4E9'
}

TWELVE_COLORBLIND_HEX_DICT = {
    'deep magenta': '#9F0162',
    'jungle green': '#009F81',
    'hot pink': '#FF5AAF',
    'aqua': '#00FCCF',
    'purple': '#8400CD',
    'blue': '#008DF9',
    'cyan': '#00C2F9',
    'plum': '#FFB2FD',
    'ruby red': '#A40122',
    'red': '#E20134',
    'orange': '#FF6E3A',
    'yellow': '#FFC33B'
}

# MATPLOTLIB LATEX AXIS LABEL STRING #
LATEX_AXIS_LABEL_DICT = {
    't': '$-t$ (GeV$^2$)',
    'cross_section': '$\\frac{d\\sigma}{dt}$ $\\frac{nb}{GeV^2}$',
    'yield': 'counts',
    'flux_corrected_yield': 'counts',
    'acceptance': 'acceptance',
    'mean': 'mean (GeV)',
    'width': 'width (GeV)',
    'chi2ndf': '$\\frac{\\chi^2}{ndf}$',
    'pipkmks': '$\\pi^+K^-K_s$',
    'pimkpks': '$\\pi^-K^+K_s$'
}

LATEX_PLOT_TITLE_DICT = {
    'cross_section': 'Cross Section',
    'yield': 'Yields',
    'flux_corrected_yield': 'Flux Normalized Yields',
    'acceptance': 'Acceptance',
    'mean': 'BW Mean',
    'width': 'BW Width',
    'chi2ndf': 'Fit $\\chi^2$/ndf',
    'pipkmks': '$\\pi^+K^-K_s$',
    'pimkpks': '$\\pi^-K^+K_s$'
}

RUN_DICT = {
    'fall': '2018_fall',
    'spring': '2018_spring',
    '2017': '2017',
    '2019_unconstrained': '2019_unconstrained',
    '2019_constrained': '2019_constrained'
        }

F1_CUT_LIST_PIPKMKS = ['no', 'plus', 'zero', 'all']
F1_CUT_LIST_PIMKPKS = ['no', 'minus', 'zero', 'all']


KSTAR_CUT_TITLE_DICT = {
    'no': 'No K* Rejection',
    'plus': 'K*^{+} Rejected',
    'minus': 'K*^{-} Rejected',
    'zero': 'K*^{0} Rejected',
    'all': 'Both K* Rejected'
}


ALLOWED_E_BINS = range(7, 12)
ALLOWED_T_BINS = range(1, 8)
ALLOWED_RUN_PERIODS = ['spring', 'fall', '2017']
ALLOWED_CHANNELS = ['pipkmks', 'pimkpks']
ALLOWED_DATATYPES_RECON = ['data', 'signal', 'phasespace', 'nstar', 'f1_1420']
ALLOWED_DATATYPES_THROWN = ['signal', 'phasespace']
ALLOWED_NSTAR_MASSES = [1440, 1520, 1535, 1650, 1675, 1680, 1700, 1710, 1720]

T_BIN_DICT = {1: '0.1_0.2', 2: '0.2_0.3', 3: '0.3_0.4',
              4: '0.4_0.65', 5: '0.65_0.9', 
              6: '0.9_1.4', 7: '1.4_1.9'
              }

T_CUT_DICT = {0: (0.0, 0.1), 1: (0.1, 0.2), 2: (0.2, 0.3), 3: (0.3, 0.4),
              4: (0.4, 0.65), 5: (0.65, 0.9), 
              6: (0.9, 1.4), 7: (1.4, 1.9)
              }

T_WIDTH_DICT = {1: 0.1, 2: 0.1, 3: 0.1, 4: 0.25, 5: 0.25, 6: 0.5, 7: 0.5}

FLUX_DICT = {
    'fall': '50685_51768',
    'spring': '40856_42559'
        }

BEAM_DICT = {
    7: '6.5_7.5',
    8: '7.5_8.5',
    9: '8.5_9.5',
    10: '9.5_10.5',
    11: '10.5_11.5'
        }

BEAM_CUT_DICT = {
    7: (6.5, 7.5),
    8: (7.5, 8.5),
    9: (8.5, 9.5),
    10: (9.5, 10.5),
    11: (10.5, 11.5)
}

BEAM_INDEX_DICT = {
    1: (6.5, 7.5),
    2: (7.5, 8.5),
    3: (8.5, 9.5),
    4: (9.5, 10.5),
    5: (10.5, 11.5)
}


