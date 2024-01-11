import sys
import os
import pwd


def main():
    PARTITION = "priority"
    TIMELIMIT = "3:00:00"
    ENVIRONMENT = '/work/halld/home/viducic/scripts/file_utils/analysis_jobs_env.csh'
    LOG_DIR = '/farm_out/viducic/'
    NCORES=16

    with open('tempSlurm.txt', 'w') as slurmOut:
        slurmOut.write("#!/bin/csh \n")
        slurmOut.write("#SBATCH --nodes=1 \n")
        slurmOut.write("#SBATCH --ntasks=32 \n")
        slurmOut.write("#SBATCH --ntasks-per-core=1 \n")
        slurmOut.write("#SBATCH --threads-per-core=1 \n")
        slurmOut.write(f"#SBATCH --partition={PARTITION} \n")
        slurmOut.write(f"#SBATCH --mem=16GB \n")
        slurmOut.write(f"#SBATCH --time={TIMELIMIT} \n")
        slurmOut.write(f"#SBATCH --error={LOG_DIR}/analysis.err \n")
        slurmOut.write(f"#SBATCH --output={LOG_DIR}/analysis.out \n")
        slurmOut.write(f'#SBATCH --account=halld \n')
        slurmOut.write(f'source {ENVIRONMENT} \n')
        slurmOut.write(f'python3 /work/halld/home/viducic/scripts/file_utils/run_analysis_chain.py')

    command = 'sbatch tempSlurm.txt'
    os.system(command)
    os.remove('tempSlurm.txt')

if __name__ == "__main__":
    main()