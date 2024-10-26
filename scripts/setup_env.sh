#!/bin/bash

# Script: setup_env.sh
# Purpose: Automate the setup of the development environment for Metasurface Design Automation

echo "Starting environment setup..."

# Step 1: Check for Python and Install Virtual Environment
if ! command -v python3 &>/dev/null; then
    echo "Python3 not found. Please install Python 3.7 or higher."
    exit 1
fi

# Step 2: Create Virtual Environment
echo "Creating virtual environment..."
python3 -m venv metasurface_env

# Step 3: Activate Virtual Environment
source metasurface_env/bin/activate

# Step 4: Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Step 5: Install Dependencies
echo "Installing required packages..."
pip install -r requirements.txt

# Step 6: Check and Set Up Configuration Files
CONFIG_DIR="config"
if [ ! -d "$CONFIG_DIR" ]; then
    echo "Creating configuration directory..."
    mkdir $CONFIG_DIR
fi

# Copy default configuration files if not present
if [ ! -f "$CONFIG_DIR/simulation_config.yaml" ]; then
    echo "Copying default simulation configuration..."
    cp docs/default_configs/simulation_config.yaml $CONFIG_DIR/
fi

if [ ! -f "$CONFIG_DIR/job_submission.yaml" ]; then
    echo "Copying default job submission configuration..."
    cp docs/default_configs/job_submission.yaml $CONFIG_DIR/
fi

if [ ! -f "$CONFIG_DIR/app_settings.yaml" ]; then
    echo "Copying default app settings..."
    cp docs/default_configs/app_settings.yaml $CONFIG_DIR/
fi

# Step 7: Display Setup Summary
echo "Environment setup complete!"
echo "To activate the virtual environment, run: source metasurface_env/bin/activate"
echo "Make sure to customize configuration files in the 'config' directory as needed."

# End of setup script
