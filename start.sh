#!/bin/bash

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
./cplusplus/build/low_level &
sleep 5

# Wait for all background processes to finish
wait
echo "All processes are running."
