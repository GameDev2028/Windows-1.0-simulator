import tkinter as tk
from tkinter import filedialog, messagebox
try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None  # Will warn the user if PIL is missing

WIN_BG = "#C0C0C0"
TITLE_BG = "#000080"
TITLE_FG = "#FFFFFF"
BORDER_LIGHT = "#FFFFFF"
BORDER_DARK = "#808080"
FONT = ("Fixedsys", 10)
TITLE_FONT = ("Fixedsys", 10, "bold")
BUTTON_BG = WIN_BG
BUTTON_FG = "#000000"
ENTRY_BG = "#FFFFFF"
ENTRY_FG = "#000000"

def win1_button(master, **kwargs):
    opts = {
        "font": FONT,
        "bg": BUTTON_BG,
        "fg": BUTTON_FG,
        "bd": 1,
        "relief": tk.RAISED,
        "activebackground": BORDER_LIGHT,
        "activeforeground": BUTTON_FG,
        "highlightbackground": BORDER_DARK,
    }
    opts.update(kwargs)
    return tk.Button(master, **opts)

class DraggableWindow(tk.Toplevel):
    def __init__(self, master, title="Window", width=300, height=200, **kwargs):
        super().__init__(master, **kwargs)
        self.title(title)
        self.geometry(f"{width}x{height}+120+120")
        self.overrideredirect(True)
        self.config(bg=BORDER_DARK)
        self.outline = tk.Frame(self, bg=BORDER_LIGHT)
        self.outline.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self.frame = tk.Frame(self.outline, bg=WIN_BG)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self.title_bar = tk.Frame(self.frame, bg=TITLE_BG, height=24)
        self.title_bar.pack(fill=tk.X)
        self.title_label = tk.Label(self.title_bar, text=title, fg=TITLE_FG, bg=TITLE_BG, font=TITLE_FONT, padx=6)
        self.title_label.pack(side=tk.LEFT, pady=2)
        self.close_btn = win1_button(self.title_bar, text="■", width=2, height=1, command=self.destroy)
        self.close_btn.pack(side=tk.RIGHT, padx=4, pady=2)
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        self.bind("<Button-1>", lambda e: self.lift())
    def start_move(self, event):
        self._drag_data = {"x": event.x, "y": event.y}
    def do_move(self, event):
        x = self.winfo_x() + event.x - self._drag_data["x"]
        y = self.winfo_y() + event.y - self._drag_data["y"]
        self.geometry(f"+{x}+{y}")

class PaintApp(DraggableWindow):
    def __init__(self, master, **kwargs):
        super().__init__(master, title="Paint", width=384, height=280, **kwargs)
        self.current_color = "#000000"
        self.pen_width = 2
        self.last_x, self.last_y = None, None
        self.canvas_width, self.canvas_height = 340, 170

        # --- Toolbar (Save button is always shown)
        toolbar = tk.Frame(self.frame, bg=WIN_BG)
        toolbar.pack(fill=tk.X, padx=5, pady=(3,2))

        win1_button(toolbar, text="Save", width=6, command=self.save_to_file).pack(side=tk.RIGHT, padx=2)
        win1_button(toolbar, text="Clear", width=6, command=self.clear_canvas).pack(side=tk.RIGHT, padx=2)
        tk.Label(toolbar, text="Color:", bg=WIN_BG, font=FONT).pack(side=tk.LEFT, padx=(2,0))
        for color in ["#000000", "#0000ff", "#ff0000", "#008000", "#ffff00", "#ffa500", "#ffffff"]:
            cbtn = win1_button(toolbar, width=2, text="   ", command=lambda col=color: self.set_color(col), bg=color)
            cbtn.pack(side=tk.LEFT, padx=1)
        tk.Label(toolbar, text="Width:", bg=WIN_BG, font=FONT).pack(side=tk.LEFT, padx=(6,0))
        self.width_var = tk.IntVar(value=self.pen_width)
        w_entry = tk.Spinbox(toolbar, from_=1, to=10, width=2, textvariable=self.width_var, font=FONT, bd=1)
        w_entry.pack(side=tk.LEFT, padx=2)
        w_entry.bind("<KeyRelease>", lambda e: self.set_width())
        w_entry.bind("<ButtonRelease-1>", lambda e: self.set_width())

        # --- Canvas area
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
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_draw)
        # For saving: memory image
        if Image:
            self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
            self.draw_pil = ImageDraw.Draw(self.image)
        else:
            self.image = None
            self.draw_pil = None
    def set_color(self, color):
        self.current_color = color
    def set_width(self):
        try:
            self.pen_width = int(self.width_var.get())
        except Exception:
            self.pen_width = 2
    def clear_canvas(self):
        self.canvas.delete("all")
        if self.image:
            self.image.paste("white", [0, 0, self.canvas_width, self.canvas_height])
            self.draw_pil = ImageDraw.Draw(self.image)
    def start_draw(self, event):
        self.last_x, self.last_y = event.x, event.y
    def draw(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.set_width()
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill=self.current_color,
                width=self.pen_width,
                capstyle=tk.PROJECTING,
                smooth=False
            )
            if self.draw_pil:
                self.draw_pil.line(
                    [self.last_x, self.last_y, event.x, event.y],
                    fill=self.current_color,
                    width=self.pen_width
                )
            self.last_x, self.last_y = event.x, event.y
    def reset_draw(self, event):
        self.last_x, self.last_y = None, None
    def save_to_file(self):
        if not self.image:
            messagebox.showerror("Paint", "Pillow is required for saving images.\nInstall with: pip install pillow")
            return
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

