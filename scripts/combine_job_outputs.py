# combine the DSelector outputs from the farm 

import os
import glob

def mv_current_to_old(file):
    command = "mv " + file + " old"
    os.system(command)

def add_histograms():
    base_command = "hadd /w/halld-scshelf2101/home/viducic/selector_output/f1/"

    os.system(base_command + "pipkmks_2018_fall.root /lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pipkmks/f1_pipkmks/f1_pipkmks_05*")
    os.system(base_command + "pipkmks_2018_spring.root /lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pipkmks/f1_pipkmks/f1_pipkmks_04*")
    os.system(base_command + "pipkmks_2018_full.root /w/halld-scshelf2101/home/viducic/selector_output/f1/pipkmks_2018_fall.root /w/halld-scshelf2101/home/viducic/selector_output/f1/pipkmks_2018_spring.root")
  #  os.system(base_command + "pipkmks_2019_fall.root /lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pipkmks/f1_pipkmks/f1_pipkmks_07*")

    os.system(base_command + "flat_pipkmks_2018_fall.root /lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pipkmks/flat_f1_pipkmks/flat_f1_pipkmks_05*")
    os.system(base_command + "flat_pipkmks_2018_spring.root /lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pipkmks/flat_f1_pipkmks/flat_f1_pipkmks_04*")
    os.system(base_command + "flat_pipkmks_2018_full.root /w/halld-scshelf2101/home/viducic/selector_output/f1/flat_pipkmks_2018_fall.root /w/halld-scshelf2101/home/viducic/selector_output/f1/flat_pipkmks_2018_spring.root")
   # os.system(base_command + "flat_pipkmks_2019_fall.root /lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pipkmks/flat_f1_pipkmks/flat_f1_pipkmks_07*")
    
    os.system(base_command + "pimkpks_2018_fall.root /lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pimkpks/f1_pimkpks/f1_pimkpks_05*")
    os.system(base_command + "pimkpks_2018_spring.root /lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pimkpks/f1_pimkpks/f1_pimkpmks_04*")
    os.system(base_command + "pimkpks_2017.root /lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pimkpks/f1_pimkpks/f1_pimkpks_03*")
   # os.system(base_command + "pimkpks_2019_fall.root /lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pimkpks/f1_pimkpks/f1_pimkpks_07*")
    os.system(base_command + "pimkpks_2018_full.root /w/halld-scshelf2101/home/viducic/selector_output/f1/pimkpks_2018_fall.root /w/halld-scshelf2101/home/viducic/selector_output/f1/pimkpks_2018_spring.root")
    
    os.system(base_command + "flat_pimkpks_2018_fall.root /lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pimkpks/flat_f1_pimkpks/flat_f1_pimkpks_05*")
    os.system(base_command + "flat_pimkpks_2018_spring.root /lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pimkpks/flat_f1_pimkpks/flat_f1_pimkpmks_04*")
    os.system(base_command + "flat_pimkpks_2017.root /lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pimkpks/flat_f1_pimkpks/flat_f1_pimkpks_03*")
   # os.system(base_command + "flat_pimkpks_2019_fall.root /lustre19/expphy/volatile/halld/home/viducic/selector_output/f1_pimkpks/flat_f1_pimkpks/flat_f1_pimkpks_07*")
    os.system(base_command + "flat_pimkpks_2018_full.root /w/halld-scshelf2101/home/viducic/selector_output/f1/flat_pimkpks_2018_fall.root /w/halld-scshelf2101/home/viducic/selector_output/f1/flat_pimkpks_2018_spring.root")

print("Starting workflow")

print("Moving old outputs to /old")
old_files = glob.glob("/w/halld-scshelf2101/home/viducic/selector_output/f1/*")
for file in old_files:
    mv_current_to_old(file)

print("Adding new outputs")
add_histograms()

print("Files added. Workflow complete")
