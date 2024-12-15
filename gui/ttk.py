import customtkinter as ctk
from gui.equalizer import PixelStack

from visual.compare import listPriorityKeys

def GUI():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Object Detection Webcam")
    root.attributes("-fullscreen", True)
        
    return root

def SetupLayout(root: ctk.CTk):
    
    main = ctk.CTkFrame(root)
    main.pack(side=ctk.LEFT, fill="both", expand=True)
    
    video = ctk.CTkLabel(main, text="")
    video.pack(expand=True, fill='both', padx=0, pady=0)
    
    sidebar = ctk.CTkFrame(root)
    sidebar.pack(side=ctk.LEFT, padx=10, pady=10, fill="both")

    noise = ctk.CTkFrame(sidebar)
    noise.pack(side=ctk.TOP)

    message = ctk.CTkFrame(sidebar)
    message.pack(side=ctk.TOP, padx=10, expand=True, fill="both")
    
    control = ctk.CTkFrame(sidebar)
    control.pack(side=ctk.BOTTOM, pady=10, padx=10, fill="both")

    return  main, video, control, noise, message

def SetupGraphEqualizer(noisePanel: ctk.CTkFrame):
    def setup(text:str):
        y = ctk.CTkFrame(noisePanel)
        y.pack(side=ctk.LEFT, fill="both")
        
        z = ctk.CTkLabel(y, width=10, height=1, text=text)
        z.pack(side=ctk.TOP)
        
        return PixelStack(y)
    
    return {
        key: setup(key).set_value
        for key in listPriorityKeys
    }

def SetupButtons(root:ctk.CTk, control_frame: ctk.CTkFrame, actions: dict[str, callable]):
    startObjectDetection = ctk.CTkButton(
        control_frame, 
        text="Start OD", 
        command=actions["startObjectDetection"],
        width=10
    )
    startObjectDetection.pack(side=ctk.LEFT)
    
    stopObjectDetection = ctk.CTkButton(
        control_frame, 
        text="Stop OD", 
        command=actions["stopObjectDetection"],
        width=10
    )
    stopObjectDetection.pack(side=ctk.LEFT, padx=5)

    quit_button = ctk.CTkButton(
        control_frame, 
        text="X", 
        command=root.quit,
        width=2
    )
    quit_button.pack(side=ctk.RIGHT)


