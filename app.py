from datetime import date
import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "expenses.db"


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            spent_on TEXT NOT NULL
        )"""
    )
    conn.commit()
    conn.close()


PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Expense Tracker</title>
  <style>
    :root {
      --bg: #f4f7fb;
      --card: #ffffff;
      --primary: #4f46e5;
      --primary-dark: #3730a3;
      --accent: #14b8a6;
      --danger: #ef4444;
      --text: #1f2937;
      --muted: #6b7280;
      --border: #e5e7eb;
      --shadow: 0 18px 38px rgba(15, 23, 42, 0.08);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: linear-gradient(135deg, #eef2ff, #f8fafc 40%, #ecfeff);
      color: var(--text);
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 40px 20px 60px;
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      margin-bottom: 28px;
      flex-wrap: wrap;
    }

    h1 {
      margin: 0;
      font-size: clamp(2rem, 3vw, 2.8rem);
      color: var(--text);
    }

    .tag {
      background: rgba(79, 70, 229, 0.12);
      color: var(--primary-dark);
      padding: 8px 14px;
      border-radius: 999px;
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 18px;
      margin-bottom: 24px;
    }

    .stat-card, .panel {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 18px;
      box-shadow: var(--shadow);
    }

    .stat-card {
      padding: 20px;
    }

    .stat-label {
      color: var(--muted);
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 12px;
      font-weight: 700;
    }

    .stat-value {
      font-size: clamp(1.8rem, 3vw, 2.5rem);
      font-weight: 800;
      margin: 0;
    }

    .stat-value.green { color: #0f9f6e; }
    .stat-value.blue { color: var(--primary); }
    .stat-value.orange { color: #f59e0b; }

    .panel {
      padding: 22px;
      margin-bottom: 24px;
    }

    .panel h2 {
      margin: 0 0 16px;
      font-size: 1.2rem;
    }

    form.add-form {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 12px;
    }

    input, select, button {
      width: 100%;
      border-radius: 12px;
      border: 1px solid var(--border);
      padding: 12px 14px;
      font-size: 0.98rem;
    }

    input:focus, select:focus {
      outline: 3px solid rgba(79, 70, 229, 0.12);
      border-color: var(--primary);
    }

    button {
      border: none;
      cursor: pointer;
      transition: transform 0.2s ease, opacity 0.2s ease;
      font-weight: 700;
    }

    button:hover {
      transform: translateY(-1px);
      opacity: 0.97;
    }

    .primary-btn {
      background: linear-gradient(135deg, var(--primary), var(--primary-dark));
      color: white;
    }

    .danger-btn {
      background: linear-gradient(135deg, #f87171, var(--danger));
      color: white;
      padding: 10px 12px;
      width: auto;
      min-width: 52px;
    }

    .summary-list {
      list-style: none;
      padding: 0;
      margin: 16px 0 0;
      display: grid;
      gap: 10px;
    }

    .summary-list li {
      display: flex;
      justify-content: space-between;
      padding: 10px 12px;
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 10px;
    }

    .summary-list .category {
      font-weight: 700;
    }

    .message {
      margin-top: 14px;
      padding: 12px 14px;
      border-radius: 10px;
      font-weight: 600;
    }

    .message.error {
      background: #fee2e2;
      color: #991b1b;
      border: 1px solid #fecaca;
    }

    .message.success {
      background: #dcfce7;
      color: #166534;
      border: 1px solid #bbf7d0;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 8px;
    }

    th, td {
      text-align: left;
      padding: 14px 12px;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }

    th {
      color: var(--muted);
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      background: #f8fafc;
    }

    .pill {
      display: inline-block;
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(20, 184, 166, 0.12);
      color: #0f766e;
      font-weight: 700;
      font-size: 0.78rem;
    }

    .empty {
      color: var(--muted);
      text-align: center;
      padding: 18px 12px;
    }

    @media (max-width: 640px) {
      .topbar {
        flex-direction: column;
        align-items: flex-start;
      }

      th, td {
        padding: 10px 8px;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="topbar">
      <h1>Expense Tracker</h1>
      <div class="tag">Smart budget</div>
    </div>

    <div class="grid">
      <div class="stat-card">
        <div class="stat-label">Total spend</div>
        <p class="stat-value green">Rs. {{ "%.2f"|format(grand) }}</p>
      </div>
      <div class="stat-card">
        <div class="stat-label">This month</div>
        <p class="stat-value blue">Rs. {{ "%.2f"|format(month_total) }}</p>
      </div>
      <div class="stat-card">
        <div class="stat-label">Transactions</div>
        <p class="stat-value orange">{{ rows|length }}</p>
      </div>
    </div>

    <div class="panel">
      <h2>Add New Expense</h2>
      <form class="add-form" method="post" action="/add">
        <input name="title" placeholder="Expense title" required>
        <input name="amount" type="number" step="0.01" min="0.01" placeholder="Amount" required>
        <select name="category">
          <option value="Food">Food</option>
          <option value="Travel">Travel</option>
          <option value="Shopping">Shopping</option>
          <option value="Bills">Bills</option>
          <option value="Other">Other</option>
        </select>
        <input name="spent_on" type="date" value="{{ today }}">
        <button class="primary-btn" type="submit">Add Expense</button>
      </form>

      {% if error %}
        <div class="message error">{{ error }}</div>
      {% endif %}

      {% if success %}
        <div class="message success">{{ success }}</div>
      {% endif %}
    </div>

    <div class="panel">
      <h2>Category Breakdown</h2>
      {% if totals %}
      <ul class="summary-list">
        {% for t in totals %}
          <li>
            <span class="category">{{ t.category }}</span>
            <strong>Rs. {{ "%.2f"|format(t.total) }}</strong>
          </li>
        {% endfor %}
      </ul>
      {% else %}
      <p class="empty">Add your first expense to see the breakdown.</p>
      {% endif %}
    </div>

    <div class="panel">
      <h2>Recent Expenses</h2>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Title</th>
            <th>Category</th>
            <th>Amount</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {% for r in rows %}
          <tr>
            <td>{{ r.spent_on }}</td>
            <td>{{ r.title }}</td>
            <td><span class="pill">{{ r.category }}</span></td>
            <td>Rs. {{ "%.2f"|format(r.amount) }}</td>
            <td>
              <form method="post" action="/delete/{{ r.id }}">
                <button class="danger-btn" type="submit" aria-label="Delete expense">Delete</button>
              </form>
            </td>
          </tr>
          {% else %}
          <tr><td colspan="5" class="empty">No expenses added yet.</td></tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
"""


