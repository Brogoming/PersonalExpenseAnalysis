# Personal Expense Analysis

The purpose of this project is to empower individuals to take control of their finances by analyzing their spending
habits. It uses Pandas for data handling, Matplotlib for visualizations, and NumPy for efficient numerical computations.
The tool can graph trends, predict future expenses, and suggest cutbacks to help users manage their finances more
effectively.

Whether you're budgeting for the first time or trying to improve your financial health, this tool helps you visualize
spending patterns, forecast future spending, and identify areas where you can save.

![Python Version](https://img.shields.io/badge/python-3.12-blue)
![Project Started](https://img.shields.io/badge/Project%20Started-July%207%2C%202025-orange)

## Index

- [Instructions](#instructions)
- [Import File Rules](#import-file-rules)
- [Tabs](#tabs)
- [Features](#features)
- [Future Plans](#future-plans-maybe)
- [Milestones](#-milestones)
- [Developers](#developers)

## Instructions

1. Install all the necessary Python packages from the requirements.txt file
2. Run the program from the main.py file
    1. At this point the GUI should pop up
3. Go over to the file option the menu bar and click on it, two options should show up
    1. **Import** - By selecting this you are prompted to import the necessary csv file, make sure it is in the right
       format. Go to [Import File Rules](#import-file-rules) for more instructions
    2. **Exit** - By selecting this it closes the program
4. Once you import the file, if evey thing is set up correctly you should see a tab of the file you imported. That tab
   has subtabs:
    - [Original Table](#original-table)
    - [Modified Table](#modified-table)
    - [Account Overview](#account-overview)
    - [Spent Overview](#spent-overview)
    - [Earned Overview](#earned-overview)
5. By clicking into any of these you can see the data represented in tables and graphs

## Import File Rules

Follow these rules in order to make the application work.

1. Create a csv file, no other file type will work at this moment
2. Use the following example as your header

   | Dates | Amount | Tag | Optional Tag | Account |
         |-------|--------|-----|--------------|---------|

3. Fill in the data
    - Dates - Put valid dates in this format mm/dd/yyyy. `Example: 2/24/2025`.
    - Amount - Either positive or negative numbers, the Spent and Earned numbers will be automatically formatted but the
      Transfer amount will not so be aware of those.
    - Tag - Use one of 3 tags per row `Spent, Earned, Transfer`.
    - Optional Tag - You can leave this blank, but you can put what ever extra tag in to better see what you spent or
      how you get your earnings `Example: Groceries, Movies, Utilities, etc...`.
    - Account - Name of an account `Example: Checking, Savings, 401k, etc...`.

### Example Table

| Dates     | Amount | Tag      | Optional Tag | Account  |
|-----------|--------|----------|--------------|----------|
| 1/1/2025  | 100    | Earned   | Work         | Savings  |
| 1/2/2025  | 50     | Earned   | Work         | Checking |
| 1/10/2025 | 25     | Spent    | Groceries    | Checking |
| 1/14/2025 | -25    | Transfer |              | Savings  |
| 1/20/2025 | 25     | Transfer |              | Checking |
| 1/25/2025 | 50     | Spent    | Utilities    | Checking |

## Tabs

### Original Table

This tab basically shows you the csv file you imported in a table view.

### Modified Table

This tab spreads out the data from the original file in Spent, Earned, Transferred, and Account totals for each account
for every day between the first day and the last day in the file.

### Account Overview

This tab shows a line graph representing the amount of each accounts over time. This also uses Linear Regression to help
predict then next 6 months.

### Spent Overview

This tab shows both a bar graph and a pie chart on what was spent.
The bar graph shows what was spent per month.
The pie chart shows the percentage of what was spent between the first day and the last day in the file.

### Earned Overview

This tab shows both a bar graph and a pie chart on what was earned.
The bar graph shows what type of earnings per month.
The pie chart shows the percentage of the different types of earnings between the first day and the last day in the
file.

## Features

- You can import multiple files, just not at the same time.
- If you hover your curser over the graph it will tell you the value of that spot.

## Future Plans (Maybe)

- Be able to edit table cells in the [Original Table](#original-table)
- Be able to add rows to the [Original Table](#original-table)
- Be able to close file tabs
- Give the use more options and setting to configure like starting account amounts or length of prediction
- Graph animations
- Export menu option
- Dark mode
- Better error handling
- More file import options
- Have an instructions button
- Have a template button

## 📌 Milestones

### ✅ Milestone 1: Project Setup

- [x] Set up project directory and virtual environment
- [x] Create `requirements.txt` for dependencies
- [x] Initialize Git repo and create `README.md`

### 📊 Milestone 2: Expense Data Handling

- [x] Define a standard CSV format or accept user-uploaded data
- [x] Use Pandas to read, clean, and categorize expenses
- [x] Summarize expenses by category and month
- [x] Implement handling for missing or malformed data

### 📈 Milestone 3: Visualizations

- [x] Line chart of monthly expenses over time
- [x] Pie charts of spending and income by category
- [x] Bar chart comparing months/categories for spending and income

### 🔮 Milestone 4: Expense Forecasting

- [x] Use moving averages or linear regression to predict next 6 months' expenses

### 💾 Milestone 5: User Interface & Experience

- [X] Build a simple CLI or GUI (e.g., Streamlit or Tkinter)
- [X] Allow importing new data without overwriting old analysis
- [X] User can hover over a data point and tells them the exact value

### 🧪 Milestone 6: Testing and Final Touches

- [X] Add usage instructions to `README.md`
- [X] Polish codebase (comments, docstrings, clean structure)

# Developers:

- [Dakota Gullicksen](https://www.linkedin.com/in/dakota-w-gullicksen/)