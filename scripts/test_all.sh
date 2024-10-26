#!/bin/bash

# Script: test_all.sh
# Purpose: Start all unit tests for the automation program

echo "Starting all unit tests..."

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
  echo "Error: Please activate the virtual environment before running the tests."
  exit 1
fi

# Run tests for each module with pytest
modules=("data_processor" "job_manager" "machine_learning" "design_generator" "app")

for module in "${modules[@]}"; do
  echo "Running tests for $module..."
  pytest $module/tests --disable-warnings || exit 1
done

# Summary
echo "All tests completed successfully!"
