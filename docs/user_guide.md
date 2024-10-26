User Guide
Overview
This guide provides instructions on how to use the Metasurface Design Automation project. It covers generating design files, submitting simulation jobs, and processing output data. Each section includes examples to simplify the process.

1. Generating Metasurface Design Files
Step 1: Prepare Template
Edit or create design templates in design_generator/templates/. Sample templates are available for reference.
Step 2: Run the Generator Script

python design_generator/generator.py --template design_generator/templates/template_1.json
Options:
--template: Specify the template file to use.
--randomize: Add this option to generate random designs.
Example:
python design_generator/generator.py --template design_generator/templates/template_1.json --randomize
2. Submitting Simulation Jobs
Step 1: Configure Job Submission
Adjust settings in config/job_submission.yaml to match your cluster environment.
Step 2: Use Job Submission Script

python job_manager/submitter.py --config config/job_submission.yaml
Monitor Jobs:
Jobs can be tracked using the monitor.py script:

python job_manager/monitor.py --track
3. Processing Simulation Output Data
Step 1: Parse Output Files
python data_processor/parser.py --input ./simulation_outputs
Options:
--input: Directory where simulation outputs are stored.
Step 2: Aggregate Data for ML

python data_processor/aggregator.py --source ./processed_data
Example:

python data_processor/parser.py --input ./simulation_outputs
python data_processor/aggregator.py --source ./processed_data
4. Training Machine Learning Models
Step 1: Prepare Dataset
Ensure processed data is ready in the dataset directory.

Step 2: Start Training

python machine_learning/model_trainer.py --dataset ./datasets/training_data.h5
Options:
--model: Specify model type (e.g., cnn, vae).
Monitor Training Progress:
Logs will be stored in ./logs.
Troubleshooting
Failed Job Submissions:

Check config/job_submission.yaml for correct cluster settings.
Ensure network connectivity to the cluster.
Unexpected Script Errors:

Refer to ./logs for detailed error logs.
Make sure all dependencies are installed.
Additional Support
For more information, refer to the Setup Guide or raise an issue on the GitHub repository.