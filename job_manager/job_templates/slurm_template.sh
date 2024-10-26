#!/bin/bash
#SBATCH --job-name={job_name}          # Job name
#SBATCH --output={job_name}.out        # Standard output and error log
#SBATCH --nodes={nodes}                # Number of nodes
#SBATCH --ntasks-per-node={tasks_per_node}  # Tasks per node
#SBATCH --time={walltime}              # Walltime (HH:MM:SS)
#SBATCH --partition={partition}        # Partition name (optional)
#SBATCH --mail-type=END,FAIL           # Notifications for job done & fail
#SBATCH --mail-user={email}            # Your email address

# Load required modules (adjust as needed)
module load ansys/2023R2
module load python/3.8

# Navigate to the working directory
cd $SLURM_SUBMIT_DIR

# Run the simulation script using the generated design file
python3 simulate.py {design_file}

echo "Job {job_name} completed"
