
import csv
from datetime import datetime
from prettyprint import pp

from categories import CATEGORIES, UNCATEGORIZED_KEY

def convert_date(date):
    return datetime.strptime(date, '%d/%m/%Y')


def _transaction(row):
    transaction = {
        'date': convert_date(row[1]),
        'amount': row[3],
        'type': row[4],
        'description': row[5]
    }
    return transaction


def _transactions (filename='data.csv'):
    transactions = []
    with open(filename, 'r') as input_file:
        reader = csv.reader(input_file)
        next(reader, None)
        for row in reader:
            transaction = _transaction(row)
            transactions.append(transaction)
    return transactions


def _transactions_per_month(transactions, month=None):
    transactions = _transactions()
    if not month:
        return transactions
    result = []
    for transaction in transactions:
        if transaction['date'].month == month:
            result.append(transaction)
    return result


def _transactions_per_categories(transactions, categories=CATEGORIES):
    keys = CATEGORIES.keys()
    result = {UNCATEGORIZED_KEY: []}
    for transaction in transactions:
        match = False
        for key in keys:
            for substring in CATEGORIES[key]:
                if substring.lower() in transaction['description'].lower():
                    if key in result:
                        result[key].append(transaction)
                    else:
                        result[key] = [transaction]
                    match = True
        if match == False:
            otherArray = result[UNCATEGORIZED_KEY]
            otherArray.append(transaction)
    return result


def _net_for_transactions(transactions):
    result = 0.0
    for transaction in transactions:
        amount = transaction['amount']
        amount = float(amount)
        result += amount
    print("Net is %s" % result)
    return result


def _expenses_for_transactions(transactions):
    result = 0.0
    for transaction in transactions:
        amount = transaction['amount']
        amount = float(amount)
        if amount < 0:
            result += amount
    return abs(result)


def _income_for_transactions(transactions):
    result = 0.0
    for transaction in transactions:
        amount = transaction['amount']
        amount = float(amount)
        if amount > 0:
            result += amount
    return abs(result)

if __name__ == "__main__":
    print('===========')
    transactions = _transactions()
    for month in range(0, 13):
        transactions = _transactions_per_month(transactions, month)
        income = _income_for_transactions(transactions)
        expenses = _expenses_for_transactions(transactions)
        if len(transactions) < 1:
            continue
        print("Income for month %s: %s" % (month, income))
        print("Expenses for month %s: %s" % (month, expenses))
        print("Net for month: %s" % (income - expenses))
        print('===========')
        pp("From %s to %s" % (transactions[-1]['date'], transactions[0]['date']))
        print("Parsing %s transactions for month %s" % (len(transactions), month))
        transactions = _transactions_per_categories(transactions)
        for key, category_transactions in transactions.iteritems():
            print("Expenses for category %s with %s transactions: %s" % (
                key,
                len(category_transactions),
                _expenses_for_transactions(category_transactions)))
        print('===========')

