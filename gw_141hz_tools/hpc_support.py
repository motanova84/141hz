#!/usr/bin/env python3
"""
HPC and Cloud Computing Support
================================

Utilities for distributed computing on HPC clusters and cloud platforms.

Features:
- Dask distributed computation
- Slurm job submission
- Multi-event batch processing for GWTC-3/GWTC-4
- Resource management and monitoring

Usage:
    from gw_141hz_tools.hpc_support import HPCManager
    
    manager = HPCManager()
    results = manager.process_gwtc_catalog(catalog='GWTC-3', use_dask=True)
"""

import numpy as np
import json
import os
from typing import List, Dict, Any, Optional, Callable
import subprocess
import warnings

# Try to import Dask
try:
    import dask
    import dask.array as da
    from dask.distributed import Client, LocalCluster
    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False


class HPCManager:
    """
    Manager for HPC and cloud-based distributed processing.
    
    Parameters
    ----------
    use_dask : bool, optional
        Use Dask for distributed computing (default: False)
    n_workers : int, optional
        Number of Dask workers (default: 4)
    threads_per_worker : int, optional
        Threads per worker (default: 2)
    """
    
    def __init__(
        self,
        use_dask: bool = False,
        n_workers: int = 4,
        threads_per_worker: int = 2
    ):
        self.use_dask = use_dask and DASK_AVAILABLE
        self.n_workers = n_workers
        self.threads_per_worker = threads_per_worker
        self.client = None
        
        if use_dask and not DASK_AVAILABLE:
            warnings.warn(
                "Dask requested but not available. "
                "Install with: pip install dask distributed",
                UserWarning
            )
            self.use_dask = False
        
        if self.use_dask:
            self._setup_dask()
        
        print(f"HPC Manager initialized:")
        print(f"  - Dask: {'✓ ' + str(n_workers) + ' workers' if self.use_dask else '✗'}")
    
    def _setup_dask(self) -> None:
        """Initialize Dask cluster."""
        try:
            # Check if scheduler address is provided via environment
            scheduler_address = os.environ.get('DASK_SCHEDULER_ADDRESS')
            
            if scheduler_address:
                # Connect to existing cluster
                print(f"Connecting to Dask scheduler: {scheduler_address}")
                self.client = Client(scheduler_address)
            else:
                # Create local cluster
                print(f"Creating local Dask cluster...")
                cluster = LocalCluster(
                    n_workers=self.n_workers,
                    threads_per_worker=self.threads_per_worker,
                    processes=True,
                    memory_limit='auto'
                )
                self.client = Client(cluster)
            
            print(f"  Dashboard: {self.client.dashboard_link}")
            
        except Exception as e:
            warnings.warn(f"Failed to setup Dask: {e}", UserWarning)
            self.use_dask = False
            self.client = None
    
    def process_event_batch(
        self,
        events: List[str],
        process_func: Callable,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Process multiple GW events in parallel.
        
        Parameters
        ----------
        events : list of str
            List of event names (e.g., ['GW150914', 'GW151226'])
        process_func : callable
            Function to process each event: func(event_name, **kwargs) -> dict
        **kwargs
            Additional arguments passed to process_func
            
        Returns
        -------
        results : list of dict
            Processing results for each event
        """
        if self.use_dask:
            # Distributed processing with Dask
            futures = []
            for event in events:
                future = self.client.submit(process_func, event, **kwargs)
                futures.append(future)
            
            # Gather results
            results = self.client.gather(futures)
        else:
            # Sequential processing
            results = [process_func(event, **kwargs) for event in events]
        
        return results
    
    def process_gwtc_catalog(
        self,
        catalog: str = 'GWTC-3',
        analysis_func: Optional[Callable] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process entire GWTC catalog.
        
        Parameters
        ----------
        catalog : str, optional
            Catalog name: 'GWTC-1', 'GWTC-2', 'GWTC-3', 'GWTC-4'
        analysis_func : callable, optional
            Analysis function (default: simple 141.7 Hz detection)
        **kwargs
            Additional arguments for analysis
            
        Returns
        -------
        results : dict
            Catalog-wide analysis results
        """
        # Get event list for catalog
        events = self._get_catalog_events(catalog)
        
        print(f"\nProcessing {catalog} catalog: {len(events)} events")
        print("="*60)
        
        if analysis_func is None:
            analysis_func = self._default_analysis
        
        # Process all events
        event_results = self.process_event_batch(events, analysis_func, **kwargs)
        
        # Aggregate results
        results = {
            'catalog': catalog,
            'n_events': len(events),
            'events': events,
            'individual_results': event_results,
            'summary': self._aggregate_results(event_results)
        }
        
        return results
    
    def _get_catalog_events(self, catalog: str) -> List[str]:
        """Get list of events in catalog."""
        catalogs = {
            'GWTC-1': [
                'GW150914', 'GW151012', 'GW151226',
                'GW170104', 'GW170608', 'GW170729',
                'GW170809', 'GW170814', 'GW170817',
                'GW170818', 'GW170823'
            ],
            'GWTC-2': [
                'GW190403', 'GW190408', 'GW190412',
                'GW190413', 'GW190421', 'GW190424',
                'GW190425', 'GW190426', 'GW190512',
                'GW190513', 'GW190514', 'GW190517',
                'GW190519', 'GW190521', 'GW190527',
                'GW190602', 'GW190620', 'GW190630',
                'GW190701', 'GW190706', 'GW190707',
                'GW190708', 'GW190719', 'GW190720',
                'GW190725', 'GW190727', 'GW190728',
                'GW190731', 'GW190803', 'GW190814',
                'GW190828', 'GW190909', 'GW190910',
                'GW190915', 'GW190916', 'GW190917',
                'GW190924', 'GW190925', 'GW190926',
                'GW190929', 'GW190930'
            ],
            'GWTC-3': [
                # Subset of GWTC-3 events (O3b)
                'GW191103', 'GW191105', 'GW191109',
                'GW191113', 'GW191126', 'GW191127',
                'GW191129', 'GW191204', 'GW191215',
                'GW191216', 'GW191219', 'GW191222',
                'GW200105', 'GW200112', 'GW200115',
                'GW200128', 'GW200129', 'GW200202',
                'GW200208', 'GW200209', 'GW200210',
                'GW200216', 'GW200219', 'GW200220',
                'GW200224', 'GW200225', 'GW200302',
                'GW200306', 'GW200308', 'GW200311',
                'GW200316', 'GW200322'
            ],
            'GWTC-4': [
                # Placeholder for GWTC-4 (not yet released)
                # Will be updated when catalog is published
            ]
        }
        
        if catalog not in catalogs:
            raise ValueError(f"Unknown catalog: {catalog}")
        
        return catalogs[catalog]
    
    def _default_analysis(
        self,
        event: str,
        target_freq: float = 141.7,
        **kwargs
    ) -> Dict[str, Any]:
        """Default analysis function (placeholder)."""
        return {
            'event': event,
            'target_freq': target_freq,
            'status': 'placeholder',
            'note': 'Real analysis would download and process data'
        }
    
    def _aggregate_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate individual event results."""
        return {
            'n_processed': len(results),
            'n_success': sum(1 for r in results if r.get('status') == 'success'),
            'n_placeholder': sum(1 for r in results if r.get('status') == 'placeholder')
        }
    
    def shutdown(self) -> None:
        """Shutdown Dask cluster."""
        if self.client is not None:
            self.client.close()
            self.client = None


class SlurmJobGenerator:
    """
    Generate Slurm job submission scripts for HPC clusters.
    
    Parameters
    ----------
    partition : str, optional
        Slurm partition name (default: 'normal')
    time_limit : str, optional
        Job time limit (default: '24:00:00')
    memory : str, optional
        Memory per node (default: '64G')
    nodes : int, optional
        Number of nodes (default: 1)
    tasks_per_node : int, optional
        Tasks per node (default: 1)
    cpus_per_task : int, optional
        CPUs per task (default: 8)
    gpu : bool, optional
        Request GPU resources (default: False)
    """
    
    def __init__(
        self,
        partition: str = 'normal',
        time_limit: str = '24:00:00',
        memory: str = '64G',
        nodes: int = 1,
        tasks_per_node: int = 1,
        cpus_per_task: int = 8,
        gpu: bool = False
    ):
        self.partition = partition
        self.time_limit = time_limit
        self.memory = memory
        self.nodes = nodes
        self.tasks_per_node = tasks_per_node
        self.cpus_per_task = cpus_per_task
        self.gpu = gpu
    
    def generate_job_script(
        self,
        job_name: str,
        script_path: str,
        output_dir: str,
        python_script: str,
        arguments: str = '',
        modules: Optional[List[str]] = None,
        conda_env: Optional[str] = None,
        additional_commands: Optional[List[str]] = None
    ) -> str:
        """
        Generate Slurm job submission script.
        
        Parameters
        ----------
        job_name : str
            Job name
        script_path : str
            Path to save the job script
        output_dir : str
            Directory for output files
        python_script : str
            Python script to execute
        arguments : str, optional
            Command-line arguments
        modules : list of str, optional
            Modules to load
        conda_env : str, optional
            Conda environment to activate
        additional_commands : list of str, optional
            Additional shell commands
            
        Returns
        -------
        script_path : str
            Path to generated script
        """
        os.makedirs(output_dir, exist_ok=True)
        
        script_content = f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --partition={self.partition}
#SBATCH --time={self.time_limit}
#SBATCH --nodes={self.nodes}
#SBATCH --ntasks-per-node={self.tasks_per_node}
#SBATCH --cpus-per-task={self.cpus_per_task}
#SBATCH --mem={self.memory}
#SBATCH --output={output_dir}/{job_name}_%j.out
#SBATCH --error={output_dir}/{job_name}_%j.err
"""
        
        if self.gpu:
            script_content += "#SBATCH --gres=gpu:1\n"
        
        script_content += "\n"
        
        # Module loading
        if modules:
            for module in modules:
                script_content += f"module load {module}\n"
            script_content += "\n"
        
        # Conda environment
        if conda_env:
            script_content += f"source activate {conda_env}\n\n"
        
        # Additional commands
        if additional_commands:
            for cmd in additional_commands:
                script_content += f"{cmd}\n"
            script_content += "\n"
        
        # Main execution
        script_content += f"""# Execute analysis
echo "Job started at $(date)"
echo "Running on node: $(hostname)"
echo "Working directory: $(pwd)"

python {python_script} {arguments}

echo "Job completed at $(date)"
"""
        
        # Write script
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(script_path, 0o755)
        
        print(f"Generated Slurm job script: {script_path}")
        return script_path
    
    def generate_array_job(
        self,
        job_name: str,
        script_path: str,
        output_dir: str,
        python_script: str,
        events: List[str],
        **kwargs
    ) -> str:
        """
        Generate Slurm array job for multiple events.
        
        Parameters
        ----------
        job_name : str
            Base job name
        script_path : str
            Path to save the job script
        output_dir : str
            Directory for output files
        python_script : str
            Python script to execute
        events : list of str
            List of event names
        **kwargs
            Additional arguments for generate_job_script
            
        Returns
        -------
        script_path : str
            Path to generated script
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Create events list file
        events_file = os.path.join(output_dir, 'events_list.txt')
        with open(events_file, 'w') as f:
            f.write('\n'.join(events))
        
        # Generate array job script
        array_range = f"1-{len(events)}"
        
        script_content = f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --partition={self.partition}
#SBATCH --time={self.time_limit}
#SBATCH --nodes={self.nodes}
#SBATCH --ntasks-per-node={self.tasks_per_node}
#SBATCH --cpus-per-task={self.cpus_per_task}
#SBATCH --mem={self.memory}
#SBATCH --array={array_range}
#SBATCH --output={output_dir}/{job_name}_%A_%a.out
#SBATCH --error={output_dir}/{job_name}_%A_%a.err
"""
        
        if self.gpu:
            script_content += "#SBATCH --gres=gpu:1\n"
        
        script_content += f"""
# Get event name from array
EVENT=$(sed -n "${{SLURM_ARRAY_TASK_ID}}p" {events_file})

echo "Processing event: $EVENT"
echo "Array task ID: $SLURM_ARRAY_TASK_ID"
echo "Job ID: $SLURM_JOB_ID"

# Execute analysis
# Execute analysis
python {python_script} --events $EVENT --output-dir {output_dir}

echo "Completed: $EVENT"
"""
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        os.chmod(script_path, 0o755)
        
        print(f"Generated Slurm array job script: {script_path}")
        print(f"  Events: {len(events)}")
        print(f"  Array range: {array_range}")
        
        return script_path
    
    def submit_job(self, script_path: str) -> Optional[str]:
        """
        Submit job to Slurm.
        
        Parameters
        ----------
        script_path : str
            Path to job script
            
        Returns
        -------
        job_id : str or None
            Slurm job ID if successful
        """
        try:
            result = subprocess.run(
                ['sbatch', script_path],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Extract job ID from output
            output = result.stdout.strip()
            job_id = output.split()[-1]
            
            print(f"Submitted job: {job_id}")
            return job_id
            
        except subprocess.CalledProcessError as e:
            print(f"Failed to submit job: {e}")
            return None
        except FileNotFoundError:
            print("Slurm not available (sbatch command not found)")
            return None


def create_hpc_examples() -> None:
    """Create example HPC job scripts."""
    print("\n" + "="*60)
    print("Creating HPC Example Scripts")
    print("="*60)
    
    output_dir = "hpc_jobs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Example 1: Single event analysis
    slurm = SlurmJobGenerator(
        partition='normal',
        time_limit='04:00:00',
        cpus_per_task=8,
        memory='32G'
    )
    
    slurm.generate_job_script(
        job_name='gw150914_141hz',
        script_path=f'{output_dir}/job_gw150914.sh',
        output_dir=output_dir,
        python_script='scripts/analizar_ringdown.py',
        arguments='--event GW150914 --freq 141.7',
        conda_env='gw_analysis'
    )
    
    # Example 2: GPU-accelerated analysis
    slurm_gpu = SlurmJobGenerator(
        partition='gpu',
        time_limit='02:00:00',
        cpus_per_task=8,
        memory='64G',
        gpu=True
    )
    
    slurm_gpu.generate_job_script(
        job_name='gw_gpu_analysis',
        script_path=f'{output_dir}/job_gpu_analysis.sh',
        output_dir=output_dir,
        python_script='scripts/analisis_gw250114.py',
        arguments='--use-gpu --events GWTC-3',
        conda_env='gw_analysis',
        modules=['cuda/12.0', 'python/3.11']
    )
    
    # Example 3: Array job for GWTC-3
    gwtc3_events = [
        'GW191103', 'GW191105', 'GW191109', 'GW191113',
        'GW200105', 'GW200112', 'GW200115', 'GW200129'
    ]
    
    slurm.generate_array_job(
        job_name='gwtc3_141hz',
        script_path=f'{output_dir}/job_gwtc3_array.sh',
        output_dir=output_dir,
        python_script='scripts/analisis_gw250114.py',
        events=gwtc3_events
    )
    
    print(f"\nExample scripts created in {output_dir}/")
    print("To submit: sbatch hpc_jobs/job_*.sh")


if __name__ == "__main__":
    # Create example HPC scripts
    create_hpc_examples()
