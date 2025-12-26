#!/bin/bash
#SBATCH --job-name=GW150914_141hz
#SBATCH --partition=normal
#SBATCH --time=08:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --output=results/hpc_output/GW150914_141hz_%j.out
#SBATCH --error=results/hpc_output/GW150914_141hz_%j.err

module load python/3.11

source activate gw_analysis

# Execute analysis
echo "Job started at $(date)"
echo "Running on node: $(hostname)"
echo "Working directory: $(pwd)"

python scripts/example_optimized_analysis.py --events GW150914 

echo "Job completed at $(date)"
