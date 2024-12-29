import os
import customtkinter as ctk
import json

from visual.preprocessing import height, width


class DrawingApp:
    def __init__(self, priority: str):
        if priority != "high" and priority != "medium":
            print("> Wrong Priority")
            return

        self.root = ctk.CTk()
        self.priority = priority
        self.root.title(f"Drawing App {priority}")

        self.sidebar = ctk.CTkFrame(self.root)
        self.sidebar.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH, padx=10, pady=10)

        self.canvas = ctk.CTkCanvas(self.root, bg="white", width=width, height=height)
        self.canvas.pack(side=ctk.TOP)

        self.pen_color = "red" if self.priority == "high" else "orange"
        self.drawing = False
        self.last_x, self.last_y = None, None

        self.lines = []  # List to store drawn lines
        self.lines_data = []  # List to store drawn lines

        self.undo_button = ctk.CTkButton(self.sidebar, text="Undo", command=self.undo)
        self.erase_button = ctk.CTkButton(
            self.sidebar, text="Erase", command=self.erase
        )
        self.save_button = ctk.CTkButton(
            self.sidebar, text="Save", command=self.save_data
        )
        self.close_button = ctk.CTkButton(
            self.sidebar, text="Close", command=self.root.quit
        )

        self.load_data()

        self.undo_button.pack(side=ctk.LEFT)
        self.erase_button.pack(side=ctk.LEFT, padx=10)
        self.close_button.pack(side=ctk.RIGHT)
        self.save_button.pack(side=ctk.RIGHT, padx=10)

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        self.root.mainloop()

    def start_draw(self, event):
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            line = self.canvas.create_line(
                self.last_x, self.last_y, x, y, fill=self.pen_color, width=2
            )
            self.lines.append(line)  # Store the drawn line
            self.lines_data.append({"x": x, "y": y})  # Store the drawn line

            self.last_x, self.last_y = x, y

    def load_data(self):
        if os.path.exists("canvas.json"):
            with open("canvas.json", "r") as file:
                self.data = json.load(file)
                self.lines_data = self.data[self.priority]

        else:
            print("> State file not found")
            return

        last = {"x": None, "y": None}
        for line_data in self.lines_data:
            x = line_data["x"]
            y = line_data["y"]

            if last["x"] is not None:
                if x is not None:
                    line = self.canvas.create_line(
                        last["x"], last["y"], x, y, fill=self.pen_color, width=2
                    )
                    self.lines.append(line)

            last["x"] = x
            last["y"] = y

    def save_data(self):
        self.data[self.priority] = self.lines_data

        json_object = json.dumps(self.data, indent=4)

        with open("canvas.json", "w") as outfile:
            outfile.write(json_object)

        self.root.quit()

    def stop_draw(self, event):
        self.drawing = False
        self.lines_data.append({"x": None, "y": None})

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
    DrawingApp("medium")
