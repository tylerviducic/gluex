import os

directories_pimkpks = {
    "spring": "spring_2018",
    "fall": "fall_2018",
    "2017": "2017"
}

filenames_pimkpks = {
    "spring": "2018_spring",
    "fall": "2018_fall",
    "2017": "2017"
}

runfile = '/work/halld/home/viducic/mc/analysis/pimkpks/RunF1Phasespace_KsKpPim_CorrectRF.C'

def run_selector_macro(run_period: str):
    top_dir =  '/lustre19/expphy/volatile/halld/home/viducic/pimkpks_mc/phasespace/tree_pimkpks__ks_pippim__B4_M16/'
    print(f"RUNNING DSELECTOR FOR PI+K-Ks OVER {run_period.upper()} PHASESPACE MC")
    filepath_for_selector = f'{top_dir}{directories_pimkpks[run_period]}/*'
    ds_command = f"root -l -b -q \'{runfile}(\"{filepath_for_selector}\")\'"
    print(ds_command)
    os.system(ds_command)


def rename_file(run_period: str):
    outfile =  '/work/halld/home/viducic/data/pimkpks/mc/phasespace/pimkpks_flat_bestX2.root'
    mv_command = f'mv {outfile} /work/halld/home/viducic/data/pimkpks/mc/phasespace/pimkpks_flat_bestX2_{filenames_pimkpks[run_period]}.root'
    print(mv_command)
    os.system(mv_command)


if __name__ == "__main__":
    for run_period in directories_pimkpks:
        run_selector_macro(run_period)
        rename_file(run_period)