@app.route("/")
def home():
    return show_page()


def show_page(error=None, success=None):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM expenses ORDER BY spent_on DESC, id DESC"
    ).fetchall()
    totals = conn.execute(
        "SELECT category, SUM(amount) AS total FROM expenses GROUP BY category ORDER BY total DESC"
    ).fetchall()
    month_total = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM expenses WHERE spent_on >= ?",
        (date.today().replace(day=1).isoformat(),),
    ).fetchone()["total"]
    conn.close()

    grand = sum(float(r["amount"]) for r in rows)
    return render_template_string(
        PAGE,
        rows=rows,
        totals=totals,
        grand=grand,
        month_total=month_total,
        today=date.today().isoformat(),
        error=error,
        success=success,
    )


@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "Other").strip() or "Other"
    spent_on = request.form.get("spent_on") or date.today().isoformat()

    try:
        amount = float(request.form.get("amount", ""))
    except (TypeError, ValueError):
        return show_page(error="Please enter a valid numeric amount.")

    if not title:
        return show_page(error="Expense title is required.")

    if amount <= 0:
        return show_page(error="Amount must be greater than zero.")

    try:
        date.fromisoformat(spent_on)
    except ValueError:
        return show_page(error="Please provide a valid date.")

    conn = get_db()
    conn.execute(
        "INSERT INTO expenses (title, amount, category, spent_on) VALUES (?, ?, ?, ?)",
        (title, amount, category, spent_on),
    )
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)