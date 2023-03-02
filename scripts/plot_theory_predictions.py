# plot theory predictions provided by Nanjing Normal

import pandas as pd
import matplotlib.pyplot as plt

filename8 = '/Users/tylerviducic/research/gluex/theory_predictions/t-slope-8GeVnew.dat'
filename9 = '/Users/tylerviducic/research/gluex/theory_predictions/t-slope-9GeVnew.dat'
filename10 = '/Users/tylerviducic/research/gluex/theory_predictions/t-slope-10GeVnew.dat'
filename11 = '/Users/tylerviducic/research/gluex/theory_predictions/t-slope-11GeVnew.dat'

df8 = pd.read_csv(filename8, delim_whitespace=True)
df9 = pd.read_csv(filename9, delim_whitespace=True)
df10 = pd.read_csv(filename10, delim_whitespace=True)
df11 = pd.read_csv(filename11, delim_whitespace=True)
df8.columns = ['minus_t', 'diff_cs']
df9.columns = ['minus_t', 'diff_cs']
df10.columns = ['minus_t', 'diff_cs']
df11.columns = ['minus_t', 'diff_cs']


fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.scatter(df8['minus_t'], df8['diff_cs'], marker='o' ,color='black', s=3)
ax2.scatter(df9['minus_t'], df9['diff_cs'],marker = 'P', color='red', s=3)
ax2.scatter(df10['minus_t'], df10['diff_cs'],marker = 's', color='blue', s=3)
ax2.scatter(df11['minus_t'], df11['diff_cs'],marker = '*', color='purple', s=3)
# ax2.plot(df8['minus_t'], df8['diff_cs'], color='black')
ax2.set_ylabel("d_sigma/d_t")
ax2.set_xlabel("-t (GeV)^2")
ax2.set_title("d_sigma/d_t vs -t")
ax2.set_yscale('log')
plt.xlim([0, 2])

plt.show()

