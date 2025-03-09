import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
import pandas as pd
import matplotlib.pyplot as plt

class CSVToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Tool")
        self.data = None
        self.root.configure(bg='#121212')

        # Set the window size
        self.root.geometry("800x600")

        # Layout
        self.create_widgets()

    def create_widgets(self):
        # CSV File Section
        self.csv_file_frame = tk.Frame(self.root, bg="#121212", relief="solid", borderwidth=2)
        self.csv_file_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.file_label = tk.Label(self.csv_file_frame, text="CSV File:", font=('Segoe UI', 12), fg="#00c8ff", bg="#121212")
        self.file_label.grid(row=0, column=0, padx=10, sticky="w")

        self.file_entry = tk.Entry(self.csv_file_frame, width=40, font=('Segoe UI', 12), bg="#1e1e1e", fg="#00c8ff", insertbackground="white")
        self.file_entry.grid(row=0, column=1, padx=10, sticky="w")

        self.browse_button = tk.Button(self.csv_file_frame, text="Browse", command=self.browse_file, font=('Segoe UI', 12), bg="#00c8ff", fg="white", relief="flat")
        self.browse_button.grid(row=0, column=2, padx=10, sticky="w")

        # Modify & Output Section
        self.modify_output_frame = tk.Frame(self.root, bg="#121212", relief="solid", borderwidth=2)
        self.modify_output_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.modify_original_var = tk.BooleanVar()
        self.modify_original_checkbox = tk.Checkbutton(self.modify_output_frame, text="Modify the original file", variable=self.modify_original_var, font=('Segoe UI', 12), fg="#00c8ff", bg="#121212")
        self.modify_original_checkbox.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.create_output_var = tk.BooleanVar()
        self.create_output_checkbox = tk.Checkbutton(self.modify_output_frame, text="Create a separate output file", variable=self.create_output_var, font=('Segoe UI', 12), fg="#00c8ff", bg="#121212")
        self.create_output_checkbox.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.show_output_var = tk.BooleanVar()
        self.show_output_checkbox = tk.Checkbutton(self.modify_output_frame, text="Show the output in the GUI", variable=self.show_output_var, font=('Segoe UI', 12), fg="#00c8ff", bg="#121212")
        self.show_output_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Operation Section
        self.operation_frame = tk.Frame(self.root, bg="#121212", relief="solid", borderwidth=2)
        self.operation_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.operation_label = tk.Label(self.operation_frame, text="Operation:", font=('Segoe UI', 12), fg="#00c8ff", bg="#121212")
        self.operation_label.grid(row=0, column=0, padx=10, sticky="w")

        self.operation_combobox = Combobox(self.operation_frame, values=["summary", "visualize", "filter", "sort", "clean", "aggregate", "transform", "save"], font=('Segoe UI', 12))
        self.operation_combobox.grid(row=0, column=1, padx=10, sticky="w")
        self.operation_combobox.bind("<<ComboboxSelected>>", self.update_ui_based_on_operation)

        # Column Section
        self.column_frame = tk.Frame(self.root, bg="#121212", relief="solid", borderwidth=2)
        self.column_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.column_label = tk.Label(self.column_frame, text="Column:", font=('Segoe UI', 12), fg="#00c8ff", bg="#121212")
        self.column_label.grid(row=0, column=0, padx=10, sticky="w")

        self.column_combobox = Combobox(self.column_frame, font=('Segoe UI', 12))
        self.column_combobox.grid(row=0, column=1, padx=10, sticky="w")

        # Value Section (For Filter & Fill)
        self.value_frame = tk.Frame(self.root, bg="#121212", relief="solid", borderwidth=2)
        self.value_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.value_label = tk.Label(self.value_frame, text="Value:", font=('Segoe UI', 12), fg="#00c8ff", bg="#121212")
        self.value_label.grid(row=0, column=0, padx=10, sticky="w")

        self.value_combobox = Combobox(self.value_frame, font=('Segoe UI', 12))
        self.value_combobox.grid(row=0, column=1, padx=10, sticky="w")

        # Fill Value Entry (For Cleaning)
        self.fill_value_entry = tk.Entry(self.value_frame, font=('Segoe UI', 12), bg="#1e1e1e", fg="#00c8ff", insertbackground="white")
        self.fill_value_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.fill_value_entry.grid_forget()  # Hide initially

        # Visualization Section
        self.visualization_frame = tk.Frame(self.root, bg="#121212", relief="solid", borderwidth=2)
        self.visualization_frame.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.visualization_label = tk.Label(self.visualization_frame, text="Visualization Type:", font=('Segoe UI', 12), fg="#00c8ff", bg="#121212")
        self.visualization_label.grid(row=0, column=0, padx=10, sticky="w")

        self.visualization_combobox = Combobox(self.visualization_frame, values=["None", "hist", "pie", "bar", "line"], font=('Segoe UI', 12))
        self.visualization_combobox.grid(row=0, column=1, padx=10, sticky="w")

        # Missing Data Action Section
        self.action_frame = tk.Frame(self.root, bg="#121212", relief="solid", borderwidth=2)
        self.action_frame.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        self.action_label = tk.Label(self.action_frame, text="Missing Data Action:", font=('Segoe UI', 12), fg="#00c8ff", bg="#121212")
        self.action_label.grid(row=0, column=0, padx=10, sticky="w")

        self.action_combobox = Combobox(self.action_frame, values=["None", "drop", "fill"], font=('Segoe UI', 12))
        self.action_combobox.grid(row=0, column=1, padx=10, sticky="w")

        # Aggregation Section
        self.aggregation_frame = tk.Frame(self.root, bg="#121212", relief="solid", borderwidth=2)
        self.aggregation_frame.grid(row=7, column=0, padx=20, pady=10, sticky="ew")

        self.aggregation_label = tk.Label(self.aggregation_frame, text="Aggregation Function:", font=('Segoe UI', 12), fg="#00c8ff", bg="#121212")
        self.aggregation_label.grid(row=0, column=0, padx=10, sticky="w")

        self.aggregation_combobox = Combobox(self.aggregation_frame, values=["None", "mean", "sum", "count"], font=('Segoe UI', 12))
        self.aggregation_combobox.grid(row=0, column=1, padx=10, sticky="w")

        # Transformation Section (New Column Entry)
        self.new_column_frame = tk.Frame(self.root, bg="#121212", relief="solid", borderwidth=2)
        self.new_column_frame.grid(row=8, column=0, padx=20, pady=10, sticky="ew")

        self.new_column_label = tk.Label(self.new_column_frame, text="New Column:", font=('Segoe UI', 12), fg="#00c8ff", bg="#121212")
        self.new_column_label.grid(row=0, column=0, padx=10, sticky="w")

        self.new_column_entry = tk.Entry(self.new_column_frame, font=('Segoe UI', 12), bg="#1e1e1e", fg="#00c8ff", insertbackground="white")
        self.new_column_entry.grid(row=0, column=1, padx=10, sticky="w")

        # Action button section
        self.run_button = tk.Button(self.root, text="Run Operation", command=self.run_operation, font=('Segoe UI', 12), bg="#00c8ff", fg="white", relief="flat")
        self.run_button.grid(row=9, column=0, padx=20, pady=20, columnspan=2)

    def update_ui_based_on_operation(self, event):
        # Enable/Disable widgets based on selected operation
        operation = self.operation_combobox.get()

        # Default: Enable all fields
        self.column_combobox.config(state="normal")
        self.value_combobox.config(state="normal")
        self.fill_value_entry.grid_forget()
        self.value_combobox.grid()

        # Disable checkboxes for non-applicable operations
        if operation in ["summary", "visualize", "save"]:
            self.modify_original_checkbox.config(state="disabled")
            self.create_output_checkbox.config(state="disabled")
            self.show_output_checkbox.config(state="disabled")
        else:
            self.modify_original_checkbox.config(state="normal")
            self.create_output_checkbox.config(state="normal")
            self.show_output_checkbox.config(state="normal")

        if operation == "visualize":
            self.visualization_combobox.config(state="normal")
        elif operation == "filter":
            self.fill_value_entry.grid_forget()
            self.value_combobox.grid()
        elif operation == "clean" and self.action_combobox.get() == "fill":
            self.fill_value_entry.grid(row=1, column=1, padx=10, sticky="w")
            self.value_combobox.grid_forget()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.data = pd.read_csv(file_path)

            # Update comboboxes with actual columns from the file
            columns = ["None"] + list(self.data.columns)
            self.column_combobox['values'] = columns
            self.value_combobox['values'] = columns

    def run_operation(self):
        if self.data is None or self.data.empty:
            messagebox.showerror("Error", "No data loaded.")
            return

        operation = self.operation_combobox.get()
        column = self.column_combobox.get()
        value = self.value_combobox.get()
        fill_value = self.fill_value_entry.get() if self.fill_value_entry.get() else None
        visualization_type = self.visualization_combobox.get()
        aggregation_func = self.aggregation_combobox.get()

        if operation == "summary":
            self.show_summary()
        elif operation == "visualize":
            self.visualize_data(visualization_type)
        elif operation == "filter":
            self.filter_data(column, value)
        elif operation == "sort":
            self.sort_data(column)
        elif operation == "clean":
            self.clean_data(column, aggregation_func, fill_value)
        elif operation == "aggregate":
            self.aggregate_data(column, aggregation_func)
        elif operation == "transform":
            self.transform_data(column)
        elif operation == "save":
            self.save_data()

    def show_summary(self):
        summary = self.data.describe(include="all")
        messagebox.showinfo("Data Summary", str(summary))

    def visualize_data(self, visualization_type):
        if visualization_type == "hist":
            self.data.hist()
        elif visualization_type == "pie":
            self.data.plot.pie(subplots=True, figsize=(10, 6))
        elif visualization_type == "bar":
            self.data.plot.bar(figsize=(10, 6))
        elif visualization_type == "line":
            self.data.plot.line(figsize=(10, 6))

        plt.show()

    def filter_data(self, column, value):
        if column == "None" or value == "None":
            messagebox.showerror("Error", "Please select both a column and value to filter.")
            return

        filtered_data = self.data[self.data[column] == value]
        self.show_output(filtered_data)

    def sort_data(self, column):
        if column == "None":
            messagebox.showerror("Error", "Please select a column to sort.")
            return

        sorted_data = self.data.sort_values(by=column)
        self.show_output(sorted_data)

    def clean_data(self, column, aggregation_func, fill_value):
        if column == "None":
            messagebox.showerror("Error", "Please select a column to clean.")
            return

        if fill_value:
            self.data[column].fillna(fill_value, inplace=True)
        else:
            if aggregation_func != "None":
                self.data[column] = self.data[column].apply(lambda x: aggregation_func)
            self.data[column].dropna(inplace=True)

        self.show_output(self.data)

    def aggregate_data(self, column, aggregation_func):
        if column == "None":
            messagebox.showerror("Error", "Please select a column to aggregate.")
            return

        if aggregation_func == "None":
            messagebox.showerror("Error", "Please select an aggregation function.")
            return

        aggregated_data = self.data.groupby(column).agg(aggregation_func)
        self.show_output(aggregated_data)

    def transform_data(self, column):
        if column == "None":
            messagebox.showerror("Error", "Please select a column to transform.")
            return

        new_column = self.new_column_entry.get()
        if new_column:
            self.data[new_column] = self.data[column].apply(lambda x: x * 2)  # Example transformation
        self.show_output(self.data)

    def show_output(self, output_data):
        if self.show_output_var.get():
            messagebox.showinfo("Data Output", str(output_data))

    def save_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.data.to_csv(file_path, index=False)
            messagebox.showinfo("Data Saved", f"Data saved to {file_path}")

def main():
    root = tk.Tk()
    app = CSVToolApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
