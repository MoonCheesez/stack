cmake_minimum_required (VERSION 2.6)
project(OpenGL_Playground)

find_package(OpenGL REQUIRED)
find_package(glfw3 REQUIRED)
find_package(GLEW REQUIRED)

include_directories(
    /usr/local/include
)

add_executable(OpenGL_Playground
    playground.cpp

    common/shader.cpp
    common/shader.hpp

    SimpleVertexShader.vertexshader
    SimpleFragmentShader.fragmentshader
)

link_libraries(
    /usr/local/lib
)

target_link_libraries(OpenGL_Playground
    glfw
    ${OPENGL_gl_LIBRARY}
    ${GLEW_LIBRARIES}
)
