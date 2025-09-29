import customtkinter as ctk
import random
import json
import os  # Added for file operations


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def random_scatter_position(x1, y1, x2, y2):
    x = random.randint(x1 + 20, x2 - 80)
    y = random.randint(y1 + 20, y2 - 30)
    return x, y


class EisenhowerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Eisenhower Matrix")
        self.geometry("1100x700")
        # MAIN WINDOW BACKGROUND COLOR
        self.configure(bg="#7A9B57")  # Forest green
        
        # Save file for matrix data
        self.save_file = "eisenhower_matrix_save.json"
        
        self.tasks = {
            "Urgent & Important": [],
            "Urgent & Not Important": [],
            "Not Urgent & Important": [],
            "Not Urgent & Not Important": []
        }
        self.task_text_ids = []
        self.task_click_map = {}

        # Load saved tasks
        self.load_tasks()

        self.create_left_panel()
        self.create_matrix_panel()
        
        # Save on window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_tasks(self):
        """Load saved tasks when app starts"""
        try:
            with open(self.save_file, 'r') as f:
                self.tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If no save file or corrupted, keep default empty tasks
            pass

    def save_tasks(self):
        """Save current tasks to file"""
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def on_closing(self):
        """Save before closing app"""
        self.save_tasks()
        self.destroy()

    def create_left_panel(self):
        # LEFT PANEL BACKGROUND COLOR
        sidebar = ctk.CTkFrame(self, width=340, fg_color="#F5E6A3", corner_radius=0)  # Creamy yellow
        sidebar.pack(side="left", fill="y", padx=0, pady=0)
        sidebar.pack_propagate(False)

        # RIGHT BORDER OF LEFT PANEL COLOR
        border_frame = ctk.CTkFrame(sidebar, width=8, fg_color="#8B4B9B")  # Purple border
        border_frame.pack(side="right", fill="y")

        content_frame = ctk.CTkFrame(sidebar, fg_color="#F5E6A3", corner_radius=0)  # Match left panel
        content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=40)

        # FONT SETTINGS
        title_font = ctk.CTkFont(family="Comic Sans MS", size=32, weight="bold")
        label_font = ctk.CTkFont(family="Comic Sans MS", size=16, weight="bold")
        button_font = ctk.CTkFont(family="Comic Sans MS", size=16, weight="bold")

        # TITLE TEXT COLOR
        ctk.CTkLabel(content_frame, text="Add Task", font=title_font,
                     text_color="#000000", fg_color="transparent").pack(pady=(0, 40))

        # ENTRY FIELD COLORS
        self.task_entry = ctk.CTkEntry(content_frame, width=280, height=45, 
                                     placeholder_text="Enter task here...",
                                     placeholder_text_color="#B8E6B8",
                                     font=ctk.CTkFont(size=14),
                                     fg_color="#7A9B57",
                                     border_color="#7A9B57",
                                     text_color="#FFFFFF",
                                     corner_radius=8)
        self.task_entry.pack(pady=(0, 30))

        # CHECKBOX CONTAINER COLORS
        checkbox_frame = ctk.CTkFrame(content_frame, width=280, height=120, 
                                    fg_color="#6B4423", corner_radius=15)
        checkbox_frame.pack(pady=(0, 30))
        checkbox_frame.pack_propagate(False)

        self.var_important = ctk.BooleanVar()
        self.var_urgent = ctk.BooleanVar()

        # FIXED CHECKBOXES - Grey when unchecked, green checkmark when checked
        important_cb = ctk.CTkCheckBox(checkbox_frame, text="Important?", 
                                     variable=self.var_important,
                                     font=label_font, 
                                     text_color="#FFFFFF",
                                     fg_color="#CCCCCC",  # Grey background (unchecked)
                                     hover_color="#AAAAAA",  # Darker grey on hover
                                     checkmark_color="#7A9B57",  # Green checkmark when checked
                                     border_color="#999999")  # Darker grey border
        important_cb.pack(pady=(20, 10))

        urgent_cb = ctk.CTkCheckBox(checkbox_frame, text="Urgent?", 
                                  variable=self.var_urgent, 
                                  font=label_font, 
                                  text_color="#FFFFFF",
                                  fg_color="#CCCCCC",  # Grey background (unchecked)
                                  hover_color="#AAAAAA",  # Darker grey on hover
                                  checkmark_color="#7A9B57",  # Green checkmark when checked
                                  border_color="#999999")  # Darker grey border
        urgent_cb.pack(pady=(0, 20))

        # BUTTON COLORS
        add_btn = ctk.CTkButton(content_frame, text="Add Task", 
                              font=button_font,
                              width=200, height=45,
                              fg_color="#A8D8A8",
                              hover_color="#90C290",
                              text_color="#FFFFFF",
                              corner_radius=8,
                              command=self.add_task)
        add_btn.pack(pady=(0, 15))

        clear_btn = ctk.CTkButton(content_frame, text="Clear Matrix", 
                                font=button_font,
                                width=200, height=45,
                                fg_color="#E85A5A",
                                hover_color="#D44444",
                                text_color="#FFFFFF",
                                corner_radius=8,
                                command=self.clear_matrix)
        clear_btn.pack()

    def create_matrix_panel(self):
        # MATRIX PANEL BACKGROUND COLOR
        matrix_container = ctk.CTkFrame(self, fg_color="#7A9B57", corner_radius=0)
        matrix_container.pack(side="right", fill="both", expand=True, padx=0, pady=0)

        self.canvas = ctk.CTkCanvas(matrix_container, bg="#7A9B57", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=30, pady=30)
        
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.after(100, self.draw_matrix_background)

    def draw_rounded_rectangle(self, x1, y1, x2, y2, radius, fill_color):
        """Draw a rounded rectangle on canvas"""
        # Create rounded corners using arcs
        self.canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, 
                             start=90, extent=90, fill=fill_color, outline=fill_color)
        self.canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, 
                             start=0, extent=90, fill=fill_color, outline=fill_color)
        self.canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, 
                             start=180, extent=90, fill=fill_color, outline=fill_color)
        self.canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, 
                             start=270, extent=90, fill=fill_color, outline=fill_color)
        
        # Fill the middle rectangles
        self.canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, 
                                   fill=fill_color, outline="")
        self.canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, 
                                   fill=fill_color, outline="")

    def draw_matrix_background(self):
        self.canvas.update_idletasks()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        self.canvas.delete("all")
        self.task_text_ids.clear()
        self.task_click_map.clear()

        # FIXED: Uniform border thickness
        border_width = 30
        corner_radius = 15
        
        # UNIFORM COORDINATES for the border
        border_x1, border_y1 = 30, 30
        border_x2, border_y2 = width - 30, height - 30
        
        # Draw uniform brown border with rounded corners
        self.draw_rounded_rectangle(border_x1, border_y1, border_x2, border_y2, 
                                  corner_radius, "#6B4423")

        # Inner cream area with uniform spacing
        inner_x1 = border_x1 + border_width
        inner_y1 = border_y1 + border_width + 20  # Small extra space for top labels
        inner_x2 = border_x2 - border_width
        inner_y2 = border_y2 - border_width

        # Draw cream background
        self.draw_rounded_rectangle(inner_x1, inner_y1, inner_x2, inner_y2, 
                                  corner_radius-8, "#F5E6A3")

        # Calculate center lines
        center_x = (inner_x1 + inner_x2) // 2
        center_y = (inner_y1 + inner_y2) // 2

        # Draw grid lines
        self.canvas.create_line(center_x, inner_y1, center_x, inner_y2, 
                              fill="#6B4423", width=3)
        self.canvas.create_line(inner_x1, center_y, inner_x2, center_y, 
                              fill="#6B4423", width=3)

        # IMPROVED AXIS LABELS
        axis_font = ("Comic Sans MS", 16, "bold")
        label_color = "#FFFFFF"
        
        # Top axis labels (horizontal)
        label_y = border_y1 + 15
        self.canvas.create_text((inner_x1 + center_x) // 2, label_y, 
                              text="Urgent", fill=label_color, font=axis_font)
        self.canvas.create_text((center_x + inner_x2) // 2, label_y, 
                              text="Not Urgent", fill=label_color, font=axis_font)
        
        # FIXED: Sideways vertical labels (horizontal text rotated)
        label_x = border_x1 + 15
        vertical_font = ("Comic Sans MS", 16, "bold")
        
        # Left axis labels - SIDEWAYS text instead of stacked
        self.canvas.create_text(label_x, (inner_y1 + center_y) // 2, 
                              text="Important", fill=label_color, 
                              font=vertical_font, angle=90)  # Rotated 90 degrees
        self.canvas.create_text(label_x, (center_y + inner_y2) // 2, 
                              text="Not Important", fill=label_color, 
                              font=vertical_font, angle=90)  # Rotated 90 degrees

        # Store quadrant bounds
        self.quadrant_bounds = {
            "Urgent & Important": (inner_x1 + 15, inner_y1 + 15, center_x - 8, center_y - 8),
            "Urgent & Not Important": (center_x + 8, inner_y1 + 15, inner_x2 - 15, center_y - 8),
            "Not Urgent & Important": (inner_x1 + 15, center_y + 8, center_x - 8, inner_y2 - 15),
            "Not Urgent & Not Important": (center_x + 8, center_y + 8, inner_x2 - 15, inner_y2 - 15)
        }

        self.refresh_canvas()

    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            return
        
        important = self.var_important.get()
        urgent = self.var_urgent.get()

        # FIXED LOGIC - Custom mapping as requested
        if urgent and important:
            cat = "Urgent & Important"  # Top-left (both checked)
        elif urgent and not important:
            cat = "Not Urgent & Important"  # Bottom-left (urgent only → your requirement)
        elif not urgent and important:
            cat = "Urgent & Not Important"  # Top-right (important only → your requirement)
        else:
            cat = "Not Urgent & Not Important"  # Bottom-right (neither checked)

        bounds = self.quadrant_bounds.get(cat, (100, 100, 300, 300))
        x, y = random_scatter_position(*bounds)
        
        self.tasks[cat].append((task, x, y, False))
        
        self.task_entry.delete(0, "end")
        self.var_urgent.set(False)
        self.var_important.set(False)
        self.refresh_canvas()
        
        # Save tasks after adding
        self.save_tasks()

    def clear_matrix(self):
        for v in self.tasks.values():
            v.clear()
        self.refresh_canvas()
        
        # Delete save file when clearing matrix
        if os.path.exists(self.save_file):
            os.remove(self.save_file)

    def on_canvas_click(self, event):
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        
        if clicked_item in self.task_click_map:
            category, task_index = self.task_click_map[clicked_item]
            task_text, x, y, is_completed = self.tasks[category][task_index]
            self.tasks[category][task_index] = (task_text, x, y, not is_completed)
            self.refresh_canvas()
            
            # Save tasks after toggling completion
            self.save_tasks()

    def refresh_canvas(self):
        for text_id in self.task_text_ids:
            self.canvas.delete(text_id)
        self.task_text_ids.clear()
        self.task_click_map.clear()

        task_font = ("Comic Sans MS", 11, "bold")
        normal_task_color = "#000000"
        completed_task_color = "#888888"

        for category, tasks in self.tasks.items():
            for i, (task_text, x, y, is_completed) in enumerate(tasks):
                if is_completed:
                    display_text = f"̶{task_text}̶"
                    text_color = completed_task_color
                else:
                    display_text = task_text
                    text_color = normal_task_color
                
                text_id = self.canvas.create_text(x, y, text=display_text, 
                                                fill=text_color, font=task_font,
                                                anchor="w")
                self.task_text_ids.append(text_id)
                self.task_click_map[text_id] = (category, i)

    def on_resize(self, event=None):
        self.canvas.after(10, self.draw_matrix_background)


if __name__ == "__main__":
    app = EisenhowerApp()
    app.bind('<Configure>', app.on_resize)
    app.mainloop()
