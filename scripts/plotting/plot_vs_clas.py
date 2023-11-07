# plot ACY vs CLAS 

from cmath import sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def tri(a, b, c):
    return a*a - 2 * a * (b + c) + (b - c) * (b - c)

def w_to_egamma(w):
    mp = 0.93827
    return (w**2 - mp**2)/(2*mp)

def cosTheta_to_t(w, cosTheta):
    m1 = 0.93827**2
    m3 = 0.93827**2
    m2 = 0
    m4 = 1.285**2
    s = w*w
    qi = sqrt(tri(s, m1, m2)/4/s)
    qf = sqrt(tri(s, m3, m4)/4/s)
    som = m1 + m2 + m3 + m4

    t = -1 * (2 * qi * qf * cosTheta + som/2 - s/2 - (m1 - m2) * (m3 - m4) / 2 / s)
    return t


def t_over_cosTheta(w, cosTheta):
    m1 = 0.93827**2
    m3 = 0.93827**2
    m2 = 0
    m4 = 1.285**2
    s = w*w
    qi = sqrt(tri(s, m1, m2)/4/s)
    qf = sqrt(tri(s, m3, m4)/4/s)
    som = m1 + m2 + m3 + m4

    return -1/(2 * qi * qf + (som/2 - s/2 - (m1 - m2) * (m3 - m4) / 2 / s)/cosTheta)



list_W = [2.35, 2.35, 2.35, 2.35, 2.35, 2.35, 2.35, 2.35, 2.35,
          2.45, 2.45, 2.45, 2.45, 2.45, 2.45, 2.45, 2.45, 2.45,
          2.55, 2.55, 2.55, 2.55, 2.55, 2.55, 2.55, 2.55, 2.55,
          2.65, 2.65, 2.65, 2.65, 2.65, 2.65, 2.65, 2.65, 2.65,
          2.75, 2.75, 2.75, 2.75, 2.75, 2.75, 2.75, 2.75, 2.75]

list_cosThetaCM = [-0.70, -0.50, -0.30, -0.10, 0.10, 0.30, 0.50, 0.70, 0.85,
                   -0.70, -0.50, -0.30, -0.10, 0.10, 0.30, 0.50, 0.70, 0.85,
                   -0.70, -0.50, -0.30, -0.10, 0.10, 0.30, 0.50, 0.70, 0.85,
                   -0.70, -0.50, -0.30, -0.10, 0.10, 0.30, 0.50, 0.70, 0.85,
                   -0.70, -0.50, -0.30, -0.10, 0.10, 0.30, 0.50, 0.70, 0.85]

list_dsigma_domega = [5.96, 4.70, 6.24, 8.37, 8.29, 7.81, 7.42, 5.01, 3.18,
                      2.80, 6.42, 6.39, 5.73, 7.29, 8.10, 6.58, 6.68, 2.16,
                      4.22, 3.50, 4.38, 5.37, 6.57, 6.70, 12.12, 9.70, 7.95,
                      2.21, 2.58, 2.85, 3.73, 3.03, 4.26, 8.40, 9.81, 0.50,
                      2.49, 1.55, 1.70, 1.71, 1.95, 4.01, 5.15, 9.26, 5.73]

list_stat_error = [0.57, 0.45, 0.54, 0.74, 0.67, 0.64, 0.76, 0.58, 1.00,
                   0.40, 0.60, 0.63, 0.48, 0.52, 0.60, 0.62, 0.59, 1.05,
                   0.49, 0.30, 0.51, 0.42, 0.48, 0.52, 0.78, 1.04, 1.10,
                   0.35, 0.33, 0.37, 0.31, 0.28, 0.43, 0.49, 1.06, 1.06,
                   0.28, 0.26, 0.18, 0.28, 0.19, 0.41, 0.45, 0.90, 1.21]

