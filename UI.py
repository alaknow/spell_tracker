import tkinter as tk
from PIL import Image, ImageTk
import time
import json
import os
import sys

# Function to get the correct resource path
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Load spells from JSON file
spells_json_path = resource_path("spells.json")
with open(spells_json_path, "r", encoding="utf-8") as file:
    spells_data = json.load(file)

# Function to filter spells
def get_spells_by_level_and_class(level, character_class):
    return [spell for spell in spells_data if str(spell["level"]) == str(level) and character_class in spell["classes"]]

class SpellSlotTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Spell Slot Tracker")
        
        # Get screen size
        self.window_width = int(root.winfo_screenwidth() * 0.9)
        self.window_height = int(root.winfo_screenheight() * 0.9)
        root.geometry(f"{self.window_width}x{self.window_height}")
        
        # Load background image dynamically
        self.bg_image = Image.open(resource_path("images/background.png")).resize((self.window_width, self.window_height), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)
        
        # Slot setup
        self.spell_levels = 3  # Number of spell levels
        self.slot_counts = [4, 3, 2]  # Initial slot count
        self.image_paths = [resource_path(f"images/Druid{i}.png") for i in range(5)]
        self.slot_size = int(self.window_width * 0.15)  # Scalable slot size
        self.images = [ImageTk.PhotoImage(Image.open(path).resize((self.slot_size, self.slot_size))) for path in self.image_paths]
        
        self.labels = []
        self.selected_spells_labels = []
        self.selected_spells = [[] for _ in range(self.spell_levels)]
        
        # Dropdown for selecting a class
        self.character_class = tk.StringVar()
        self.character_class.set("All Classes")
        class_options = sorted({cls for spell in spells_data for cls in spell["classes"]})
        class_options.insert(0, "All Classes")
        self.class_menu = tk.OptionMenu(root, self.character_class, *class_options)
        self.class_menu.pack(pady=10)
        
        # Create slot UI
        for i in range(self.spell_levels):
            frame = tk.Frame(root, bg="lightgray", bd=2, relief=tk.RIDGE)
            frame.pack(pady=10, padx=10, fill="x")
            
            label = tk.Label(frame, image=self.images[self.slot_counts[i]], bg="lightgray")
            label.pack(side=tk.LEFT, padx=10)
            label.bind("<Button-1>", lambda event, i=i: self.use_spell(i))
            self.labels.append(label)
            
            spell_button = tk.Button(frame, text=f"{i+1} Level Spells", command=lambda i=i: self.show_spell_menu(i),
                                     bg="darkgreen", fg="white", font=("Arial", 16), height=2, width=15)
            spell_button.pack(side=tk.RIGHT, padx=10)
            
            spell_label = tk.Label(frame, text="No spells selected", font=("Arial", 12), bg="lightgray")
            spell_label.pack(side=tk.RIGHT, padx=10)
            self.selected_spells_labels.append(spell_label)
        
        self.reset_button = tk.Button(root, text="Reset All", command=self.reset_slots, bg="brown", fg="white", font=("Arial", 16), height=2, width=15)
        self.reset_button.pack(pady=10)
        
        root.bind("<Configure>", self.resize_ui)
    
    def use_spell(self, level):
        if self.slot_counts[level] > 0:
            self.slot_counts[level] -= 1
            self.labels[level].config(image=self.images[self.slot_counts[level]])
            if self.slot_counts[level] == 0:
                self.labels[level].unbind("<Button-1>")
    
    def show_spell_menu(self, level):
        menu = tk.Toplevel(self.root)
        menu.title(f"{level+1} Level Spells")
        menu_width, menu_height = int(self.window_width * 0.6), int(self.window_height * 0.7)
        menu.geometry(f"{menu_width}x{menu_height}")
        
        selected_class = self.character_class.get()
        spells = get_spells_by_level_and_class(level + 1, selected_class) if selected_class != "All Classes" else [spell for spell in spells_data if str(spell["level"]) == str(level + 1)]
        
        canvas = tk.Canvas(menu, width=menu_width, height=menu_height)
        scrollbar = tk.Scrollbar(menu, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for spell in spells:
            tk.Button(scroll_frame, text=spell["name"], font=("Arial", 14), command=lambda spell=spell, level=level: self.select_spell(spell, level, menu)).pack(fill="x", pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def select_spell(self, spell, level, menu):
        if len(sum(self.selected_spells, [])) < 7:
            self.selected_spells[level].append(spell["name"])
            self.selected_spells_labels[level].config(text=", ".join(self.selected_spells[level]))
        menu.destroy()
    
    def reset_slots(self):
        self.slot_counts = [4, 3, 2]
        for i in range(self.spell_levels):
            self.labels[i].config(image=self.images[self.slot_counts[i]])
            self.selected_spells[i] = []
            self.selected_spells_labels[i].config(text="No spells selected")
            self.labels[i].bind("<Button-1>", lambda event, i=i: self.use_spell(i))
    
    def resize_ui(self, event):
        self.window_width, self.window_height = event.width, event.height
        self.bg_image = Image.open(resource_path("images/background.png")).resize((self.window_width, self.window_height), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label.config(image=self.bg_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpellSlotTracker(root)
    root.mainloop()