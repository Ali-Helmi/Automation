import subprocess
import time
import os
import yaml

# Load configurations
with open("config/job_submission.yaml", "r") as f:
    config = yaml.safe_load(f)

CHECK_INTERVAL = config.get("check_interval", 60)  # Default to 60 seconds
MAX_RETRIES = config.get("max_retries", 3)

def check_job_status(job_id):
    """Check the status of a job using SLURM command 'squeue'."""
    result = subprocess.run(["squeue", "-j", str(job_id)], stdout=subprocess.PIPE)
    return "RUNNING" if job_id in result.stdout.decode() else "COMPLETED"

def resubmit_job(job_script):
    """Resubmit a job if it fails."""
    retries = 0
    while retries < MAX_RETRIES:
        print(f"Resubmitting job ({retries + 1}/{MAX_RETRIES})...")
        result = subprocess.run(["sbatch", job_script])
        if result.returncode == 0:
            print("Job resubmitted successfully.")
            return
        retries += 1
        time.sleep(10)

def monitor_jobs(job_list):
    """Monitor a list of job IDs and resubmit if necessary."""
    for job_script, job_id in job_list:
        status = check_job_status(job_id)
        if status != "COMPLETED":
            print(f"Job {job_id} failed or stopped. Attempting to resubmit.")
            resubmit_job(job_script)

def main():
    # Load job details from a file or API
    job_list = [
        # Example job entries
        ("job_manager/job_templates/slurm_template.sh", "12345"),
    ]

    while True:
        monitor_jobs(job_list)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
