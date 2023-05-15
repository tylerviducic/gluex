# plot the quantity M(recon)-M(thrown) for the signal MC

import ROOT
from common_analysis_tools import *

file_and_tree = get_flat_file_and_tree('pipkmks', 'spring', 'signal')
df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])

df = df.Define('p_px_thrown', 'p_p4_true.Px()')
df = df.Define('p_py_thrown', 'p_p4_true.Py()')
df = df.Define('p_pz_thrown', 'p_p4_true.Pz()')
df = df.Define('p_E_thrown', 'p_p4_true.E()')

df = df.Define('pip1_px_thrown', 'pip1_p4_true.Px()')
df = df.Define('pip1_py_thrown', 'pip1_p4_true.Py()')
df = df.Define('pip1_pz_thrown', 'pip1_p4_true.Pz()')
df = df.Define('pip1_E_thrown', 'pip1_p4_true.E()')

df = df.Define('pip2_px_thrown', 'pip2_p4_true.Px()')
df = df.Define('pip2_py_thrown', 'pip2_p4_true.Py()')
df = df.Define('pip2_pz_thrown', 'pip2_p4_true.Pz()')
df = df.Define('pip2_E_thrown', 'pip2_p4_true.E()')

df = df.Define('pim_px_thrown', 'pim_p4_true.Px()')
df = df.Define('pim_py_thrown', 'pim_p4_true.Py()')
df = df.Define('pim_pz_thrown', 'pim_p4_true.Pz()')
df = df.Define('pim_E_thrown', 'pim_p4_true.E()')

df = df.Define('km_px_thrown', 'km_p4_true.Px()')
df = df.Define('km_py_thrown', 'km_p4_true.Py()')
df = df.Define('km_pz_thrown', 'km_p4_true.Pz()')
df = df.Define('km_E_thrown', 'km_p4_true.E()')

df = df.Define('pipkmks_px_thrown', 'pip1_px_thrown + pip2_px_thrown + km_px_thrown + pim_px_thrown')
df = df.Define('pipkmks_py_thrown', 'pip1_py_thrown + pip2_py_thrown + km_py_thrown + pim_py_thrown')
df = df.Define('pipkmks_pz_thrown', 'pip1_pz_thrown + pip2_pz_thrown + km_pz_thrown + pim_pz_thrown')
df = df.Define('pipkmks_E_thrown', 'pip1_E_thrown + pip2_E_thrown + km_E_thrown + pim_E_thrown')
df = df.Define('pipkmks_m_thrown', 'sqrt(pipkmks_E_thrown*pipkmks_E_thrown - pipkmks_px_thrown*pipkmks_px_thrown - pipkmks_py_thrown*pipkmks_py_thrown - pipkmks_pz_thrown*pipkmks_pz_thrown)')

df = df.Define('pipkmks_resolution', 'pipkmks_m - pipkmks_m_thrown')

hist = df.Histo1D(('pipkmks_resolution', 'pipkmks_resolution', 100, -0.1, 0.1), 'pipkmks_resolution')
hist.Draw()

input('Press any key to continue...')