list_sys_error = [1.57, 0.66, 0.90, 1.26, 1.17, 1.26, 1.05, 0.7, 0.45,
                  0.93, 1.07, 1.32, 0.75, 1.04, 1.96, 1.16, 1.45, 0.26,
                  0.88, 0,44, 1.46, 1.10, 1.08, 1.01, 2.66, 1.46, 2.20,
                  0.37, 0.39, 0.40, 0.84, 0.86, 0.86, 1.40, 2.40, 1.90,
                  0.32, 0.20, 0.30, 0.44, 0.25, 1.00, 1.82, 1.29, 0.74]

list_e_gam = [w_to_egamma(w) for w in list_W]
list_t = [cosTheta_to_t(w, cosTheta) for w, cosTheta in zip(list_W, list_cosThetaCM)]
list_dsigma_dt = [dsigma_domega * 2*np.pi * t_over_cosTheta(w, cosTheta) for dsigma_domega, w, cosTheta in zip(list_dsigma_domega, list_W, list_cosThetaCM)]
list_clas_error = [sqrt(stat * stat + sys * sys) for stat, sys in zip(list_stat_error, list_sys_error)]

clas_df = pd.DataFrame()
clas_df['w'] = list_W
clas_df['cosThetaCM'] = list_cosThetaCM
clas_df['e_gam'] = list_e_gam
clas_df['t'] = list_t
clas_df['dsigma_domega'] = list_dsigma_domega
clas_df['dsigma_dt'] = list_dsigma_dt
clas_df['clas_error'] = list_clas_error

clas_df.to_csv('/work/halld/home/viducic/scripts/plotting/dnp_maui/clas_data.csv')

# print(clas_df)
clas_250 = clas_df[(clas_df['w'] == 2.35)]
clas_275 = clas_df[(clas_df['w'] == 2.45)]
clas_300 = clas_df[(clas_df['w'] == 2.55)]
clas_325 = clas_df[(clas_df['w'] == 2.65)]
clas_350 = clas_df[(clas_df['w'] == 2.75)]

# print(clas_250)

# gluex_7_df = pd.read_csv('cs_dataframe_7.csv')
# gluex_8_df = pd.read_csv('cs_dataframe_8.csv')
# gluex_9_df = pd.read_csv('cs_dataframe_9.csv')
# gluex_10_df = pd.read_csv('cs_dataframe_10.csv')

# gluex_8_df['acceptance'] = [0.002214, 0.002216, 0.002384, 0.002338, 0.002213, 0.002364, 0.002587, 0.002421, 0.001853, 0.001882, 0.001647]
# gluex_9_df['acceptance'] = [0.002417, 0.002489, 0.002532, 0.002344, 0.002728, 0.002455, 0.002208, 0.002204, 0.002450, 0.002161, 0.002133]

# gluex_8_df['yield'] = [635.333867, 555.083820, 489.691353, 419.347608, 635.462639, 566.107510, 334.218194, 212.526919, 138.599223, 210.110430, 118.737893]
# gluex_9_df['yield'] = [624.338253, 557.093599, 476.607482, 361.240174, 569.031236, 360.780601, 308.491354, 205.882647, 112.896585, 175.463157, 77.242692]

# gluex_7_df['acy'] = gluex_7_df['yield'] / (gluex_7_df['acceptance'] * gluex_7_df['bin_width'] * 100000)
# gluex_8_df['acy'] = gluex_8_df['yield'] / (gluex_8_df['acceptance'] * gluex_8_df['bin_width']* 100000)
# gluex_9_df['acy'] = gluex_9_df['yield'] / (gluex_9_df['acceptance'] * gluex_9_df['bin_width']* 100000)
# gluex_10_df['acy'] = gluex_10_df['yield'] / (gluex_10_df['acceptance'] * gluex_10_df['bin_width'] * 100000)

