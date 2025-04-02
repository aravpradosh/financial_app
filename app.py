from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

df_income = pd.DataFrame(columns=["Category", "Particulars", "Amount"])  # Category: Revenue, COGS, Expenses
df_balance = pd.DataFrame(columns=["Category", "Particulars", "Amount"])  # Category: Asset, Liability, Equity

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/income_statement', methods=['GET', 'POST'])
def income_statement():
    global df_income
    if request.method == 'POST':
        category = request.form.get('category')  # Revenue, COGS, Expenses
        particular = request.form.get('particular')
        amount = request.form.get('amount')

        if category and particular and amount:
            try:
                amount = float(amount)
                new_entry = pd.DataFrame({"Category": [category], "Particulars": [particular], "Amount": [amount]})
                df_income = pd.concat([df_income, new_entry], ignore_index=True)
            except ValueError:
                return "Invalid amount entered", 400

    # Compute totals
    total_revenue = df_income[df_income["Category"] == "Revenue"]["Amount"].sum()
    total_cogs = df_income[df_income["Category"] == "COGS"]["Amount"].sum()
    total_expenses = df_income[df_income["Category"] == "Expenses"]["Amount"].sum()
    gross_profit = total_revenue - total_cogs
    net_profit = gross_profit - total_expenses

    return render_template(
        'income_statement.html',
        income_statement=df_income.to_dict(orient="records"),
        total_revenue=total_revenue,
        total_cogs=total_cogs,
        gross_profit=gross_profit,
        total_expenses=total_expenses,
        net_profit=net_profit
    )

@app.route('/modify_income', methods=['POST'])
def modify_income_statement():
    global df_income
    action = request.form.get('action')
    particular = request.form.get('particular')
    amount = request.form.get('amount')

    if action == "modify":
        if particular in df_income["Particulars"].values:
            try:
                new_amount = float(amount)
                df_income.loc[df_income["Particulars"] == particular, "Amount"] = new_amount
            except ValueError:
                return "Invalid amount entered", 400
        else:
            return "Particular not found", 400

    elif action == "delete":
        df_income = df_income[df_income["Particulars"] != particular].reset_index(drop=True)

    return redirect(url_for('income_statement'))

@app.route('/balance_sheet', methods=['GET', 'POST'])
@app.route('/balance_sheet', methods=['GET', 'POST'])
def balance_sheet():
    global df_balance
    if request.method == 'POST':
        category = request.form.get('category')
        particular = request.form.get('particular')
        amount = request.form.get('amount')

        if category and particular and amount:
            try:
                amount = float(amount)
                new_entry = pd.DataFrame({"Category": [category], "Particulars": [particular], "Amount": [amount]})
                df_balance = pd.concat([df_balance, new_entry], ignore_index=True)
            except ValueError:
                return "Invalid amount entered", 400

    # Compute totals
    total_assets = df_balance[df_balance["Category"] == "Asset"]["Amount"].sum()
    total_liabilities = df_balance[df_balance["Category"] == "Liability"]["Amount"].sum()
    total_equity = df_balance[df_balance["Category"] == "Equity"]["Amount"].sum()

    # Check if balanced
    balance_status = "Balanced ✅" if total_assets == (total_liabilities + total_equity) else "Not Balanced ❌"

    return render_template(
        'balance_sheet.html',
        balance_sheet=df_balance.to_dict(orient="records"),
        total_assets=total_assets,
        total_liabilities=total_liabilities,
        total_equity=total_equity,
        balance_status=balance_status
    )

@app.route('/modify_balance', methods=['POST'])
def modify_balance_sheet():
    global df_balance
    action = request.form.get('action')
    particular = request.form.get('particular')
    amount = request.form.get('amount')

    if action == "modify":
        if particular in df_balance["Particulars"].values:
            try:
                new_amount = float(amount)
                df_balance.loc[df_balance["Particulars"] == particular, "Amount"] = new_amount
            except ValueError:
                return "Invalid amount entered", 400
        else:
            return "Particular not found", 400

    elif action == "delete":
        df_balance = df_balance[df_balance["Particulars"] != particular].reset_index(drop=True)

    return redirect(url_for('balance_sheet'))

if __name__ == '__main__':
    app.run(debug=True)
