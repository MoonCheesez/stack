#!/bin/bash
# This shell script will do a normal build. If there is no build directory,
# it will execute clean_build.sh

# Exit if any command fails
set -e
# Execute a clean build if build directory does not exist.
if [ ! -d "build" ]; then
    ./clean_build.sh
    exit
fi

cd build
# CMake
echo "Executing CMake..."
cmake ..
# Make
echo "Executing make..."
make all
# Copy executable
echo "Copying executable to directory"
cp OpenGL_Playground ..
# Run executable
echo "Running..."
cd ..
./OpenGL_Playground

