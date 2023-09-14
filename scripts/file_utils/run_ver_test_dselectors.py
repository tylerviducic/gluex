import os


runfile_datafile_dict = {
    '/work/halld/home/viducic/analysis/pipkmks/RunVerTest16.C': '/work/halld/home/viducic/data/pipkmks/data/ver_test/pipkmks_041000-041008_ver_16.root',
    '/work/halld/home/viducic/analysis/pipkmks/RunVerTest23.C': '/work/halld/home/viducic/data/pipkmks/data/ver_test/pipkmks_041000-041008_ver_23.root',
    '/work/halld/home/viducic/analysis/pimkpks/RunVerTest16.C': '/work/halld/home/viducic/data/pimkpks/data/ver_test/pimkpks_041000-041008_ver_16.root',
    '/work/halld/home/viducic/analysis/pimkpks/RunVerTest23.C': '/work/halld/home/viducic/data/pimkpks/data/ver_test/pimkpks_041000-041008_ver_23.root'
}


for runfile in runfile_datafile_dict:
    command = f'root -l -b -q \'{runfile}("{runfile_datafile_dict[runfile]}")\''
    print(command)
    os.system(command)