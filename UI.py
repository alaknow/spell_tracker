import tkinter as tk
from PIL import Image, ImageTk
import time
import json
import os
import sys

# Function to get the correct resource path, works for development & PyInstaller
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Paths to resources
background_image_path = resource_path("images/background.png")
image_paths = [
    resource_path("images/Druid0.png"),
    resource_path("images/Druid1.png"),
    resource_path("images/Druid2.png"),
    resource_path("images/Druid3.png"),
    resource_path("images/Druid4.png")
]

# Load spells from JSON file
spells_json_path = resource_path("spells.json")
with open(spells_json_path, "r", encoding="utf-8") as file:
    spells_data = json.load(file)

# Function to filter spells by level and class
def get_spells_by_level_and_class(level, character_class):
    return [spell for spell in spells_data if str(spell["level"]) == str(level) and character_class in spell["classes"]]

class SpellSlotTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Spell Slot Tracker")
        
        # Set background image
        self.bg_image = ImageTk.PhotoImage(Image.open(background_image_path).resize((800, 600)))
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)
        
        self.spell_levels = 3  # Number of spell levels to track
        self.initial_slots = [4, 3, len(image_paths) - 1]  # Set initial slots per level
        self.slot_counts = self.initial_slots[:]
        self.images = [ImageTk.PhotoImage(Image.open(path).resize((150, 150))) for path in image_paths]
        
        self.labels = []
        self.selected_spells_labels = []  # Labels for displaying selected spells per level
        self.selected_spells = [[] for _ in range(self.spell_levels)]  # Stores selected spells per level
        
        # Dropdown for selecting a class
        self.character_class = tk.StringVar()
        self.character_class.set("All Classes")
        class_options = sorted({cls for spell in spells_data for cls in spell["classes"]})
        class_options.insert(0, "All Classes")
        self.class_menu = tk.OptionMenu(root, self.character_class, *class_options)
        self.class_menu.pack()
        
        for i in range(self.spell_levels):
            frame = tk.Frame(root, bg="lightgray", bd=2, relief=tk.RIDGE)
            frame.pack(pady=5, padx=10)
            frame.configure(highlightbackground="gray", highlightthickness=2)
            
            label = tk.Label(frame, image=self.images[self.slot_counts[i]], bg="lightgray")
            label.pack(side=tk.LEFT, padx=10)
            label.bind("<Button-1>", lambda event, i=i: self.use_spell(i))  # Bind left click to label
            self.labels.append(label)
            
            spell_button = tk.Button(frame, text=f"{i+1}st Level Spells" if i == 0 else f"{i+1}nd Level Spells" if i == 1 else f"{i+1}rd Level Spells", command=lambda i=i: self.show_spell_menu(i), bg="darkgreen", fg="white")
            spell_button.pack(side=tk.RIGHT, padx=10)
            
            spell_label = tk.Label(frame, text="No spells selected", font=("Arial", 10), bg="lightgray")
            spell_label.pack(side=tk.RIGHT, padx=10)
            self.selected_spells_labels.append(spell_label)
        
        self.reset_button = tk.Button(root, text="Reset All", command=self.reset_slots, bg="brown", fg="white")
        self.reset_button.pack(pady=10)
    
    def use_spell(self, level):
        if self.slot_counts[level] > 0:
            self.fade_out(level)
            self.slot_counts[level] -= 1
            self.labels[level].config(image=self.images[self.slot_counts[level]])
            
            # Disable clicking when slots are depleted
            if self.slot_counts[level] == 0:
                self.labels[level].unbind("<Button-1>")
    
    def fade_out(self, level):
        """Creates a fade-out effect while preserving transparency."""
        img = Image.open(image_paths[self.slot_counts[level]]).convert("RGBA")
        
        # Create a transparent background
        background = Image.new("RGBA", img.size, (255, 255, 255, 0))  # Transparent
        
        for alpha in range(100, -1, -5):  # Gradually decrease alpha
            faded = Image.blend(background, img, alpha / 100)  # Blend with transparent bg
            fade_image = ImageTk.PhotoImage(faded.resize((150, 150)))
            
            self.labels[level].config(image=fade_image)
            self.labels[level].image = fade_image  # Prevent garbage collection
            self.root.update()
            time.sleep(0.02)  # Small delay to simulate fading
    
    def show_spell_menu(self, level):
        """Displays a menu of available spells for the selected level and chosen class."""
        menu = tk.Toplevel(self.root)
        menu.title(f"{level+1} Level Spells")
        selected_class = self.character_class.get()
        spells = get_spells_by_level_and_class(level + 1, selected_class) if selected_class != "All Classes" else [spell for spell in spells_data if str(spell["level"]) == str(level + 1)]
        
        for spell in spells:
            tk.Button(menu, text=spell["name"], command=lambda spell=spell, level=level: self.select_spell(spell, level, menu)).pack()
    
    def select_spell(self, spell, level, menu):
        """Handles spell selection, updates the spell label, and closes the menu."""
        if len(sum(self.selected_spells, [])) < 7:  # Limit to 7 total spells
            self.selected_spells[level].append(spell["name"])
            self.selected_spells_labels[level].config(text=", ".join(self.selected_spells[level]))
        menu.destroy()
    
    def reset_slots(self):
        self.slot_counts = self.initial_slots[:]
        for i in range(self.spell_levels):
            self.labels[i].config(image=self.images[self.slot_counts[i]])
            self.selected_spells[i] = []
            self.selected_spells_labels[i].config(text="No spells selected")
            self.labels[i].bind("<Button-1>", lambda event, i=i: self.use_spell(i))  # Re-enable clicking

if __name__ == "__main__":
    root = tk.Tk()
    app = SpellSlotTracker(root)
    root.mainloop()
