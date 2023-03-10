import tkinter as tk


class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Main Application")
        self.root.geometry("400x400")
        self.root.configure(background="white")

        self.create_database_frame = tk.Frame(self.root, background="red")
        self.create_database_frame.grid(row=0, column=0, sticky="nsew")

        self.create_modules_frame = tk.Frame(self.root, background="green")
        self.create_modules_frame.grid(row=0, column=0, sticky="nsew")

        # Create "Modules" button that switches to the CreateModulesFrame
        self.modules_button = tk.Button(self.root, text="Modules", command=self.show_modules_frame)
        self.modules_button.grid(row=1, column=0, padx=10, pady=10)

        # Create "Database" button that switches to the CreateDatabaseFrame
        self.database_button = tk.Button(self.root, text="Database", command=self.show_database_frame)

    def show_modules_frame(self):
        # Hide the CreateDatabaseFrame and show the CreateModulesFrame
        self.create_database_frame.grid_forget()
        self.create_modules_frame.grid(row=0, column=0, sticky="nsew")

        # Hide the "Modules" button
        self.modules_button.grid_forget()

        # Show the "Database" button
        self.database_button.grid(row=1, column=0, padx=10, pady=10)

    def show_database_frame(self):
        # Hide the CreateModulesFrame and show the CreateDatabaseFrame
        self.create_modules_frame.grid_forget()
        self.create_database_frame.grid(row=0, column=0, sticky="nsew")

        # Hide the "Database" button
        self.database_button.grid_forget()

        # Show the "Modules" button
        self.modules_button.grid(row=1, column=0, padx=10, pady=10)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApplication()
    app.run()