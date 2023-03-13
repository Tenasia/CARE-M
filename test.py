import tkinter as tk
import webview

root = tk.Tk()

def show_map():
    zoom_level = 20
    file_path =f"my_map.html?zoom={zoom_level}"
    webview.create_window('Google Map', 'mymap.html', width=800, height=800)
    webview.start()

button = tk.Button(root, text='Show Map', command=show_map)
button.pack()

root.mainloop()