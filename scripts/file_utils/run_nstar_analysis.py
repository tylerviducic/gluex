from my_library.flat_analysis import run_analysis
from my_library.constants import ALLOWED_NSTAR_MASSES

for mass in ALLOWED_NSTAR_MASSES:
    print(f'running analysis for nstar({mass})')
    run_analysis('pimkpks', 'spring', 'nstar', nstar_mass=mass)