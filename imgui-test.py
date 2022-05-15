import glfw
from OpenGL.GL import *
import imgui
from imgui.integrations.glfw import GlfwRenderer
import numpy as np
from PIL import Image
import sys

from ShaderProgram import *

width  = 1280
height = 720
title  = "pyimgui test"

vertices = np.array(
      #positions       #colors         #texture coords
    [ 0.5,  0.5, 0.0,  1.0, 0.0, 0.0,  1.0, 1.0,   #top right
      0.5, -0.5, 0.0,  0.0, 1.0, 0.0,  1.0, 0.0,   #bottom right
     -0.5, -0.5, 0.0,  0.0, 0.0, 1.0,  0.0, 0.0,   #bottom left
     -0.5,  0.5, 0.0,  1.0, 1.0, 0.0,  0.0, 1.0],  #top left
    dtype=np.float32
)

indices = np.array(
    [0, 1, 3,
     1, 2, 3],
     dtype=np.uint32
)

def main():
    if not glfw.init():
        print("Failed to initialise GLFW")
        return

    window = glfw.create_window(width, height, title, None, None)
    if not window:
        print("Failed to create GLFW window")
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebufferSizeCallback)

    #Create VAO and VBO
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    sizeInBytes = vertices.dtype.itemsize
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeInBytes, ctypes.c_void_p(0 * sizeInBytes))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeInBytes, ctypes.c_void_p(3 * sizeInBytes))
    glEnableVertexAttribArray(1)

    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeInBytes, ctypes.c_void_p(6 * sizeInBytes))
    glEnableVertexAttribArray(2)
    glBindVertexArray(0)

    #Texture Stuff
    wallTex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, wallTex)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    with Image.open("./resources/textures/wall.jpg") as image:
        img_width, img_height = image.size
        img_data = np.array(list(image.getdata()))
    
    #print(f"Width: {img_width}, Height: {img_height}\nData: {img_data}")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    del img_data

    #Create Shaders & Shader program
    vs = Shader("./shaders/default.vert", GL_VERTEX_SHADER)
    fs = Shader("./shaders/default.frag", GL_FRAGMENT_SHADER)
    program = Program(vs, fs)
    program.use()

    #imgui setup
    imgui.create_context()
    io = imgui.get_io()
    impl = GlfwRenderer(window)

    while not glfw.window_should_close(window):

        #User Inputs
        processInput(window)
        impl.process_inputs()

        #imgui start frame
        imgui.new_frame()

        #Render Stuff
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        program.use()
        glBindTexture(GL_TEXTURE_2D, wallTex)
        glBindVertexArray(vao)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glBindVertexArray(0)

        #Create imgui window
        #imgui.show_demo_window()
        gui(window)

        #Render imgui stuff
        imgui.render()
        impl.render(imgui.get_draw_data())
        
        #End imgui frame
        imgui.end_frame()

        #Swap Buffers & poll events
        glfw.swap_buffers(window)
        glfw.poll_events()

    impl.shutdown()
    glfw.terminate()

def processInput(window: glfw._GLFWwindow):

    #Close Application
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def framebufferSizeCallback(glfw_window: glfw._GLFWwindow, width: int, height: int):
    glViewport(0, 0, width, height)

def gui(glfw_window: glfw._GLFWwindow):
    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File"):
            clicked, selected = imgui.menu_item("Quit", "Esccd ")
            if clicked:
                glfw.set_window_should_close(glfw_window, True)
            imgui.end_menu()
        imgui.end_main_menu_bar()

    imgui.begin("A Window")
    imgui.text("Hello from a window")
    imgui.end()

if __name__ == "__main__":
    main()