
from OpenGL.GL import *

class Shader:
    def __init__(self, path, shaderType):
        self.source = None
        with open(path) as file:
            self.source = file.readlines()

        self.id = glCreateShader(shaderType)
        glShaderSource(self.id, self.source)
        glCompileShader(self.id)

        status = glGetShaderiv(self.id, GL_COMPILE_STATUS)
        if not status:
            print(f"ERROR::SHADER::{str(shaderType).upper()}::COMPILATION_FAILED\n{glGetShaderInfoLog(self.id)}")
    
    def delete(self):
        glDeleteShader(self.id)

class Program:
    def __init__(self, vertexShader: Shader, fragmentShader: Shader):
        #Create program
        self.id = glCreateProgram()
        #Attach vertex and fragment shaders
        glAttachShader(self.id, vertexShader.id)
        glAttachShader(self.id, fragmentShader.id)
        #Link both shaders together
        glLinkProgram(self.id)

        #Make sure everything went fine
        status = glGetProgramiv(self.id, GL_LINK_STATUS)
        if not status:
            print(f"ERROR::SHADER::PROGRAM::LINKING_FAILED\n{glGetProgramInfoLog(self.id)}")
        else:
            #Delete shaders because they've been linked and are no longer needed
            vertexShader.delete()
            fragmentShader.delete()

    def use(self):
        """ Active this shader program """
        glUseProgram(self.id)
    
    def setMat4(self, name, mat):
        """ Send a 4x4 Matrix to the shader program"""
        glUniformMatrix4fv(glGetUniformLocation(self.id, name), 1, GL_FALSE, mat)

    def setVec3(self, name, x, y, z):
        """ Send a 4 column Vector to the shader program"""
        glUniform3f(glGetUniformLocation(self.id, name), x, y, z)