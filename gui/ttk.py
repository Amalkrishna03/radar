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

    grid = ctk.CTkFrame(main)
    grid.pack(expand=True, fill="both", padx=0, pady=0)
    grid.configure(fg_color="#EDECEC")
    
    
    frame = ctk.CTkFrame(master=grid)
    frame.grid(row=1, column=1)
    
    frame1 = ctk.CTkFrame(master=grid)
    frame1.grid(row=1, column=2)
    
    frame2 = ctk.CTkFrame(master=grid)
    frame2.grid(row=2, column=1)
    
    video = ctk.CTkLabel(master=frame)
    video.pack(side=ctk.TOP, padx=10, pady=10)

    video1 = ctk.CTkLabel(master=frame1, text="1")
    video1.pack(side=ctk.TOP, padx=10, pady=10)

    video2 = ctk.CTkLabel(master=frame2, text="2")
    video2.pack(side=ctk.TOP, padx=10, pady=10)

    sidebar = ctk.CTkFrame(root)
    sidebar.pack(side=ctk.LEFT, padx=10, pady=10, fill="both")

    noise = ctk.CTkFrame(sidebar)
    noise.pack(side=ctk.TOP, pady=10)

    message = ctk.CTkFrame(sidebar)
    message.pack(side=ctk.TOP, padx=10, expand=True, fill="both")

    control = ctk.CTkFrame(sidebar)
    control.pack(side=ctk.BOTTOM, pady=10, padx=10, fill="both")

    return main, video, control, noise, message, video1, video2


def SetupGraphEqualizer(noisePanel: ctk.CTkFrame):
    def setup(text: str):
        y = ctk.CTkFrame(noisePanel)
        y.pack(side=ctk.LEFT, fill="both")

        z = ctk.CTkLabel(y, width=10, height=1, text=text)
        z.pack(side=ctk.TOP)

        return PixelStack(y)

    return {key: setup(key).set_value for key in listPriorityKeys}


def SetupButtons(control_frame: ctk.CTkFrame, actions: dict[str, callable]):
    for b in actions:
        button = ctk.CTkButton(
            control_frame,
            text=" ".join(b.split("_")),
            command=actions[b],
        )
        button.pack(side=ctk.TOP, pady=5)