class Calculator(DraggableWindow):
    def __init__(self, master, **kwargs):
        super().__init__(master, title="Calculator", width=172, height=226, **kwargs)
        self.expr = ""
        disp_frame = tk.Frame(self.frame, bg=BORDER_DARK)
        disp_frame.pack(pady=(9,4), padx=12)
        self.display = tk.Entry(
            disp_frame,
            font=FONT,
            bd=1,
            relief=tk.FLAT,
            justify="right",
            bg=ENTRY_BG,
            fg=ENTRY_FG,
            insertbackground=ENTRY_FG,
            width=18
        )
        self.display.pack(fill=tk.X, ipady=2)
        btns = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
        ]
        for row in btns:
            fr = tk.Frame(self.frame, bg=WIN_BG)
            fr.pack()
            for ch in row:
                if ch == "=":
                    b = win1_button(fr, text=ch, width=4, height=2, command=self.calculate)
                else:
                    b = win1_button(fr, text=ch, width=4, height=2, command=lambda c=ch: self.add_char(c))
                b.pack(side=tk.LEFT, padx=2, pady=2)
        fr2 = tk.Frame(self.frame, bg=WIN_BG)
        fr2.pack()
        win1_button(fr2, text="CE", width=6, command=self.clear_all).pack(side=tk.LEFT, padx=2, pady=2)
        win1_button(fr2, text="C", width=6, command=self.clear).pack(side=tk.LEFT, padx=2, pady=2)
    def add_char(self, ch):
        self.expr += ch
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expr)
    def clear(self):
        self.expr = self.expr[:-1]
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expr)
    def clear_all(self):
        self.expr = ""
        self.display.delete(0, tk.END)
    def calculate(self):
        try:
            result = str(eval(self.expr))
            self.display.delete(0, tk.END)
            self.display.insert(0, result)
            self.expr = result
        except Exception:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
            self.expr = ""

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Windows 1.0 Simulator")
        self.geometry("600x400")
        self.configure(bg=WIN_BG)
        self.resizable(False, False)
        self.desktop_label = tk.Label(self, text="Windows 1.0 Simulator", fg="#000000", bg=WIN_BG, font=TITLE_FONT)
        self.desktop_label.place(x=10, y=10)
        self.icon_notepad = win1_button(self, text="Notepad", width=13, height=2, command=self.launch_notepad)
        self.icon_notepad.place(x=12, y=50)
        self.icon_calc = win1_button(self, text="Calculator", width=13, height=2, command=self.launch_calculator)
        self.icon_calc.place(x=12, y=110)
        self.icon_paint = win1_button(self, text="Paint", width=13, height=2, command=self.launch_paint)
        self.icon_paint.place(x=12, y=170)
        self.taskbar = tk.Frame(self, bg=TITLE_BG, height=28)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        win1_button(self.taskbar, text="Notepad", width=12, command=self.launch_notepad).pack(side=tk.LEFT, padx=6, pady=2)
        win1_button(self.taskbar, text="Calculator", width=12, command=self.launch_calculator).pack(side=tk.LEFT, padx=6, pady=2)
        win1_button(self.taskbar, text="Paint", width=12, command=self.launch_paint).pack(side=tk.LEFT, padx=6, pady=2)
    def launch_notepad(self):
        Notepad(self)
    def launch_calculator(self):
        Calculator(self)
    def launch_paint(self):
        PaintApp(self)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()