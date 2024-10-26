File: docs/api_reference.md

API Reference
This document provides a comprehensive reference for the functions, modules, and scripts within the project, including descriptions, parameters, and expected outputs.

Table of Contents
Design Generation Module
Job Management Module
Data Processing and Aggregation
Machine Learning Module
Application Interface
Design Generation Module
generator.py
Functionality: Automates the creation of design files based on input parameters.
Main Functions:
generate_design(parameters: dict): Generates design files using parameterized inputs.
random_pattern_generation(seed: int): Generates random design patterns based on a seed.
Expected Output: Saved design files in specified formats.
utils.py
Purpose: Utility functions for geometric manipulation.
Functions:
create_shape(shape: str, params: dict): Creates specified geometric shapes.
manage_file_paths(path: str): Handles file path verification and updates.
Job Management Module
submitter.py
Purpose: Submits jobs to the supercomputer for simulation.
Functions:
submit_job(config: dict): Configures and submits jobs based on provided settings.
batch_submit_jobs(configs: list): Handles batch job submissions.
monitor.py
Purpose: Monitors the status of submitted jobs and manages retries.
Functions:
monitor_job_status(job_id: str): Returns current status of the job.
retry_failed_jobs(job_list: list): Retries failed jobs from a batch.
Data Processing and Aggregation
parser.py
Functionality: Extracts and cleans simulation output data.
Functions:
parse_output(data: str): Processes raw output for errors and removes unnecessary data.
structure_data(parsed_data: dict): Formats parsed data for further analysis.
aggregator.py
Purpose: Aggregates parsed data into uniform datasets.
Functions:
aggregate_results(results: list): Combines parsed data into a single dataset.
save_dataset(dataset: pd.DataFrame): Saves aggregated data in specified format.
validator.py
Purpose: Validates and checks data integrity.
Functions:
check_missing_values(data: pd.DataFrame): Identifies missing or inconsistent data.
validate_data_format(data: pd.DataFrame): Ensures data matches expected formats.
Machine Learning Module
cnn_model.py
Functionality: Defines a CNN model for design prediction.
Functions:
build_cnn(input_shape: tuple): Constructs CNN architecture.
train_model(data: pd.DataFrame): Trains the CNN model on provided dataset.
model_trainer.py
Purpose: Trains and validates ML models.
Functions:
train_model(data, config): Configures and trains model based on specified parameters.
evaluate_model(): Measures model accuracy and performance.
evaluation.py
Purpose: Evaluates model performance metrics.
Functions:
generate_metrics(predictions, labels): Creates performance metrics.
create_confusion_matrix(predictions, labels): Generates confusion matrix for evaluation.
Application Interface
app_interface.py
Functionality: CLI for inverse design application.
Main Commands:
run_design_query(parameters: dict): Runs query to generate designs based on desired outputs.
inverse_design.py
Purpose: Backend logic for matching output with design patterns.
Functions:
query_model(parameters: dict): Queries trained ML models for design suggestions.
get_design_suggestions(output_specs: dict): Returns potential design matches.