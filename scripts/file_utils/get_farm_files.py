# python script for pulling files from farm

import pysftp
import getpass

hostname = 'ftp.jlab.org'
my_username = 'viducic'
my_password = getpass.getpass("Enter Password:")
print("Getting Files...")

files_to_get =  [
                #'/w/halld-scifs17exp/home/viducic/selector_output/pi0_fall.root', 
                #'/w/halld-scifs17exp/home/viducic/selector_output/pi0_spring.root',
                #'/w/halld-scifs17exp/home/viducic/selector_output/pi0_premakoff.root',
                # '/w/halld-scifs17exp/home/viducic/selector_output/f1_analysis.root',
                # '/w/halld-scifs17exp/home/viducic/selector_output/f1_analysis_debug.root',
                # '/w/halld-scifs17exp/home/viducic/selector_output/f1_pimkpks.root',
                # '/w/halld-scifs17exp/home/viducic/selector_output/f1_pipkmks_2018_full.root',
                # '/w/halld-scifs17exp/home/viducic/selector_output/f1_pimkpks_2018_full.root'
                #'/w/halld-scifs17exp/home/viducic/selector_output/pi0_2018_full.root'
                "flat_pimkpks_2017.root",
                "flat_pimkpks_2018_spring.root",
                "flat_pipkmks_2018_spring.root",
                "pimkpks_2018_full.root",
                "pipkmks_2018_full.root",
                "flat_pimkpks_2018_fall.root",
                "flat_pipkmks_2018_fall.root",
                "pimkpks_2017.root",
                "pimkpks_2018_spring.root",
                "pipkmks_2018_spring.root",
                "flat_pimkpks_2018_full.root",
                "flat_pipkmks_2018_full.root",
                "pimkpks_2018_fall.root",
                "pipkmks_2018_fall.root"
                ]



# remote_plots = '/w/halld-scifs17exp/home/viducic/plots/fall_spring_compare'

selector_target = '/Users/tylerviducic/research/gluex/selector_output/'
# plots_target = '/home/tylerviducic/research/gluex/plots/fall_spring_comparison'
remote_path = '/work/halld/home/viducic/selector_output/f1/'

with pysftp.Connection(host=hostname, username=my_username, password=my_password) as sftp:
    for file in files_to_get:
        sftp.get(remotepath=(remote_path + file), localpath=(selector_target + file), callback=None)
    
    #sftp.get_d(remote_plots, plots_target)

print('done')
    