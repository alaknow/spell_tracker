import tkinter as tk
from PIL import Image, ImageTk

# Paths to spell slot images (ordered from full to empty)
image_paths = [
    "/mnt/data/Druid4.png",
    "/mnt/data/Druid3.png",
    "/mnt/data/Druid2.png",
    "/mnt/data/Druid1.png",
    "/mnt/data/Druid0.png"
]

class SpellSlotTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Spell Slot Tracker")
        
        self.spell_levels = 3  # Number of spell levels to track
        self.slot_counts = [len(image_paths) - 1] * self.spell_levels  # Max slots per level
        self.images = [ImageTk.PhotoImage(Image.open(path).resize((150, 150))) for path in image_paths]
        
        self.labels = []
        self.buttons = []
        
        for i in range(self.spell_levels):
            frame = tk.Frame(root)
            frame.pack()
            
            label = tk.Label(frame, image=self.images[self.slot_counts[i]])
            label.pack(side=tk.LEFT)
            self.labels.append(label)
            
            button = tk.Button(frame, text=f"Use Level {i+1} Spell Slot", command=lambda i=i: self.use_spell(i))
            button.pack(side=tk.LEFT)
            self.buttons.append(button)
        
        self.reset_button = tk.Button(root, text="Reset All", command=self.reset_slots)
        self.reset_button.pack()
    
    def use_spell(self, level):
        if self.slot_counts[level] > 0:
            self.slot_counts[level] -= 1
            self.labels[level].config(image=self.images[self.slot_counts[level]])
    
    def reset_slots(self):
        self.slot_counts = [len(image_paths) - 1] * self.spell_levels
        for i in range(self.spell_levels):
            self.labels[i].config(image=self.images[self.slot_counts[i]])

if __name__ == "__main__":
    root = tk.Tk()
    app = SpellSlotTracker(root)
    root.mainloop()