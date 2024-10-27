# job_manager/submitter.py
# Purpose: Automate job submission to the supercomputer, utilizing settings from config/job_submission.yaml

import os
import subprocess
import yaml
from pathlib import Path

def load_config(config_path):
    """
    Loads job submission configuration from a YAML file.
    
    Args:
        config_path (str): Path to the job submission configuration file.
    
    Returns:
        dict: Configuration parameters.
    """
    config_path = Path(config_path)
    if not config_path.exists():
        print(f"Configuration file {config_path} not found.")
        return {}
    
    #with config_path.open('r') as file:
    #    return yaml.safe_load(file)
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def create_submission_script(config, job_name, design_file):
    """
    Creates a job submission script based on template and configuration.
    
    Args:
        config (dict): Job submission configuration parameters.
        job_name (str): Name of the job.
        design_file (str): Path to the design file to be simulated.
    
    Returns:
        str: Path to the generated job script.
    """
    # script_template = config.get('script_template', 'job_manager/job_templates/slurm_template.sh')
    # job_script = f"{job_name}.sh"
    
    # with open(script_template, 'r') as template:
    #     script_content = template.read()

    # # Replace placeholders in the template
    # script_content = script_content.replace("{job_name}", job_name)
    # script_content = script_content.replace("{design_file}", design_file)
    # script_content = script_content.replace("{nodes}", str(config['nodes']))
    # script_content = script_content.replace("{tasks_per_node}", str(config['tasks_per_node']))
    # script_content = script_content.replace("{walltime}", config['walltime'])
    
    # # Write the filled script
    # with open(job_script, 'w') as file:
    #     file.write(script_content)
    
    # print(f"Job script generated: {job_script}")
    # return job_script
    
    try:
        nodes = str(config.get('nodes', 1))
        tasks_per_node = str(config.get('tasks_per_node', 1))
        walltime = config.get('walltime', '01:00:00')
        template_file = Path(config.get('script_template', 'job_templates/slurm_template.sh'))

        with template_file.open('r') as template:
            script_content = template.read().replace("{job_name}", job_name) \
                                            .replace("{design_file}", design_file) \
                                            .replace("{nodes}", nodes) \
                                            .replace("{tasks_per_node}", tasks_per_node) \
                                            .replace("{walltime}", walltime)

        job_script = Path(f"{job_name}.sh")
        job_script.write_text(script_content)
        print(f"Job script generated: {job_script}")
        return job_script
    except KeyError as e:
        print(f"Configuration missing key: {e}")

def submit_job(script_path):
    """
    Submits a job to the cluster using the job script.
    
    Args:
        script_path (str): Path to the job script.
    
    Returns:
        str: Submission status.
    """
    try:
        result = subprocess.run(['sbatch', script_path], capture_output=True, text=True, check=True)
        print(f"Job submitted: {result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error submitting job: {e.stderr.strip()}")
        return None

def batch_submit_jobs(config_path, design_files):
    """
    Batch submits multiple design files to the cluster.
    
    Args:
        config_path (str): Path to job submission configuration.
        design_files (list): List of design file paths to be simulated.
    """
    config = load_config(config_path)
    for i, design_file in enumerate(design_files):
        job_name = f"{config['job_prefix']}_simulation_{i+1}"
        script_path = create_submission_script(config, job_name, design_file)
        submit_status = submit_job(script_path)
        if submit_status:
            print(f"Successfully submitted: {job_name}")
        else:
            print(f"Failed to submit: {job_name}")
