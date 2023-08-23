import os

directories_pipkmks = {
    "spring": "spring_2018",
    "fall": "fall_2018",
    "2017": "2017"
}

def run_selector_macro(run_period: str):
    top_dir =  '/lustre19/expphy/volatile/halld/home/viducic/pipkmks_mc/signal/tree_pipkmks__ks_pippim__B4_M16/'
    for run_period in directories_pipkmks:
        print("RUNNING DSELECTOR FOR PI+K-Ks OVER {run_period}} SIGNAL MC")
        filepath_for_selector = f'{top_dir}{directories_pipkmks[run_period]}/*'
        ds_command = f'root -l -b RunF1MC_KsKmPip.C({filepath_for_selector})'
        os.system(ds_command)

def rename_file(run_period: str):
    outfile =  '/work/halld/home/viducic/data/pipkmks/mc/signal/pipkmks_flat_bestX2.root'
    command = f'mv outfile /work/halld/home/viducic/data/pipkmks/mc/signal/pipkmks_flat_bestX2_{directories_pipkmks[run_period]}.root'
    os.system(command)


if __name__ == "__main__":
    run_selector_macro("spring")
    rename_file("spring")
    run_selector_macro("fall")
    rename_file("fall")
    run_selector_macro("2017")
    rename_file("2017")