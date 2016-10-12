# Reset current directory
echo -n "Removing current executable..."
rm OpenGL_Playground
echo "done"
echo -n "Removing build directory..."
rm -rf build
echo "done"
# Create build directory
echo -n "Creating build directory..."
mkdir build
echo "done"
cd build
# Build
echo -n "Executing CMake..."
cmake ..
echo " - don"
echo -n "Executing make..."
make all
echo "done"
# Copy executable, fails silently
echo -n "Copying executable to directory..."
cp OpenGL_Playground .. 2>/dev/null
echo "done"
