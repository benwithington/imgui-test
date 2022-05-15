import glfw
from OpenGL.GL import *

width  = 640
height = 480
title  = "PyImGUI Test"

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

    while not glfw.window_should_close(window):

        #User Inputs
        processInput(window)

        #Render Stuff
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        #Swap Buffers & poll events
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

def processInput(window: glfw._GLFWwindow):

    #Close Application
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def framebufferSizeCallback(glfw_window: glfw._GLFWwindow, width: int, height: int):
    glViewport(0, 0, width, height)

if __name__ == "__main__":
    main()