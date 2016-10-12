// Include standard libraries
#include <stdio.h>
#include <stdlib.h>
// File manipulation libraries
#include <fstream>
#include <string>
// GLEW
#include <GL/glew.h>

#include "shader_v2.hpp"

using namespace std;

GLuint loadShaders(const char* vertex_file_path,
                   const char* fragment_file_path) {
    // Create Shaders
    GLuint vertexShaderID = glCreateShader(GL_VERTEX_SHADER);
    GLuint fragmentShaderID = glCreateShader(GL_FRAGMENT_SHADER);

    // Read Vertex Shader File
    string vertexShaderCode;
    ifstream vertexShaderFile;
    vertexShaderFile.open(vertex_file_path, ios::in);

    if (!vertexShaderFile.is_open()) {
        fprintf(stderr, "Failed to open vertex shader file. "
                        "Are you in the right directory?");
        getchar();
        return 0;
    }
    string line = "";
    while (getline(vertexShaderFile, line)) {
        vertexShaderCode += line + "\n";
    }
    vertexShaderFile.close();

    // Read the Fragment Shader File
    string fragmentShaderCode;
    ifstream fragmentShaderFile;
    fragmentShaderFile.open(fragment_file_path, ios::in);

    if (!fragmentShaderFile.is_open()) {
        fprintf(stderr, "Failed to open fragment shader file. "
                        "Are you in the right directory?");
        getchar();
        return 0;
    }
    line = "";
    while (getline(fragmentShaderFile, line)) {
        fragmentShaderCode += line + "\n";
    }
    fragmentShaderFile.close();

    // Compile Shaders
    const char* adapter[1];
    adapter[0] = vertexShaderCode.c_str();
    glShaderSource(vertexShaderID, 1, adapter, 0);
    adapter[0] = fragmentShaderCode.c_str();
    glShaderSource(fragmentShaderID, 1, adapter, 0);

    glCompileShader(vertexShaderID);
    glCompileShader(fragmentShaderID);

    // Create program
    GLuint programID = glCreateProgram();
    glAttachShader(programID, vertexShaderID);
    glAttachShader(programID, fragmentShaderID);
    glLinkProgram(programID);

    return programID;
}
