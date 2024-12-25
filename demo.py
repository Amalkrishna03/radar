import os
import customtkinter as ctk
import json

width = 640 * 2
height = 480 * 2

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")

        self.canvas = ctk.CTkCanvas(root, bg="red", width=width, height=height)
        self.canvas.pack()

        self.pen_color = "black"
        self.drawing = False
        self.last_x, self.last_y = None, None

        self.lines = []  # List to store drawn lines
        self.lines_data = []  # List to store drawn lines

        self.undo_button = ctk.CTkButton(root, text="Undo", command=self.undo)
        self.erase_button = ctk.CTkButton(root, text="Erase", command=self.erase)
        self.save_button = ctk.CTkButton(root, text="Save", command=self.save_data)
        
        self.load_data()
        
        self.undo_button.pack(side=ctk.LEFT)
        self.erase_button.pack(side=ctk.LEFT)
        self.save_button.pack(side=ctk.LEFT)

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

    def start_draw(self, event):
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            line = self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.pen_color, width=2)
            self.lines.append(line)  # Store the drawn line
            self.lines_data.append({"x":x, "y":y})  # Store the drawn line
            
            self.last_x, self.last_y = x, y
            
    def load_data(self):
        if os.path.exists("canvas.json"):
            with open('canvas.json', 'r') as file:
                data = json.load(file)
                self.lines_data = data['lines']
    
        else:
            print("> State file not found")
            return
                
        last = {
            'x': None,
            'y': None
        }
        for line_data in self.lines_data:
            x = line_data['x']
            y = line_data['y']
            
            if last['x'] is not None:
                if x is not None:
                    
                    line = self.canvas.create_line(last['x'], last['y'], x, y, fill=self.pen_color, width=2)
                    self.lines.append(line)
            
            last['x'] = x
            last['y'] = y
            
    
    def save_data(self):
        json_object = json.dumps({
            "lines": self.lines_data    
        }, indent=4)
 
        with open("canvas.json", "w") as outfile:
            outfile.write(json_object)
        

    def stop_draw(self, event):
        self.drawing = False
        self.lines_data.append({"x":None, "y":None})

    def undo(self):
        if self.lines:
            last_line = self.lines.pop()  # Remove the last drawn line
            self.canvas.delete(last_line)
            
            self.lines_data.pop()

    def erase(self):
        self.canvas.delete("all")
        self.lines.clear()
        self.lines_data.clear()
        

if __name__ == "__main__":
    root = ctk.CTk()
    app = DrawingApp(root)
    root.mainloop()
