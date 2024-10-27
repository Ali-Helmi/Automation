#!/bin/bash
#PBS -N {job_name}              # Job name
#PBS -l nodes={nodes}:ppn={tasks_per_node}  # Nodes and tasks per node
#PBS -l walltime={walltime}     # Walltime (HH:MM:SS)
#PBS -o {job_name}.out          # Standard output file
#PBS -e {job_name}.err          # Error output file
#PBS -m abe                     # Send mail on abort, begin, end
#PBS -M {email}                 # Email address for notifications

cd $PBS_O_WORKDIR

# Load required modules
module load anaconda/3
module load ansys/2024

# Activate environment and run simulation
source activate metasurface_env
python simulate.py {design_file}
echo "Job {job_name} completed"
