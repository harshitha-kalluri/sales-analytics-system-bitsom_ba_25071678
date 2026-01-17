def read_sales_data(filename):
    
    encodings = ['utf-8', 'latin-1', 'cp1252']
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
            # Skip header and empty lines
            raw_lines = [line.strip() for line in lines[1:] if line.strip()]
            return raw_lines
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
    print(f"Error: Unable to read file '{filename}' with supported encodings.")
    return []


def parse_transactions(raw_lines):
  
    transactions = []
    for line in raw_lines:
        fields = line.split('|')
        if len(fields) != 8:
            continue
        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = fields
        # Clean ProductName
        product_name = product_name.replace(',', '')
        # Clean numeric fields
        quantity = int(quantity.replace(',', ''))
        unit_price = float(unit_price.replace(',', ''))
        transaction = {
            'TransactionID': transaction_id,
            'Date': date,
            'ProductID': product_id,
            'ProductName': product_name,
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'CustomerID': customer_id,
            'Region': region
        }
        transactions.append(transaction)
    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    
    # Calculate amounts
    for t in transactions:
        t['Amount'] = t['Quantity'] * t['UnitPrice']

    # Available regions
    regions = set(t['Region'] for t in transactions if t['Region'])
    print(f"Available Regions: {', '.join(sorted(regions))}")

    # Amount range
    amounts = [t['Amount'] for t in transactions if 'Amount' in t]
    if amounts:
        min_amt = min(amounts)
        max_amt = max(amounts)
        print(f"Transaction Amount Range: {min_amt} - {max_amt}")

    valid_transactions = []
    invalid_count = 0

    for t in transactions:
        # Validation
        if (t['Quantity'] <= 0 or
            t['UnitPrice'] <= 0 or
            not t['CustomerID'] or
            not t['Region'] or
            not t['TransactionID'].startswith('T') or
            not t['ProductID'].startswith('P') or
            not t['CustomerID'].startswith('C')):
            invalid_count += 1
            continue
        valid_transactions.append(t)

    # Filtering
    filtered_by_region = 0
    filtered_by_amount = 0

    if region:
        valid_transactions = [t for t in valid_transactions if t['Region'] == region]
        filtered_by_region = len(valid_transactions)
        print(f"Records after region filter ({region}): {filtered_by_region}")

    if min_amount is not None or max_amount is not None:
        filtered = []
        for t in valid_transactions:
            amt = t['Amount']
            if min_amount is not None and amt < min_amount:
                continue
            if max_amount is not None and amt > max_amount:
                continue
            filtered.append(t)
        filtered_by_amount = len(filtered)
        valid_transactions = filtered
        print(f"Records after amount filter: {filtered_by_amount}")

    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region if region else len(valid_transactions),
        'filtered_by_amount': filtered_by_amount if (min_amount or max_amount) else len(valid_transactions),
        'final_count': len(valid_transactions)
    }

    return valid_transactions, invalid_count, summary