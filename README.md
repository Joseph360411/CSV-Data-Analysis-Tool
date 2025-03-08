

# CSV Data Analysis Tool

This is a Python-based command-line tool for performing various data operations on CSV files, including data cleaning, filtering, sorting, aggregation, transformation, and visualization. It utilizes libraries like `pandas`, `matplotlib`, and `seaborn` to help you analyze and visualize data efficiently.

## Features

- **Load CSV Data**: Load a CSV file into a pandas DataFrame.
- **Data Cleaning**: Handle missing data by dropping or filling with specified values (e.g., mean or custom value).
- **Remove Duplicates**: Remove duplicate rows based on a specific column.
- **Summary Statistics**: Generate descriptive statistics for numeric columns.
- **Data Filtering**: Filter data based on column values.
- **Data Sorting**: Sort data by a specified column.
- **Data Aggregation**: Perform aggregation (mean, sum, count) by grouping data by a column.
- **Mathematical Transformation**: Perform operations (add, subtract, multiply, divide) on columns and create new columns.
- **Visualizations**: Create visualizations such as histograms, pie charts, bar charts, and line graphs for better insights.
- **Save Data**: Save processed data to a new CSV file.

## Installation

To use this tool, you need to have Python installed on your machine along with the necessary dependencies. You can install the required packages using `pip`:

```bash
pip install pandas matplotlib seaborn
```

## Usage

The tool can be executed from the command line by running the script and specifying the required arguments.

### Syntax

```bash
python csv_tool.py <file_path> <operation> [options]
```

### Arguments

- `file`: Path to the input CSV file.
- `operation`: Choose one of the following operations to perform:
  - `summary`: Generate summary statistics.
  - `visualize`: Create visualizations (hist, pie, bar, line).
  - `filter`: Filter data based on column value.
  - `sort`: Sort data by a column.
  - `clean`: Clean missing data (drop or fill).
  - `aggregate`: Aggregate data (mean, sum, count) after grouping.
  - `transform`: Perform a mathematical operation (add, subtract, multiply, divide) on two columns and create a new one.
  - `save`: Save processed data to a new CSV file.

### Options

- `--column`: Column name to be used for various operations.
- `--value`: Value to filter data by.
- `--visualization`: Type of visualization: `hist`, `pie`, `bar`, `line`.
- `--action`: Action for handling missing data (`drop` or `fill`).
- `--fill_value`: Value to fill missing data (e.g., `mean`, `Unknown`).
- `--groupby`: Column to group data by.
- `--aggregation`: Aggregation function for grouping: `mean`, `sum`, `count`.
- `--new_column`: Name of the new column to create.
- `--math_operation`: Mathematical operation for transformation: `divide`, `multiply`, `add`, `subtract`.
- `--columns`: Columns to use for the transformation operation (e.g., for division: `column1 column2`).
- `--output`: Path to save the output CSV file.
- `--modify`: Modify the original file.
- `--show`: Display the output in the terminal.

### Example Commands

1. **Generate Summary Statistics**:
   ```bash
   python csv_tool.py data.csv summary
   ```

2. **Create a Histogram for a Column**:
   ```bash
   python csv_tool.py data.csv visualize --column Age --visualization hist
   ```

3. **Filter Data Based on Column Value**:
   ```bash
   python csv_tool.py data.csv filter --column Department --value "Sales"
   ```

4. **Sort Data by Salary**:
   ```bash
   python csv_tool.py data.csv sort --column Salary
   ```

5. **Handle Missing Data (Fill with Mean)**:
   ```bash
   python csv_tool.py data.csv clean --action fill --fill_value mean
   ```

6. **Save Cleaned Data to New File**:
   ```bash
   python csv_tool.py data.csv clean --action fill --fill_value mean --output cleaned_data.csv
   ```

7. **Aggregate Data by Department and Calculate Mean Salary**:
   ```bash
   python csv_tool.py data.csv aggregate --groupby Department --aggregation mean
   ```

8. **Create a New Column by Adding Two Existing Columns**:
   ```bash
   python csv_tool.py data.csv transform --new_column Total_Salary --math_operation add --columns Salary Bonus
   ```

9. **Save Data to a New File**:
   ```bash
   python csv_tool.py data.csv save --output output_data.csv
   ```

## License

This tool is released under the MIT License.

---
