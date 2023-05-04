# script for fitting ksk-pi+ distribution with a cut applied to one of the other K*

import ROOT as r

channel = 'pipkmks'
run_period = 'fall'
run_dict = {
    'fall': '2018_fall',
    'spring': '2018_spring',
    '2017': '2017'
}

filename = f'/work/halld/home/viducic/selector_output/f1_flat/{channel}_flat_result_{run_dict[run_period]}.root'