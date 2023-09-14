import os


filepath = '/work/halld/home/viducic/data/{}/data/ver_test/{}_041000-041008_ver_{}.root'
outpath = '/work/halld/home/viducic/data/{}/data/ver_test/{}_flat_bestX2_ver_{}.root'
selector_path = '/work/halld/home/viducic/analysis/{}/RunVerTest.C'

versions = [16, 23]
channels = ['pipkmks', 'pimkpks']

for channel in channels:
    for version in versions:
        command = f'root -l -b -q \'{selector_path.format(channel)}("{filepath.format(channel, channel, version)}")\''
        print(command)
        os.system(command)
        mv_command = f'mv {channel}_flat_bestX2.root {outpath.format(channel, channel, version)}'
        print(mv_command)
        os.system(mv_command)