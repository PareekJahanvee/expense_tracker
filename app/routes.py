from flask import Blueprint, render_template, request, redirect, url_for
import json
from datetime import datetime

routes = Blueprint('routes', __name__)

# File path for storing expenses
EXPENSE_FILE = 'data/expenses.txt'


# Helper function to read expenses from file
def read_expenses():
    try:
        with open(EXPENSE_FILE, 'r') as file:
            expenses = [json.loads(line) for line in file]
        expenses.sort(key=lambda x: x['date'])
    except FileNotFoundError:
        expenses = []
    return expenses

# Helper function to write expense to file
def write_expense(expense):
    try:
        expenses = read_expenses()
        if expenses:
            max_id = max(int(exp['id']) for exp in expenses if 'id' in exp)
        
        else:
            max_id=0
    except (ValueError,KeyError):
        max_id=0
    expense['id']= max_id + 1
    with open(EXPENSE_FILE, 'a') as file:
        file.write(json.dumps(expense) + '\n')

# Redirect the root URL to the home page
@routes.route('/')
def root_redirect():
    return redirect(url_for('routes.home'))  # Redirect root URL to /home

@routes.route('/home')
def home():
    return render_template('home.html')

@routes.route('/dashboard')
def dashboard():
    expenses = read_expenses()  # Read expenses from the file
    filter_date = request.args.get('filter_date')

    if filter_date:
        expenses = [exp for exp in expenses if exp['date'] == filter_date]
    return render_template('index.html', expenses=expenses)

@routes.route('/index')
def index():
    expenses = read_expenses()  # Read expenses from the file
    return render_template('index.html', expenses=expenses)

@routes.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']

        # Create a new expense entry as a dictionary
        new_expense = {
            'id': str(int(datetime.timestamp(datetime.now()))),  # Unique ID using timestamp
            'title': title,
            'amount': float(amount),  # Ensure amount is a float
            'category': category,
            'date': date,  # The date should already be in a proper format (YYYY-MM-DD)
        }

        # Write the expense to the file
        write_expense(new_expense)

        # Redirect to the index page to display the updated expenses
        return redirect(url_for('routes.index'))
    
    return render_template('add_expense.html')

# New route for Pie Chart
@routes.route('/pie_chart')
def pie_chart():
    # Read the expenses from the file
    expenses = read_expenses()

    # Group expenses by category and calculate the total amount for each category
    categories = set(expense['category'] for expense in expenses)  # Get unique categories
    labels = list(categories)  # List of unique expense categories
    values = [
        sum(float(expense['amount']) for expense in expenses if expense['category'] == category)
        for category in labels
    ]

    # Pass the labels and values to the template
    return render_template('pie_chart.html', labels=labels, values=values)

@routes.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    expenses = read_expenses()
    expenses = [exp for exp in expenses if int(exp.get('id',-1)) != id]
    with open(EXPENSE_FILE, 'w') as f:
        for exp in expenses:
            f.write(json.dumps(exp) + '\n')
    return redirect(url_for('routes.index'))
