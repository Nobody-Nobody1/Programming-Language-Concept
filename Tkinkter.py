import tkinter as tk
from tkinter import filedialog, messagebox
import os

def open_file():
    """Open a file dialog and display the file contents in the text widget."""
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if not file_path:  # User canceled
        return
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        text_area.delete("1.0", tk.END)  # Clear previous content
        text_area.insert(tk.END, content)
        root.title(f"File Viewer - {os.path.basename(file_path)}")
    
    except UnicodeDecodeError:
        messagebox.showerror("Error", "Cannot read file: Unsupported encoding.")
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# Create main window
root = tk.Tk()
root.title("File Viewer")
root.geometry("600x400")

# Create a menu
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

# Create a scrollable text area
text_area = tk.Text(root, wrap="word")
scroll_bar = tk.Scrollbar(root, command=text_area.yview)
text_area.configure(yscrollcommand=scroll_bar.set)

scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
text_area.pack(expand=True, fill=tk.BOTH)

# Run the application
root.mainloop()