# gluex_7_df['error'] = gluex_7_df['acy'] * gluex_7_df['yield_percent_error'] / 100
# gluex_8_df['error'] = gluex_8_df['acy'] * gluex_8_df['yield_percent_error'] / 100
# gluex_9_df['error'] = gluex_9_df['acy'] * gluex_9_df['yield_percent_error'] / 100
# gluex_10_df['error'] = gluex_10_df['acy'] * gluex_10_df['yield_percent_error'] / 100

# gluex_8_df.drop(gluex_8_df.index[-1], inplace=True)
# gluex_9_df.drop(gluex_9_df.index[-1], inplace=True)

# theory_filename8 = '/Users/tylerviducic/research/gluex/theory_predictions/t-slope-8GeVnew.dat'
# theory_filename9 = '/Users/tylerviducic/research/gluex/theory_predictions/t-slope-9GeVnew.dat'
# theory_df8 = pd.read_csv(theory_filename8, delim_whitespace=True)
# theory_df9 = pd.read_csv(theory_filename9, delim_whitespace=True)
# theory_df8.columns = ['minus_t', 'diff_cs']
# theory_df9.columns = ['minus_t', 'diff_cs']

# print(gluex_9_df)
# print(theory_df9[theory_df9['minus_t'] == 0.45])
# norm_factor = 20.858916/650.626283 

fig = plt.figure()
ax1 = fig.add_subplot(111)
# ax2 = fig.add_subplot(111)
# ax1.errorbar(clas_250['t'], clas_250['dsigma_domega'], yerr=clas_250['clas_error'], label='2.50 GeV', marker='o', color='lightcoral')
ax1.errorbar(clas_275['t'], clas_275['dsigma_domega'], yerr=clas_275['clas_error'], label='2.75 GeV', marker='o', color='red')
ax1.errorbar(clas_300['t'], clas_300['dsigma_domega'], yerr=clas_300['clas_error'],label='3.00 GeV', marker='*', color='brown')
ax1.errorbar(clas_275['t'], clas_275['dsigma_dt'], yerr=clas_275['clas_error'], label='2.75 GeV', marker='o', color='red')
ax1.errorbar(clas_300['t'], clas_300['dsigma_dt'], yerr=clas_300['clas_error'],label='3.00 GeV', marker='*', color='brown')
# ax1.errorbar(clas_325['t'], clas_325['dsigma_domega'], yerr=clas_325['clas_error'],label='3.25 GeV', marker='o', color='maroon')
# ax1.errorbar(clas_350['t'], clas_350['dsigma_domega'], yerr=clas_350['clas_error'],label='3.50 GeV', marker='o', color='orangered')
# ax1.errorbar(gluex_7_df['t'], gluex_7_df['acy'], yerr=gluex_7_df['error'], label='7.0 GeV', marker='o', color='cornflowerblue')
# ax1.errorbar(gluex_8_df['t'], gluex_8_df['acy'], yerr=gluex_8_df['error'], label='8.0 GeV', marker='o', color='midnightblue')
# ax1.errorbar(gluex_9_df['t'], gluex_9_df['acy'], yerr=gluex_9_df['error'], label='9.0 GeV', marker='o', color='blue')
# ax1.errorbar(gluex_10_df['t'], gluex_10_df['acy'], yerr=gluex_10_df['error'], label='10.0 GeV', marker='o', color='slateblue')
# ax1.scatter(theory_df8['minus_t'], theory_df8['diff_cs'].multiply(norm_factor), marker='*' ,color='limegreen', s=3,label='8.0 GeV theory')
# ax1.scatter(theory_df9['minus_t'], theory_df9['diff_cs'].multiply(norm_factor), marker='+' ,color='darkgreen', label='9.0 GeV theory')
ax1.set_xlim([0.1, 2.0])
# ax1.set_ylim([0, 15])
# ax2.set_xlim([0.1, 1.5])
# ax2.set_ylim([0, 60])
# ax1.set_yscale('log')
ax1.legend()

plt.savefig('clas_vs_t.png')
# plt.show()
