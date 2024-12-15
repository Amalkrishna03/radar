import colorsys
import tkinter as tk

import customtkinter as ctk

from visual.compare import listPriorityKeys


class PixelStack:
    def __init__(self, root, width=50, height=500, stack_size=10):
        """
        Initialize the pixel stack visualization

        :param root: Tkinter root or parent window
        :param width: Width of each pixel block
        :param height: Total height of the stack
        :param stack_size: Number of pixels in the stack
        """
        self.root = root
        self.width = width
        self.height = height
        self.stack_size = stack_size

        # Create canvas
        self.canvas = tk.Canvas(root, width=width, height=height, bg="white")
        self.canvas.pack(side=ctk.LEFT)

        # Create pixel stack rectangles
        self.pixels = []
        pixel_height = height // stack_size

        for i in range(stack_size):
            # Calculate color from green to yellow to red
            # We'll use HSV color space for smooth transition
            hue = (
                1 - i / (stack_size - 1)
            ) * 0.35  # 0.35 corresponds to green->yellow->red
            color = self._hsv_to_hex(hue, 1, 1)

            # Create rectangle from bottom to top
            rect = self.canvas.create_rectangle(
                0,
                height - (i + 1) * pixel_height,
                width,
                height - i * pixel_height,
                fill="white",  # Start with white (empty)
                outline="black",
            )
            self.pixels.append({"rect": rect, "color": color})
            
        self.set_value(30)
        # return self.canvas

    def _hsv_to_hex(self, h, s, v):
        """
        Convert HSV color to hex

        :param h: Hue (0-1)
        :param s: Saturation (0-1)
        :param v: Value (0-1)
        :return: Hex color string
        """
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return "#{:02x}{:02x}{:02x}".format(
            int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
        )

    def set_value(self, value):
        """
        Set pixels based on input value (0-100)

        :param value: Percentage of pixels to fill (0-100)
        """
        # Validate input
        value = max(0, min(100, value))

        # Calculate number of pixels to fill
        pixels_to_fill = int((value / 100) * self.stack_size)

        # Reset all pixels
        for pixel in self.pixels:
            self.canvas.itemconfig(pixel["rect"], fill="white")

        # Fill pixels from bottom
        for i in range(pixels_to_fill):
            self.canvas.itemconfig(self.pixels[i]["rect"], fill=self.pixels[i]["color"])

    def clear_stack(self):
        """
        Clear all pixels (set to white)
        """
        for pixel in self.pixels:
            self.canvas.itemconfig(pixel["rect"], fill="white")
