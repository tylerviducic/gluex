import os

topdir_gluex1 = '/lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_{}_flat_bx2/{}_flat_bestX2/'
topdir_2019 = '/lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pipkmks_flat_bx2/pipkmks_flat_bestX2_unconstrained/'
target_path = '/work/halld/home/viducic/data/{}/data/bestX2/'


file_suffix = {
    3: '2017',
    4: '2018_spring',
    5: '2018_fall',
    7: '2019_unconstrained'
}

for channel in ['pipkmks', 'pimkpks']:
    for i in range(3, 8):
        if i not in file_suffix:
            continue
        if i == 7 and channel == 'pimkpks':
            continue

        filename = f'{channel}_flat_bestX2_{file_suffix[i]}.root'
        rm_command = f'rm {target_path.format(channel)}/{filename}'
        print('---')
        print('removing old file')
        print(rm_command)
        os.system(rm_command)

        if i < 7:
            topdir = topdir_gluex1.format(channel, channel)
            sources = f'{topdir}{channel}_flat_bestX2_0{i}*.root'
        else:
            topdir = topdir_2019
            sources = f'{topdir}{channel}_flat_bestX2_unconstrained_0{i}*.root'

        add_command = f'hadd {target_path.format(channel)}{filename} {sources}'
        print('adding new file')
        print(add_command)
        os.system(add_command)



