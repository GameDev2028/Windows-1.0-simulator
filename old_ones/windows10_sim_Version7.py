import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw

# ... [rest of your constants and win1_button definition remain unchanged] ...

class Notepad(DraggableWindow):
    def __init__(self, master, **kwargs):
        super().__init__(master, title="Notepad", width=350, height=220, **kwargs)
        border = tk.Frame(self.frame, bg=BORDER_DARK, bd=0)
        border.pack(fill=tk.BOTH, expand=True, padx=5, pady=(2,6))
        self.text = tk.Text(
            border,
            font=FONT,
            bg=ENTRY_BG,
            fg=ENTRY_FG,
            bd=1,
            relief=tk.FLAT,
            insertbackground=ENTRY_FG,
            wrap=tk.WORD,
            height=10,
            width=44
        )
        self.text.pack(expand=True, fill=tk.BOTH, padx=2, pady=2)
        # Bottom bar: Save and OK
        bottom_bar = tk.Frame(self.frame, bg=WIN_BG, height=18)
        bottom_bar.pack(fill=tk.X, side=tk.BOTTOM)
        win1_button(bottom_bar, text="Save", width=6, command=self.save_to_file).pack(side=tk.RIGHT, padx=2, pady=2)
        win1_button(bottom_bar, text="OK", width=6, command=self.destroy).pack(side=tk.RIGHT, padx=2, pady=2)

    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files","*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.text.get("1.0", tk.END))
                messagebox.showinfo("Notepad", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Notepad", f"Error saving file:\n{e}")

class PaintApp(DraggableWindow):
    def __init__(self, master, **kwargs):
        super().__init__(master, title="Paint", width=384, height=280, **kwargs)
        self.current_color = "#000000"
        self.pen_width = 2
        self.last_x, self.last_y = None, None
        self.canvas_width, self.canvas_height = 340, 170

        # --- Toolbar
        toolbar = tk.Frame(self.frame, bg=WIN_BG)
        toolbar.pack(fill=tk.X, padx=5, pady=(3,2))
        tk.Label(toolbar, text="Color:", bg=WIN_BG, font=FONT).pack(side=tk.LEFT, padx=(2,0))
        for color in ["#000000", "#0000ff", "#ff0000", "#008000", "#ffff00", "#ffa500", "#ffffff"]:
            cbtn = win1_button(toolbar, width=2, text="   ", command=lambda col=color: self.set_color(col), bg=color)
            cbtn.pack(side=tk.LEFT, padx=1)
        tk.Label(toolbar, text="Width:", bg=WIN_BG, font=FONT).pack(side=tk.LEFT, padx=(6,0))
        self.width_var = tk.IntVar(value=self.pen_width)
        w_entry = tk.Spinbox(toolbar, from_=1, to=10, width=2, textvariable=self.width_var, font=FONT, bd=1, command=self.set_width)
        w_entry.pack(side=tk.LEFT, padx=2)
        win1_button(toolbar, text="Clear", width=6, command=self.clear_canvas).pack(side=tk.RIGHT, padx=4)
        win1_button(toolbar, text="Save", width=6, command=self.save_to_file).pack(side=tk.RIGHT, padx=2)

        # --- Canvas border for OG look
        paint_border = tk.Frame(self.frame, bg=BORDER_DARK)
        paint_border.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.canvas = tk.Canvas(
            paint_border,
            bg="#FFFFFF",
            width=self.canvas_width,
            height=self.canvas_height,
            bd=0,
            highlightthickness=0,
            cursor="cross"
        )
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Drawing bindings
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_draw)

        # For saving: memory image
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw_pil = ImageDraw.Draw(self.image)

    def set_color(self, color):
        self.current_color = color

    def set_width(self):
        try:
            self.pen_width = int(self.width_var.get())
        except Exception:
            self.pen_width = 2

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image.paste("white", [0, 0, self.canvas_width, self.canvas_height])
        self.draw_pil = ImageDraw.Draw(self.image)

    def start_draw(self, event):
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.set_width()
            # Draw on canvas
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill=self.current_color,
                width=self.pen_width,
                capstyle=tk.PROJECTING,
                smooth=False
            )
            # Draw on PIL image
            self.draw_pil.line(
                [self.last_x, self.last_y, event.x, event.y],
                fill=self.current_color,
                width=self.pen_width
            )
            self.last_x, self.last_y = event.x, event.y

    def reset_draw(self, event):
        self.last_x, self.last_y = None, None

    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                self.image.save(file_path, "PNG")
                messagebox.showinfo("Paint", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Paint", f"Error saving image:\n{e}")

# The rest of the code (Calculator, MainApp, etc.) remains unchanged.