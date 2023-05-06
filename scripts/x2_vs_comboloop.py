# script to validate X2 method of analysis vs combolooping and accidental weighting

import ROOT

run_period_dict = {
    'spring': '2018_spring',
    'fall': '2018_fall',
    '2017': '2017'
}

run_period = 'spring'
channel = 'pipkmks'

file_path = '/work/halld/home/viducic/selector_output/'
bx2_filename = f'f1_flat/{channel}_filtered_{run_period_dict[run_period]}.root'
comboloop_filename = f'f1/{channel}_comboloop_flat_{run_period_dict[run_period]}.root'

bx2_tree = f'{channel}_filtered_{run_period_dict[run_period]}'
comboloop_tree = f'{channel}__B4_M16'

bxdf = ROOT.RDataFrame(bx2_tree, file_path + bx2_filename)
combodf = ROOT.RDataFrame(comboloop_tree, file_path + comboloop_filename)

pp_cut = 'p_p > 0.4'

combodf = combodf.Define('p_p', 'sqrt(p_px*p_px + p_py*p_py + p_pz*p_pz)')

combodf = combodf.Filter(pp_cut)

print(f'N_events in bx2 df: {bxdf.Count().GetValue()}')
print(f'N_events in combo df after pp cut: {combodf.Count().GetValue()}')

bx_columns = set([str(bxdf.GetColumnNames()[i]) for i in range(bxdf.GetColumnNames().size())])
combo_columns = set([str(combodf.GetColumnNames()[i]) for i in range(combodf.GetColumnNames().size())])

diff1 = bx_columns - combo_columns
diff2 = combo_columns - bx_columns
print(f'Columns in bx2 df but not in combo df: {diff1}')
print(f'Columns in combo df but not in bx2 df: {diff2}')