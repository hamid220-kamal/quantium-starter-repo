#!/bin/bash

# Soul Foods Pink Morsel Sales Visualizer - CI Test Runner
# This script activates the virtual environment and runs the test suite.
# Exit codes: 0 = all tests passed, 1 = tests failed or error occurred

echo "=========================================="
echo "Soul Foods CI Test Runner"
echo "=========================================="

# Step 1: Activate the virtual environment
echo ""
echo "[1/2] Activating virtual environment..."

# Check if running on Windows (Git Bash) or Unix
if [[ -f "venv/Scripts/activate" ]]; then
    # Windows (Git Bash)
    source venv/Scripts/activate
elif [[ -f "venv/bin/activate" ]]; then
    # Unix/Linux/MacOS
    source venv/bin/activate
else
    echo "ERROR: Virtual environment not found!"
    echo "Please create a virtual environment first using: python -m venv venv"
    exit 1
fi

echo "Virtual environment activated successfully."

# Step 2: Run the test suite
echo ""
echo "[2/2] Running test suite..."
echo ""

pytest test_app.py -v

# Capture the exit code from pytest
TEST_EXIT_CODE=$?

echo ""
echo "=========================================="

# Return appropriate exit code
if [[ $TEST_EXIT_CODE -eq 0 ]]; then
    echo "SUCCESS: All tests passed!"
    echo "=========================================="
    exit 0
else
    echo "FAILURE: Some tests failed!"
    echo "=========================================="
    exit 1
fi
