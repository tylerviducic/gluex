import os


runfile_datafile_dict = {
    '/work/halld/home/viducic/analysis/pipkmks/RunVerTest16.C': '/work/halld/home/viducic/data/pipkmks/data/ver_test/pipkmks_041000-041008_ver_16.root',
    '/work/halld/home/viducic/analysis/pipkmks/RunVerTest23.C': '/work/halld/home/viducic/data/pipkmks/data/ver_test/pipkmks_041000-041008_ver_23.root',
    '/work/halld/home/viducic/analysis/pimkpks/RunVerTest16.C': '/work/halld/home/viducic/data/pimkpks/data/ver_test/pimkpks_041000-041008_ver_16.root',
    '/work/halld/home/viducic/analysis/pimkpks/RunVerTest23.C': '/work/halld/home/viducic/data/pimkpks/data/ver_test/pimkpks_041000-041008_ver_23.root'
}

result_filenames = ['pipkmks_v16', 'pipkmks_v23', 'pimkpks_v16', 'pimkpks_v23']
outfiles = ['pipkmks_flat_bestX2.root', 'pipkmks_flat_bestX2_ver23.root', 'pimkpks_flat_bestX2.root', 'pimkpks_flat_bestX2_ver23.root']

#this is a shitty hack. 
for i, runfile in enumerate(runfile_datafile_dict.keys()):
    command = f'root -l -b -q \'{runfile}("{runfile_datafile_dict[runfile]}")\''
    print(command)
    os.system(command)
    outpath = f'/work/halld/home/viducic/data/{outfiles[i].split("_")[0]}/data/ver_test/{result_filenames[i]}.root'
    mv_command = f'mv {outfiles[i]} {outpath}'
    print(mv_command)
    os.system(mv_command)