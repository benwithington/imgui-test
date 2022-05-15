import glfw
from OpenGL.GL import *
import imgui
from imgui.integrations.glfw import GlfwRenderer

width  = 1280
height = 720
title  = "pyimgui test"

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
            clicked, selected = imgui.menu_item("Quit", "Ctrl+Q")
            if clicked:
                glfw.set_window_should_close(glfw_window, True)
            imgui.end_menu()
        imgui.end_main_menu_bar()

    imgui.begin("A Window")
    imgui.text("Hello from a window")
    imgui.end()
                

if __name__ == "__main__":
    main()