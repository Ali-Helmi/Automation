Setup Guide
Overview
This guide provides a comprehensive step-by-step process to set up the development environment for the Metasurface Design Automation project. Follow the instructions below to ensure smooth and error-free setup.

Step 1: Prerequisites
System Requirements
Operating System: Linux or Windows (recommended to use WSL for Windows)
Python Version: 3.7 or higher
Additional Software: Ansys HFSS (installed and accessible)
Required Packages
Make sure Python is installed, and the necessary packages will be installed via requirements.txt.

Step 2: Clone the Repository
Open your terminal and run the following command:

git clone https://github.com/Ali-Helmi/Automation.git
cd Automation
Step 3: Setting Up the Virtual Environment
Create and Activate Virtual Environment

python3 -m venv metasurface_env
source metasurface_env/bin/activate   # On Windows: metasurface_env\Scripts\activate
Install Dependencies

pip install --upgrade pip
pip install -r requirements.txt
Step 4: Configuring the System
Update Configuration Files
Simulation Settings:
Modify parameters in config/simulation_config.yaml to match your simulation needs (frequency range, boundary conditions, etc.).
Job Submission Settings:
Configure config/job_submission.yaml for your cluster settings (queue, nodes, job scripts).
Environmental Setup Script
Run the automated setup script:


bash scripts/setup_env.sh
This will create required directories, copy default configuration files if missing, and set up paths.

Step 5: Preparing the Simulation Environment
Load Necessary Software Modules
Ensure Ansys HFSS is properly installed and accessible:

module load hfss/2024
Check Python Modules
Verify that pyaedt is installed and can interact with HFSS by running a test script:

python -c "import pyaedt; print(pyaedt.__version__)"
Step 6: Running Example Scripts
Generating Design Files

python design_generator/generator.py --template design_generator/templates/template_1.json
Submitting Simulation Jobs

python job_manager/submitter.py --config config/job_submission.yaml
Collecting Output Data

python data_processor/parser.py --input ./simulation_outputs
Troubleshooting
Common Issues
Python version incompatibility: Ensure you are using Python 3.7 or higher.
Failed job submission: Verify job scripts in config/job_submission.yaml and check cluster access.
Checking System Logs
View logs located in ./logs for debugging any issues:

tail -f logs/output_<job_id>.log
Conclusion
Your environment should now be fully set up and ready to use. If you encounter any issues, refer to the troubleshooting section or reach out via the project's GitHub issues page.