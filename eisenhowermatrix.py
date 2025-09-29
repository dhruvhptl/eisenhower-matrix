import customtkinter as ctk
import random

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def random_scatter_position(x1, y1, x2, y2):
    x = random.randint(x1 + 20, x2 - 80)  # Padding for text width
    y = random.randint(y1 + 20, y2 - 30)  # Padding for text height  
    return x, y

class EisenhowerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Eisenhower Matrix")
        self.geometry("1050x650")
        self.minsize(900, 560)

        # Store tasks as (text, x, y, is_completed) tuples
        self.tasks = {
            "Urgent & Important": [],
            "Urgent & Not Important": [],
            "Not Urgent & Important": [],
            "Not Urgent & Not Important": []
        }
        self.task_text_ids = []
        self.task_click_map = {}

        # LEFT PANEL
        sidebar = ctk.CTkFrame(self, width=240, fg_color="#000000", corner_radius=18)
        sidebar.pack(side="left", fill="y", padx=16, pady=16)

        title_font = ctk.CTkFont(family="Marhey SemiBold", size=22, weight="bold")
        label_font = ctk.CTkFont(family="Marhey SemiBold", size=15)
        button_font = ctk.CTkFont(family="Marhey SemiBold", size=14)

        ctk.CTkLabel(sidebar, text="Enter Task:", font=title_font,
                     text_color="#FFFFFF", anchor="w").pack(pady=(24,6), anchor="w", padx=14)

        self.task_entry = ctk.CTkEntry(sidebar, width=210, font=label_font)
        self.task_entry.pack(pady=(0,24), padx=14)

        self.var_important = ctk.BooleanVar()
        self.var_urgent = ctk.BooleanVar()

        ctk.CTkCheckBox(sidebar, text="Important?", variable=self.var_important,
                        font=label_font, fg_color="#666666").pack(pady=6, anchor="w", padx=14)

        ctk.CTkCheckBox(sidebar, text="Urgent?", variable=self.var_urgent,
                        font=label_font, fg_color="#666666").pack(pady=6, anchor="w", padx=14)

        ctk.CTkButton(sidebar, text="Add Task", font=button_font,
                      fg_color="#3496ff", hover_color="#1e75d8",
                      command=self.add_task).pack(pady=(26,12), ipadx=10)

        ctk.CTkButton(sidebar, text="Clear Matrix", font=button_font,
                      fg_color="#e03b3b", hover_color="#ff6969",
                      command=self.clear_matrix).pack(ipadx=10)

        # MATRIX CANVAS
        canvas_frame = ctk.CTkFrame(self, fg_color="#EECFF4")
        canvas_frame.pack(side="right", fill="both", expand=True, padx=16, pady=16)

        self.canvas = ctk.CTkCanvas(canvas_frame, bg="#EECFF4", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.after(100, self.draw_matrix_background)

    def draw_matrix_background(self):
        self.canvas.update_idletasks()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        self.canvas.delete("all")
        self.task_text_ids.clear()
        self.task_click_map.clear()

        mid_x = width // 2
        mid_y = height // 2

        # Draw matrix rectangles
        self.canvas.create_rectangle(50, 50, mid_x-10, mid_y-10, 
                                   fill="#B5FFFA", outline="#FDDEDE", width=2)
        self.canvas.create_rectangle(mid_x+10, 50, width-50, mid_y-10, 
                                   fill="#B5FFFA", outline="#FDDEDE", width=2)
        self.canvas.create_rectangle(50, mid_y+10, mid_x-10, height-50, 
                                   fill="#B5FFFA", outline="#FDDEDE", width=2)
        self.canvas.create_rectangle(mid_x+10, mid_y+10, width-50, height-50, 
                                   fill="#B5FFFA", outline="#FDDEDE", width=2)

        # Axis labels
        # Axis labels - SWAPPED LABELS ONLY
        font_tuple = ("Marhey SemiBold", 14, "bold")

        # Horizontal axis labels (now Importance)
        self.canvas.create_text(mid_x//2 + 25, 30, text="Important", fill="#B5FFFA", font=font_tuple)
        self.canvas.create_text(mid_x + mid_x//2 + 25, 30, text="Not Important", fill="#B5FFFA", font=font_tuple)

        # Vertical axis labels (now Urgency)  
        self.canvas.create_text(25, mid_y//2 + 25, text="U\nr\ng\ne\nn\nt", 
                            fill="#B5FFFA", font=font_tuple, justify="center")
        self.canvas.create_text(25, mid_y + mid_y//2 + 25, text="N\no\nt\n \nU\nr\ng\ne\nn\nt", 
                            fill="#B5FFFA", font=font_tuple, justify="center")


        self.refresh_canvas()

    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            return
        
        # FIXED LOGIC
        urgent = self.var_urgent.get()
        important = self.var_important.get()

        if urgent and important:
            cat = "Urgent & Important"
        elif urgent and not important:
            cat = "Urgent & Not Important"
        elif not urgent and important:
            cat = "Not Urgent & Important"
        else:  # not urgent and not important
            cat = "Not Urgent & Not Important"

        # Get random position within quadrant bounds
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        mid_x, mid_y = width // 2, height // 2

        quadrant_bounds = {
            "Urgent & Important": (70, 70, mid_x-30, mid_y-30),
            "Urgent & Not Important": (mid_x+30, 70, width-70, mid_y-30),
            "Not Urgent & Important": (70, mid_y+30, mid_x-30, height-70),
            "Not Urgent & Not Important": (mid_x+30, mid_y+30, width-70, height-70)
        }

        x, y = random_scatter_position(*quadrant_bounds[cat])
        
        # Store task with position and completion status
        self.tasks[cat].append((task, x, y, False))
        
        self.task_entry.delete(0, "end")
        self.var_urgent.set(False)
        self.var_important.set(False)
        self.refresh_canvas()

    def clear_matrix(self):
        for v in self.tasks.values():
            v.clear()
        self.refresh_canvas()

    def on_canvas_click(self, event):
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        
        if clicked_item in self.task_click_map:
            category, task_index = self.task_click_map[clicked_item]
            task_text, x, y, is_completed = self.tasks[category][task_index]
            self.tasks[category][task_index] = (task_text, x, y, not is_completed)
            self.refresh_canvas()

    def refresh_canvas(self):
        # Clear old task text but keep background
        for text_id in self.task_text_ids:
            self.canvas.delete(text_id)
        self.task_text_ids.clear()
        self.task_click_map.clear()

        font_tuple = ("Marhey SemiBold", 12)

        for category, tasks in self.tasks.items():
            for i, (task_text, x, y, is_completed) in enumerate(tasks):
                if is_completed:
                    display_text = f"̶{task_text}̶"  # Unicode strikethrough
                    text_color = "#888888"
                else:
                    display_text = task_text
                    text_color = "#000000"
                
                text_id = self.canvas.create_text(x, y, text=display_text, 
                                                fill=text_color, font=font_tuple,
                                                anchor="w")
                self.task_text_ids.append(text_id)
                self.task_click_map[text_id] = (category, i)

    def on_resize(self, event=None):
        self.canvas.after(10, self.draw_matrix_background)

if __name__ == "__main__":
    app = EisenhowerApp()
    app.bind('<Configure>', app.on_resize)
    app.mainloop()
