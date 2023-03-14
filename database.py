from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import gmplot

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, PhotoImage

class DataBaseGUI:
    
    X_SIZE_WINDOW = 400
    Y_SIZE_WINDOW = 400

    FONT_SIZE = 16
    FONT_FAMILY = 'Helvetica Bold'

    def __init__(self):
        
        # INITIALIZED VARIABLES
        self.window = tk.Tk()

        # VARIABLES
        self.login_frame, self.login_button, self.username_entry, self.password_entry = self.create_login_frame()
        

    def create_login_frame(self):

        # Initialize variables
        self.window.resizable(False, False)
        self.window.bind('<Return>', self.login)
        self.window.geometry(f'{DataBaseGUI.X_SIZE_WINDOW}x{DataBaseGUI.Y_SIZE_WINDOW}')
        self.window.title('CARE-M Login Page')
        self.center(self.window)

        # Create login frame
        login_frame = tk.Frame(self.window)
        login_frame.pack()

        # Create widgets
        title_label = tk.Label(login_frame, text="CARE-M DATABASE", font=(self.FONT_FAMILY, self.FONT_SIZE))
        username_label = tk.Label(login_frame, text="USERNAME", font=(self.FONT_FAMILY, self.FONT_SIZE))
        password_label = tk.Label(login_frame, text="PASSWORD", font=(self.FONT_FAMILY, self.FONT_SIZE))

        username_info = tk.Entry(login_frame, width=35)
        password_info = tk.Entry(login_frame, width=35, show="*")

        login_button = tk.Button(login_frame, text="LOGIN", font=(self.FONT_FAMILY, self.FONT_SIZE), command=self.login, width=7)

        # Pack widgets
        title_label.pack(pady=(25, 10))
        username_label.pack(pady=(25, 10))
        username_info.pack(pady=(0, 0))
        password_label.pack(pady=(25, 10))
        password_info.pack(pady=(0, 0))
        login_button.pack(pady=(35, 10))

        return login_frame, login_button, username_info, password_info

    def login(self, event=None):

        username = self.username_entry.get()
        password = self.password_entry.get()

        self.login_to_db(username, password)

    def login_to_db(self, username, password):
        self.username = username
        self.password = password

        try:
            db_config = {
                'host': 'localhost',
                'user': username,
                'db': 'care-m'
            }
            
            if password:
                db_config['password'] = password

            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()

        except mysql.connector.Error as error:
            if error.errno == 1045:
                messagebox.showinfo('Invalid', 'Username or Password Incorrect')
            else:
                print(error)
            return

        try:  
            self.login_frame.pack_forget()
            self.create_database_frame() 

            print("Successfully Logged In")
        except Exception as e:
            print("Error occured:", e)
            db.rollback()

    def create_database_frame(self):
 
        self.window.title("Database Table")
        self.window.geometry(f'{925}x{560}')
        self.window.bind('<Return>', self.submit)

        self.center(self.window)

        self.database_frame = tk.Frame(self.window)
        self.database_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # LABELS
        entry_fields = [('Serial ID', 1), ('First Name', 1), ('Last Name', 1), ('Remarks', 1)]

        # Create the labels and Entry widgets in a loop
        for i, (label_text, col) in enumerate(entry_fields):
            label = tk.Label(self.database_frame, text=label_text, width=15, height=2)
            label.grid(row=i, column=0, pady=10, padx=10)
            label.config(font=('Helvetica Bold', 10))
            
            entry = tk.Entry(self.database_frame, width=30)
            entry.grid(row=i, column=col)
            
            # Set the Entry widget as an attribute of the object using the label text as the attribute name
            setattr(self, label_text.lower().replace(' ', '_'), entry)
        
        location_fields = ['Latitude', 'Longitude']

        for i in location_fields:
            label = tk.Label(self.database_frame, text=i, width=15, height=2)
            if i == 'Latitude':
                label.grid(row=4, column=2, pady=10, padx=10)
            else:
                label.grid(row=4, column=0, pady=10, padx=10)
        
        self.longitude = tk.Entry(self.database_frame, width=30)
        self.latitude = tk.Entry(self.database_frame, width=30)

        self.longitude.grid(row=4, column=1)
        self.latitude.grid(row=4, column=3)
        
        # CRUD BUTTONS
        button_names = ['ADD', 'UPDATE', 'DELETE', 'CLEAR FORMS', 'REFRESH TABLE']
        button_commands = [self.submit, self.update, self.delete, self.clear_entries, self.show]

        for i, name in enumerate(button_names):
            button = tk.Button(self.database_frame, text=name, width=15, height=2)
            if name == 'REFRESH TABLE':
                button.grid(row=1, column=3, pady=10, ipadx=25)
            else:
                button.grid(row=i, column=2, padx=25, pady=10, ipadx=25)
            button['command'] = button_commands[i]

        modules_button = tk.Button(self.database_frame, text='MANAGE MODULES', width=15, height=2)
        modules_button.grid(row=0, column=3, padx=25, pady=10, ipadx=25)
        modules_button['command'] = self.create_module_frame
        
        self.matplot_button = tk.Button(self.database_frame, text='GRAPH POINTS', width=15, height=2)
        self.matplot_button.grid(row=2, column=3, padx=25, pady=10, ipadx=25)
        self.matplot_button['command'] = self.create_google_map

        self.create_tree()
        self.tree.bind('<<TreeviewSelect>>', self.update_entry)

        # return database_frame

    def create_tree(self):

        COLUMN_WIDTHS = {
        'ID': 100,
        'SERIAL_ID': 100,
        'FIRST_NAME': 100,
        'SURNAME': 100,
        'DATE_TIME': 125,
        'LONGITUDE': 125,
        'LATITUDE': 125,
        'REMARKS': 100
        }

        column_names = ['ID', 'SERIAL_ID', 'FIRST_NAME', 'SURNAME', 'DATE_TIME', 'LONGITUDE', 'LATITUDE', 'REMARKS']
        columns = tuple(column_names)

        self.tree = ttk.Treeview(
            self.window,
            columns=columns,
            show='headings'
        )

        scrollbar = ttk.Scrollbar(
            self.window,
            orient='vertical',
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(str(column), width=COLUMN_WIDTHS.get(column, 100))

        self.tree.grid(row=5, column=0, sticky=tk.NSEW, padx=(25, 0))
        scrollbar.grid(row=5, column=7, sticky=tk.N + tk.S)

        self.show()

    def create_module_frame(self):
        self.database_frame.grid_forget()

        self.center(self.window)

        self.module_frame = tk.Frame(self.window)
        self.module_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # LABELS
        rename_label = tk.Label(self.module_frame, text='Name Module', width=15, height=2)
        rename_label.grid(row=0, column=0, pady=10, padx=10)
        rename_label.config(font=('Helvetica Bold', 10))

        self.rename = tk.Entry(self.module_frame, width=30)
        self.rename.grid(row=0, column=1)

        modules_button = tk.Button(self.module_frame, text='MANAGE DATABASE', width=15, height=2, command=self.create_database_frame)
        modules_button.grid(row=0, column=3, padx=25, pady=10, ipadx=25)

        refresh_button = tk.Button(self.module_frame, text='REFRESH TABLE', width=15, height=2, command=self.show)
        refresh_button.grid(row=0, column=4, padx=25, pady=10, ipadx=25)
        self.create_tree_module()
        self.tree_module.bind('<<TreeviewSelect>>', self.update_entry)

    def create_tree_module(self):

        COLUMN_WIDTHS = {
        'ID': 100,
        'SERIAL_ID': 100,
        'FIRST_NAME': 100,
        'SURNAME': 100,
        'DATE_TIME': 125,
        'LOC': 125,
        'REMARKS': 100
        }

        column_names = ['ID', 'MODULE_NAME']
        columns = tuple(column_names)

        self.tree_module = ttk.Treeview(
            self.window,
            columns=columns,
            show='headings'
        )

        scrollbar = ttk.Scrollbar(
            self.window,
            orient='vertical',
            command=self.tree_module.yview
        )

        self.tree_module.configure(yscrollcommand=scrollbar.set)

        for column in columns:
            self.tree_module.heading(column, text=column)
            self.tree_module.column(str(column), width=COLUMN_WIDTHS.get(column, 100))

        self.tree_module.grid(row=5, column=0, sticky=tk.NSEW, padx=(25, 0))
        scrollbar.grid(row=5, column=7, sticky=tk.N + tk.S)

        self.show_module()

    def show_module(self):

        # Clears the table
        self.clear_all()

        db = mysql.connector.connect(host='localhost', user=self.username, password=self.password, db='care-m')
        cursor = db.cursor()    

        try:
            query = 'SELECT ID, MODULE_NAME FROM tb_carem_modules'
            cursor.execute(query)
            records = cursor.fetchall()

            for info in records:
                self.tree_module.insert('', tk.END, values=info)
        
        except Exception as e:
            print(e)
            db.rollback()
            db.close()

    def show(self):

        # Clears the table
        self.clear_all()

        db = mysql.connector.connect(host='localhost', user=self.username, password=self.password, db='care-m')
        cursor = db.cursor()    

        try:
            query = 'SELECT ID,SERIAL_ID,FIRST_NAME,SURNAME,DATE_TIME,LONGITUDE,LATITUDE,REMARKS FROM tb_carem'
            cursor.execute(query)
            records = cursor.fetchall()

            for info in records:
                self.tree.insert('', tk.END, values=info)
        
        except Exception as e:
            print(e)
            db.rollback()
            db.close()

    def submit(self, event=None):

        db = mysql.connector.connect(host='localhost', user=self.username, password=self.password, db='care-m')
        cursor = db.cursor()    
        try:
            serial_id = self.serial_id.get()
            surname = self.last_name.get()
            first_name = self.first_name.get()
            remarks = self.remarks.get()
            
            longitude = self.longitude.get()
            latitude = self.latitude.get()
            
            if not serial_id or not surname or not first_name or not remarks or not longitude or not latitude:
                messagebox.showerror('Submit Invalid', 'Please Fill in all the fields.')
            else:
                duplicate = self.check_duplicate(serial_id)
                if duplicate:
                    messagebox.showerror("Error", "Duplicate 'Serial ID' Value Entered, Please Enter A Different Value.")

                query = 'INSERT INTO `tb_carem` (`SERIAL_ID`, `SURNAME`, `FIRST_NAME`,`REMARKS`, `LONGITUDE`, `LATITUDE`) VALUES (%s, %s, %s, %s, %s, %s);'
                values = (str(serial_id), surname, first_name, remarks, longitude, latitude)
                cursor.execute(query, values)

                query_1 = 'SELECT ID,SERIAL_ID,FIRST_NAME,SURNAME,DATE_TIME,LONGITUDE,LATITUDE,REMARKS FROM tb_carem'
                cursor.execute(query_1)
                records = cursor.fetchall()
               
                self.clear_all()
                
                for info in records:
                    self.tree.insert('', 0, text='new item.', values=info)
                db.commit()
                
                messagebox.showinfo('Successful', 'Inserted Data Successfully.')

                self.serial_id.delete(0, tk.END)
                self.last_name.delete(0, tk.END)
                self.first_name.delete(0, tk.END)
                self.remarks.delete(0, tk.END)
                self.longitude.delete(0, tk.END)
                self.latitude.delete(0, tk.END)

                self.serial_id.focus_set()
   
        except mysql.connector.Error as error:
            print("Failed to retrieve column: {}".format(error))

            if error.errno == 1062:
                messagebox.showerror('Adding Invalid', 'Duplicate Serial ID')
            if error.errno == 1416:
                messagebox.showerror('Adding Invalid', 'Serial ID Cannot Contain String')
        finally:
            if db.is_connected():
                cursor.close()
                db.close()
    
    def update(self):
        
        
        serial_id = self.serial_id.get()
        surname = self.last_name.get()
        first_name = self.first_name.get()
        remarks = self.remarks.get()

        longitude = self.longitude.get()
        latitude = self.latitude.get()

        item = self.tree.item(self.tree.focus())

        id = item['values'][0]

        date = item['values'][4]
        db = mysql.connector.connect(host='localhost', user=self.username, password=self.password, db='care-m')
        cursor = db.cursor() 

        
        
        try:
            if not serial_id or not surname or not first_name or not remarks or not longitude or not latitude:
                messagebox.showerror('Update Invalid', 'Please Fill in all the fields.')
            else:

                result = messagebox.askyesno("Warning", "Are you sure you want to update this item?")
                if result:
                    if item:
                        
                        query_1 = "UPDATE tb_carem SET SERIAL_ID=%s, FIRST_NAME=%s, SURNAME=%s, LONGITUDE=%s, LATITUDE=%s REMARKS=%s WHERE id=%s"
                        values = (serial_id, first_name, surname, longitude, latitude, remarks, id)
                        cursor.execute(query_1, values)

                        query_2 = 'SELECT ID,SERIAL_ID,FIRST_NAME,SURNAME,DATE_TIME,LONGITUDE,LATITUDE,REMARKS FROM tb_carem'
                        
                        cursor.execute(query_2)
                        records = cursor.fetchall()

                        self.clear_all()
                        for info in records:
                            self.tree.insert('', tk.END, values=info)

                        db.commit()

                        messagebox.showinfo('Update Successful', f'Item with the ID: {id} was updated.')
                        
                        self.serial_id.delete(0, tk.END)
                        self.last_name.delete(0, tk.END)
                        self.first_name.delete(0, tk.END)
                        self.remarks.delete(0, tk.END)
                        self.longitude.delete(0, tk.END)
                        self.latitude.delete(0, tk.END)

                        # Update the Treeview with the new data
                        self.tree.item(item, values=(id, serial_id, first_name, surname, date, longitude, latitude, remarks))
                
        except mysql.connector.Error as error:
            print("Failed to retrieve column: {}".format(error))

            if error.errno == 1062:
                messagebox.showerror('Update Invalid', 'Duplicate Serial ID')
            if error.errno == 1416:
                messagebox.showerror('Update Invalid', 'Serial ID Cannot Contain String')

        finally:
            if db.is_connected():
                cursor.close()
                db.close()
        

    
    def delete(self):
        
        item = self.tree.selection()[0]
        data = self.tree.item(item)['values']
        
        id = data[0]

        db = mysql.connector.connect(host='localhost', user=self.username, password=self.password, db='care-m')
        cursor = db.cursor() 

        try:
            result = messagebox.askyesno("Warning", "Are you sure you want to delete this item?")

            if result:
                cursor.execute("DELETE FROM tb_carem WHERE ID=%s", (id,))
                db.commit()
                self.tree.delete(item)
                messagebox.showinfo('Delete Successful', f'Item with the ID: {id} was deleted')
            else:
                pass

        except:
            print('Something gone wrong.')

        finally:
            if db.is_connected():
                cursor.close()
                db.close()
    
    def create_google_map(self):
        # Connect to your database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Akosiwilliam47",
            database="care-m"
        )
        c = conn.cursor()

        # Retrieve the latest latitude and longitude data from your database
        c.execute("SELECT LATITUDE, LONGITUDE FROM tb_carem")
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

    def graph_points(self):

        self.matplot_button.config(state=tk.DISABLED)
        
        img = mpimg.imread('pup_map.png')

        locations = self.get_column_as_a_list('LOC')

        x_coordinates = []
        y_coordinates = []

        quadrant_1 = []
        quadrant_2 = []
        quadrant_3 = []
        quadrant_4 = []
        
        for i in locations:
                
            coordinate = i.split(', ')
            x = float(coordinate[0])
            y = float(coordinate[1])

            x_coordinates.append(x)
            y_coordinates.append(y)

            if x >= 0 and y >= 0:
                print('First Quadrant')
                quadrant_1.append((x, y))
            elif x <= 0 and y >= 0:
                print('Second Quadrant')
                quadrant_2.append((x, y))
            elif x <= 0 and y <= 0:
                print('Third Quadrant')
                quadrant_3.append((x, y))
            elif x >= 0 and y <= 0:
                print('Fourth Quadrant')
                quadrant_4.append((x, y))
            else:
                pass

        fig, ax = plt.subplots()

        ax.imshow(img, extent=[-441, 441, -421, 421])
        ax.scatter(x_coordinates, y_coordinates, c='black')
        ax.set_xlim(-350, 350)
        ax.set_ylim(-350, 350)
        ax.axhline(y=0, color='gray', linestyle='--')
        ax.axvline(x=0, color='gray', linestyle='--')

        plt.show()

        self.matplot_button.config(state=tk.NORMAL)
        
    def clear_all(self):

        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def clear_entries(self):

        self.serial_id.delete(0, tk.END)
        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.longitude.delete(0, tk.END)
        self.latitude.delete(0, tk.END)
        self.remarks.delete(0, tk.END)

    def update_entry(self, event):

        selected_item = self.tree.focus()

        serial_id = self.tree.item(selected_item)['values'][1]
        first_name = self.tree.item(selected_item)['values'][2]
        surname = self.tree.item(selected_item)['values'][3]
        longitude = self.tree.item(selected_item)['values'][5]
        latitude = self.tree.item(selected_item)['values'][6]
        remarks = self.tree.item(selected_item)['values'][7]

        self.serial_id.delete(0, tk.END)
        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.longitude.delete(0, tk.END)
        self.latitude.delete(0, tk.END)
        self.remarks.delete(0, tk.END)
        
        self.serial_id.insert(0, serial_id)
        self.first_name.insert(0, first_name)
        self.last_name.insert(0, surname)
        self.longitude.insert(0, longitude)
        self.latitude.insert(0, latitude)
        self.remarks.insert(0, remarks)

    def check_duplicate(self, value):

        try:
            # Connect to the database
            db = mysql.connector.connect(
                host="localhost",
                user=self.username,
                password=self.password,
                database='care-m'
            )
            mycursor = db.cursor()
            
            # check if value already exists in the table
            sql = "SELECT 1 FROM tb_carem WHERE SERIAL_ID = %s"
            mycursor.execute(sql, (value))
            result = mycursor.fetchone()
            
            if result:
                return True
            else:
                return False

        except mysql.connector.Error as error:
            print("Failed to check duplicate value: {}".format(error))

        finally:
            if db.is_connected():
                mycursor.close()
                db.close()

    def get_column_as_a_list(self, column):

        try:
            db = mysql.connector.connect(
                host="localhost",
                user=self.username,
                password=self.password,
                database='care-m'
            )
            mycursor = db.cursor()
            
            # Retrieve the specified column from the table
            sql = "SELECT {} FROM tb_carem".format(column)
            mycursor.execute(sql)
            result = mycursor.fetchall()

            # Convert the result to a list
            column_list = [row[0] for row in result]


            return column_list

        except mysql.connector.Error as error:
            print("Failed to retrieve column: {}".format(error))
        finally:
            if db.is_connected():
                mycursor.close()
                db.close()

    def center(self, win):

        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width

        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2

        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        win.deiconify()

def main():

    program = DataBaseGUI()
    program.window.mainloop()

if __name__ == '__main__':
    main()

