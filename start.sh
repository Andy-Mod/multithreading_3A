#!/bin/bash

# Function to handle termination
cleanup() {
    echo "Terminating all processes..."
    pkill -P $$  # Kill all child processes of this script
    exit 0
}

# Trap SIGINT (Ctrl+C) and call cleanup
trap cleanup SIGINT

# Step 1: Compile the C++ code
echo "Compiling low_level.cpp..."
cd cplusplus/
cmake -B build -S .
cmake --build build
cd ..

sleep 2

# Step 2: Launch "queueManager.py" in the background
echo "Starting queueManager.py..."
python3 src/queueManager.py &
sleep 5

# Step 3: Launch "proxy.py" in the background
echo "Starting proxy.py..."
python3 src/proxy.py &
sleep 5

# Step 4: Launch the compiled C++ program
echo "Launching the compiled C++ low_level executable..."
OMP_NUM_THREADS=8 ./cplusplus/build/low_level &
sleep 5

# Step 5: Launch Launch "boss.py" in the background
echo "Starting boss.py..."
python3 src/boss.py &
sleep 5

# Wait for all background processes to finish
echo "All processes are running. Press Ctrl+C to terminate."
wait
