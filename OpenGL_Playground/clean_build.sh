#!/bin/bash
# This shell script will execute a clean build.

# Exit if any command fails
set -e

# Reset current directory
echo "Removing build directory..."
rm -rf build
# Create build directory
echo "Creating build directory..."
mkdir build
cd build
# Build
echo "Executing CMake..."
cmake ..
echo "Executing make..."
make all
# Copy executable
echo "Copying executable to directory..."
cp OpenGL_Playground ..
# Run executable
echo "Running..."
cd ..
./OpenGL_Playground
