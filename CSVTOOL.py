import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def handle_missing_data(data, action, fill_value="Unknown"):
    data = data.copy()
    if action == "drop":
        return data.dropna()
    elif action == "fill":
        if fill_value == "mean":
            for column in data.select_dtypes(include=['float64', 'int64']):
                mean_value = data[column].mean()
                if pd.notna(mean_value):
                    data[column] = data[column].fillna(mean_value)
        else:
            data.fillna(fill_value, inplace=True)
        return data
    else:
        print("Invalid action for missing data. Use 'drop' or 'fill'.")
        return data

def remove_duplicates(data, column):
    if column not in data.columns:
        print(f"Error: Column '{column}' not found in dataset.")
        return data
    return data.drop_duplicates(subset=[column])

def summary_statistics(data):
    print("Summary Statistics:\n", data.describe())

def plot_histogram(data, column):
    if column in data.columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(data[column], bins=20, kde=True)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()
    else:
        print("Column not found in dataset.")

def plot_pie_chart(data, column):
    if column in data.columns:
        plt.figure(figsize=(6, 6))
        data[column].value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
        plt.title(f'Pie Chart of {column}')
        plt.ylabel('')
        plt.show()
    else:
        print("Column not found in dataset.")

def plot_bar_chart(data, column):
    if column in data.columns:
        plt.figure(figsize=(8, 5))
        sns.countplot(x=data[column])
        plt.title(f'Bar Chart of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()
    else:
        print("Column not found in dataset.")

def plot_line_graph(data, column):
    if column in data.columns:
        if pd.api.types.is_numeric_dtype(data[column]):
            plt.figure(figsize=(8, 5))
            sns.lineplot(data=data, x=data.index, y=column)
            plt.title(f'Line Graph of {column}')
            plt.xlabel('Index')
            plt.ylabel(column)
            plt.show()
        else:
            print(f"Column {column} is not numeric, cannot plot a line graph.")
    else:
        print("Column not found in dataset.")

def filter_data(data, column, value):
    if column in data.columns:
        return data[data[column] == value]
    else:
        print("Column not found in dataset.")
        return data

def sort_data(data, column):
    if column in data.columns:
        return data.sort_values(by=column)
    else:
        print("Column not found in dataset.")
        return data

def aggregate_data(data, groupby_column, aggregation_func):
    if groupby_column in data.columns:
        if aggregation_func == "mean":
            return data.groupby(groupby_column).mean()
        elif aggregation_func == "sum":
            return data.groupby(groupby_column).sum()
        elif aggregation_func == "count":
            return data.groupby(groupby_column).count()
        else:
            print(f"Unsupported aggregation function: {aggregation_func}")
            return data
    else:
        print("Column not found in dataset.")
        return data

def transform_data(data, new_column, operation, columns):
    if len(columns) != 2:
        print("Error: Transformation requires exactly two columns.")
        return data
    
    col1, col2 = columns
    if col1 not in data.columns or col2 not in data.columns:
        print(f"Error: Columns {col1} or {col2} not found in dataset.")
        return data
    
    if operation == "divide":
        if (data[col2] == 0).any():
            print(f"Error: Division by zero detected in column {col2}.")
            return data
        data[new_column] = data[col1] / data[col2]
    elif operation == "multiply":
        data[new_column] = data[col1] * data[col2]
    elif operation == "add":
        data[new_column] = data[col1] + data[col2]
    elif operation == "subtract":
        data[new_column] = data[col1] - data[col2]
    else:
        print(f"Unsupported operation: {operation}")
    return data

def save_data(data, output_file):
    data.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='CLI Data Analysis Tool')
    parser.add_argument('file', help='Path to the CSV file')
    parser.add_argument('operation', choices=['summary', 'visualize', 'filter', 'sort', 'clean', 'aggregate', 'transform', 'save'], help='Operation to perform')
    parser.add_argument('--column', type=str, help='Column name for various operations')
    parser.add_argument('--value', type=str, help='Value for filtering data')
    parser.add_argument('--visualization', choices=['hist', 'pie', 'bar', 'line'], help='Type of visualization to display')
    parser.add_argument('--action', choices=['drop', 'fill'], help='Action for handling missing data')
    parser.add_argument('--fill_value', type=str, default="Unknown", help='Fill value for missing data (used with "fill" action)')
    parser.add_argument('--groupby', type=str, help='Column name for grouping data')
    parser.add_argument('--aggregation', choices=['mean', 'sum', 'count'], help='Aggregation function for groupby')
    parser.add_argument('--new_column', type=str, help='New column to create')
    parser.add_argument('--math_operation', choices=['divide', 'multiply', 'add', 'subtract'], help='Mathematical operation for column transformation')
    parser.add_argument('--columns', nargs=2, type=str, help='Columns for transformation operation (e.g., for divide: column1 column2)')
    parser.add_argument('--output', type=str, help='Path to save the processed data')
    parser.add_argument('--modify', action='store_true', help='Modify the original file')
    parser.add_argument('--show', action='store_true', help='Show the output in terminal')

    args = parser.parse_args()
    data = load_data(args.file)

    if data is not None:
        if args.operation == 'summary':
            summary_statistics(data)
        elif args.operation == 'visualize' and args.column and args.visualization:
            if args.visualization == 'hist':
                plot_histogram(data, args.column)
            elif args.visualization == 'pie':
                plot_pie_chart(data, args.column)
            elif args.visualization == 'bar':
                plot_bar_chart(data, args.column)
            elif args.visualization == 'line':
                plot_line_graph(data, args.column)
        elif args.operation == 'filter' and args.column and args.value:
            print(filter_data(data, args.column, args.value))
        elif args.operation == 'sort' and args.column:
            print(sort_data(data, args.column))
        elif args.operation == 'clean' and args.action:
            cleaned_data = handle_missing_data(data, args.action, args.fill_value)
            if args.modify:
                save_data(cleaned_data, args.file)  
            if args.output:
                save_data(cleaned_data, args.output)  
            if args.show:
                print("Cleaned Data:\n", cleaned_data)  
        elif args.operation == 'aggregate' and args.groupby and args.aggregation:
            print(aggregate_data(data, args.groupby, args.aggregation))
        elif args.operation == 'transform' and args.new_column and args.math_operation and args.columns:
            print(transform_data(data, args.new_column, args.math_operation, args.columns))
        elif args.operation == 'save' and args.output:
            save_data(data, args.output)

if __name__ == '__main__':
    main()
