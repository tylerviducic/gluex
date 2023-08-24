import os

directories_pipkmks = {
    "spring": "spring_2018",
    "fall": "fall_2018",
    "2017": "2017"
}


def run_selector_macro(run_period: str):
    top_dir =  '/lustre19/expphy/volatile/halld/home/viducic/pipkmks_mc/signal/tree_pipkmks__ks_pippim__B4_M16/'
    print(f"RUNNING DSELECTOR FOR PI+K-Ks OVER {run_period.upper()} SIGNAL MC")
    filepath_for_selector = f'{top_dir}{directories_pipkmks[run_period]}/*'
    ds_command = f"root -l -b -q \'RunF1MC_KsKmPip.C(\"{filepath_for_selector}\")\'"
    print(ds_command)
    os.system(ds_command)


def rename_file(run_period: str):
    outfile =  '/work/halld/home/viducic/data/pipkmks/mc/signal/pipkmks_flat_bestX2.root'
    mv_command = f'mv {outfile} /work/halld/home/viducic/data/pipkmks/mc/signal/pipkmks_flat_bestX2_{directories_pipkmks[run_period]}.root'
    print(mv_command)
    os.system(mv_command)


if __name__ == "__main__":
    for run_period in directories_pipkmks:
        run_selector_macro(run_period)
        rename_file(run_period)