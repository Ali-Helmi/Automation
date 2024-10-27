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
# Create or clear the summary file
SUMMARY_FILE="test_summary.log"
echo "Starting all unit tests..." > "$SUMMARY_FILE"

for module in "${modules[@]}"; do
  echo "Running tests for $module..." | tee -a "$SUMMARY_FILE"
  pytest $module/tests --disable-warnings >> "$SUMMARY_FILE"
  if [ $? -ne 0 ]; then
    echo "Tests failed for $module. Check $SUMMARY_FILE for details."
    exit 1
  fi
done

echo "All tests completed successfully!" | tee -a "$SUMMARY_FILE"

echo "All tests completed successfully!"
