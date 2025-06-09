import tkinter as tk
from tkinter import simpledialog, messagebox

class DraggableWindow(tk.Toplevel):
    def __init__(self, master, title="Window", width=300, height=200, **kwargs):
        super().__init__(master, **kwargs)
        self.title(title)
        self.geometry(f"{width}x{height}+100+100")
        self.overrideredirect(True)
        self.configure(bg="#C0C0C0")
        self._drag_data = {"x": 0, "y": 0}
        # Title bar
        self.title_bar = tk.Frame(self, bg="#000080", relief="raised", bd=0, height=22)
        self.title_bar.pack(fill=tk.X)
        self.title_label = tk.Label(self.title_bar, text=title, fg="white", bg="#000080", font=("MS Sans Serif", 10, "bold"))
        self.title_label.pack(side=tk.LEFT, padx=6)
        self.close_btn = tk.Button(self.title_bar, text="X", fg="black", bg="#C0C0C0", bd=1, font=("MS Sans Serif", 8, "bold"), command=self.destroy, width=2, height=1)
        self.close_btn.pack(side=tk.RIGHT, padx=4, pady=2)
        # Dragging
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        # Focus
        self.bind("<Button-1>", lambda e: self.lift())

    def start_move(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def do_move(self, event):
        x = self.winfo_x() + event.x - self._drag_data["x"]
        y = self.winfo_y() + event.y - self._drag_data["y"]
        self.geometry(f"+{x}+{y}")

class Notepad(DraggableWindow):
    def __init__(self, master, **kwargs):
        super().__init__(master, title="Notepad", width=350, height=250, **kwargs)
        self.text = tk.Text(self, font=("Courier New", 10))
        self.text.pack(expand=True, fill=tk.BOTH, padx=4, pady=(0,4))

class Calculator(DraggableWindow):
    def __init__(self, master, **kwargs):
        super().__init__(master, title="Calculator", width=220, height=270, **kwargs)
        self.expr = ""
        self.display = tk.Entry(self, font=("Courier New", 13), bd=2, relief="sunken", justify="right")
        self.display.pack(fill=tk.X, padx=8, pady=8)
        btns = [
            "789/", "456*", "123-", "0.C+", "CE="
        ]
        for row in btns:
            f = tk.Frame(self)
            f.pack(expand=True, fill=tk.BOTH)
            for ch in row:
                if ch == '.':
                    b = tk.Button(f, text=ch, width=3, height=2, command=lambda c=ch: self.add_char(c))
                elif ch == 'C':
                    b = tk.Button(f, text=ch, width=3, height=2, command=self.clear)
                elif ch == 'E':
                    b = tk.Button(f, text="CE", width=3, height=2, command=self.clear_all)
                elif ch == '=':
                    b = tk.Button(f, text=ch, width=3, height=2, command=self.calculate)
                else:
                    b = tk.Button(f, text=ch, width=3, height=2, command=lambda c=ch: self.add_char(c))
                b.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2, pady=2)
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
        except:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
            self.expr = ""

class PaintApp(DraggableWindow):
    def __init__(self, master, **kwargs):
        super().__init__(master, title="Paint", width=400, height=320, **kwargs)
        self.current_color = "#000000"
        self.pen_width = 2

        # Toolbar
        toolbar = tk.Frame(self, bg="#C0C0C0")
        toolbar.pack(fill=tk.X, padx=2, pady=(0,2))
        tk.Label(toolbar, text="Color:", bg="#C0C0C0").pack(side=tk.LEFT, padx=(2,0))
        for color in ["#000000", "#ff0000", "#008000", "#0000ff", "#ffff00", "#ffa500", "#ffffff"]:
            cbtn = tk.Button(toolbar, bg=color, width=2, command=lambda col=color: self.set_color(col))
            cbtn.pack(side=tk.LEFT, padx=2)
        tk.Label(toolbar, text="Width:", bg="#C0C0C0").pack(side=tk.LEFT, padx=(6,0))
        self.width_var = tk.IntVar(value=self.pen_width)
        w_entry = tk.Spinbox(toolbar, from_=1, to=10, width=2, textvariable=self.width_var, command=self.set_width)
        w_entry.pack(side=tk.LEFT, padx=2)
        clear_btn = tk.Button(toolbar, text="Clear", width=6, command=self.clear_canvas)
        clear_btn.pack(side=tk.RIGHT, padx=4)

        # Canvas
        self.canvas = tk.Canvas(self, bg="#ffffff", width=380, height=230, bd=2, relief="sunken", cursor="cross")
        self.canvas.pack(padx=8, pady=(0,8), expand=True, fill=tk.BOTH)
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.last_x, self.last_y = None, None

    def set_color(self, color):
        self.current_color = color

    def set_width(self):
        try:
            self.pen_width = int(self.width_var.get())
        except Exception:
            self.pen_width = 2

    def clear_canvas(self):
        self.canvas.delete("all")

    def start_draw(self, event):
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.set_width()
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.current_color, width=self.pen_width, capstyle=tk.ROUND, smooth=True)
        self.last_x, self.last_y = event.x, event.y


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Windows 1.0 Simulator")
        self.geometry("600x400")
        self.configure(bg="#008080")
        self.resizable(False, False)
        # Desktop icons
        self.desktop_label = tk.Label(self, text="Windows 1.0 Simulator", fg="white", bg="#008080", font=("MS Sans Serif", 13, "bold"))
        self.desktop_label.place(x=10, y=10)
        self.icon_notepad = tk.Button(self, text="Notepad", width=12, height=2, command=self.launch_notepad)
        self.icon_notepad.place(x=12, y=60)
        self.icon_calc = tk.Button(self, text="Calculator", width=12, height=2, command=self.launch_calculator)
        self.icon_calc.place(x=12, y=120)
        self.icon_paint = tk.Button(self, text="Paint", width=12, height=2, command=self.launch_paint)
        self.icon_paint.place(x=12, y=180)
        # Taskbar
        self.taskbar = tk.Frame(self, bg="#000080", height=32)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.btn_notepad = tk.Button(self.taskbar, text="Notepad", width=12, command=self.launch_notepad)
        self.btn_notepad.pack(side=tk.LEFT, padx=6, pady=2)
        self.btn_calc = tk.Button(self.taskbar, text="Calculator", width=12, command=self.launch_calculator)
        self.btn_calc.pack(side=tk.LEFT, padx=6, pady=2)
        self.btn_paint = tk.Button(self.taskbar, text="Paint", width=12, command=self.launch_paint)
        self.btn_paint.pack(side=tk.LEFT, padx=6, pady=2)

    def launch_notepad(self):
        Notepad(self)
    def launch_calculator(self):
        Calculator(self)
    def launch_paint(self):
        PaintApp(self)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()