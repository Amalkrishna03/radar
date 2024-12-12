import customtkinter as ctk


def GUI():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("Object Detection Webcam")
    root.geometry("800x600")
    
    return root

def SetupLayout(root: ctk.CTk):
    # Frame for video and controls
    main = ctk.CTkFrame(root)
    main.pack(expand=True, fill='both', padx=0, pady=0)

    # Video display label
    videoLabel = ctk.CTkLabel(main, text="")
    videoLabel.pack(expand=True, fill='both', padx=0, pady=0)

    # Control frame
    controlPanel = ctk.CTkFrame(main)
    controlPanel.pack(fill='x', padx=0, pady=0)

    return  main, controlPanel, videoLabel


def SetupButtons(root:ctk.CTk, control_frame: ctk.CTkFrame):
    # detect_button.pack(side='left', padx=5)

    quit_button = ctk.CTkButton(
        control_frame, 
        text="Quit", 
        command=root.quit
    )
    quit_button.pack(side='left', padx=5)


