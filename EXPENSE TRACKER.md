EXPENSE TRACKER

A lightweight web application for tracking personal expenses, built with **Python, Flask and SQLite**.

I built this project to understand how a backend server talks to a database, how HTML forms send data to routes, and how to validate user input properly.

---

OVERVIEW

Most people lose track of small daily spends like tea, auto fare and snacks. This app gives a simple place to record every expense and instantly see where the money is going, both as a total and category by category.

FEATURES

- **Add expenses** with title, amount, category and date
- **Delete expenses** that were added by mistake
- **Live total** of all spending shown at the top
- **Category-wise summary** using SQL aggregation
- **Input validation** on both the browser side (HTML attributes) and the server side (Python checks)
- **Persistent storage**, so data stays saved after the server restarts
- **Safe database queries** using parameterized SQL to prevent SQL injection

TECH STACK

| Layer      | Technology                         |
|------------|------------------------------------|
| Language   | Python 3                           |
| Framework  | Flask                              |
| Database   | SQLite (via the built-in `sqlite3`)|
| Frontend   | HTML, CSS, Jinja2 templating       |

PROJECT STRUCTURE

```
python-expense-tracker/
├── app.py          # Flask app: routes, database logic, HTML template
├── README.md       # Project documentation
├── .gitignore      # Keeps the local database out of version control
└── expenses.db     # SQLite database (auto-created on first run)
```

DATABASE SCHEME

Single table: `expenses`

| Column     | Type    | Description                     |
|------------|---------|---------------------------------|
| `id`       | INTEGER | Primary key, auto-incremented   |
| `title`    | TEXT    | What the money was spent on     |
| `amount`   | REAL    | Amount spent                    |
| `category` | TEXT    | Food, Travel, Shopping, etc.    |
| `spent_on` | TEXT    | Date of the expense (YYYY-MM-DD)|

ROUTES

| Method | Route            | Purpose                                         |
|--------|------------------|-------------------------------------------------|
| GET    | `/`              | Show all expenses, total and category summary   |
| POST   | `/add`           | Validate form data and insert a new expense     |
| POST   | `/delete/<id>`   | Delete the expense with the given id            |

HOW ITS WORK

1. The user fills the form and clicks **Add**.
2. The browser sends a `POST` request to `/add`.
3. Flask reads the form data, validates the title and amount, and inserts a row into SQLite using a parameterized query.
4. Flask redirects back to `/`, which reads all rows, computes totals with `GROUP BY category`, and renders the page using Jinja2.

GETTING STARTED

 PREREQUISITES

- Python 3.8 or higher
- pip

INSTALLISATION

```bash
# 1. Clone the repository
git clone https://github.com/Sathishkumar252/python-expense-tracker.git

# 2. Move into the project folder
cd python-expense-tracker

# 3. Install the dependency
pip install flask

# 4. Run the app
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

WHAT I LEARNED

- Building routes and handling `GET` and `POST` requests in Flask
- Designing a simple relational table and writing CRUD queries in SQL
- Using `GROUP BY` and `SUM` to build summaries
- Validating input on the server instead of trusting the browser
- Preventing SQL injection with parameterized queries
- Using Git and GitHub to version a project

FUTURE IMPROVEMENTS

- [ ] Edit an existing expense
- [ ] Filter expenses by month
- [ ] Export expenses to CSV
- [ ] User login and separate accounts
- [ ] Charts for monthly spending

AUTHOR

**M.SATHISHKUMAR**
GitHub: [@Sathishkumar252](https://github.com/Sathishkumar252)