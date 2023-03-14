import tkinter as tk
import mysql.connector
from gmplot import gmplot

def create_google_map():
    # Connect to your database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Akosiwilliam47",
        database="college"
    )
    c = conn.cursor()

    # Retrieve the latest latitude and longitude data from your database
    c.execute("SELECT LATITUDE, LONGITUDE FROM tb_test")
    data = c.fetchall()

    # Create a new map centered on the first point in your data
    gmap = gmplot.GoogleMapPlotter(data[0][0], data[0][1], 13)

    # Plot a single marker for each point in the data
    for point in data:
        gmap.marker(point[0], point[1])

    # Draw the map and save it to an HTML file
    gmap.draw("emergency_points.html")

    # Open the map in your web browser
    import webbrowser
    webbrowser.open_new_tab('emergency_points.html')

root = tk.Tk()

button = tk.Button(root, text="Create Map", command=create_google_map)
button.pack()

root.mainloop()