cmake_minimum_required (VERSION 2.6)
project(OpenGL_Playground)

# Find packages needed
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
# Only Mac needs this
if (APPLE)
    find_package(glfw3 REQUIRED)
endif()

# This happens to be the configuration for my mac and linux system
if(APPLE)
    set(inc_dirs
        /usr/local/include
    )
    set(lnk_dirs
        /usr/local/lib
    )
elseif(UNIX)
    set(inc_dirs
        /usr/include
    )
    set(lnk_dirs
        /usr/lib
    )
endif()


include_directories(
    ${inc_dirs}
    .
)

add_executable(OpenGL_Playground
    playground.cpp

    common/shader_v2.hpp
    common/shader_v2.cpp

    SimpleVertexShader.vertexshader
    SimpleFragmentShader.fragmentshader
)

link_libraries(
    ${lnk_dirs}
)

target_link_libraries(OpenGL_Playground
    glfw
    ${OPENGL_gl_LIBRARY}
    ${GLEW_LIBRARIES}
)
