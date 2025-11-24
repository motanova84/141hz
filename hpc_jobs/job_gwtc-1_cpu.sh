#!/bin/bash
#SBATCH --job-name=gwtc-1_141hz
#SBATCH --partition=normal
#SBATCH --time=08:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --array=1-11
#SBATCH --output=results/hpc_output/gwtc-1_141hz_%A_%a.out
#SBATCH --error=results/hpc_output/gwtc-1_141hz_%A_%a.err

# Get event name from array
EVENT=$(sed -n "${SLURM_ARRAY_TASK_ID}p" results/hpc_output/events_list.txt)

echo "Processing event: $EVENT"
echo "Array task ID: $SLURM_ARRAY_TASK_ID"
echo "Job ID: $SLURM_JOB_ID"

# Execute analysis
# Execute analysis
python scripts/example_optimized_analysis.py --events $EVENT --output-dir results/hpc_output

echo "Completed: $EVENT"
