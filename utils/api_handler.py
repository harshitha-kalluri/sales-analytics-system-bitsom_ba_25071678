import requests

def fetch_all_products():
    
    try:
        response = requests.get('https://dummyjson.com/products?limit=100')
        response.raise_for_status()
        data = response.json()
        products = data.get('products', [])
        print(f"✓ Fetched {len(products)} products")
        return products
    except requests.RequestException as e:
        print(f"✗ Failed to fetch products: {e}")
        return []


def create_product_mapping(api_products):
   
    mapping = {}
    for product in api_products:
        pid = product['id']
        mapping[pid] = {
            'title': product.get('title', 'Unknown'),
            'category': product.get('category', 'Unknown'),
            'brand': product.get('brand', 'Unknown'),
            'rating': product.get('rating', 0.0)
        }
    return mapping


def enrich_sales_data(transactions, product_mapping):
    
    enriched = []
    for t in transactions:
        enriched_t = t.copy()
        try:
            pid_str = t['ProductID']
            if pid_str.startswith('P'):
                pid = int(pid_str[1:])
                if pid in product_mapping:
                    info = product_mapping[pid]
                    enriched_t['API_Category'] = info['category']
                    enriched_t['API_Brand'] = info['brand']
                    enriched_t['API_Rating'] = info['rating']
                    enriched_t['API_Match'] = True
                else:
                    enriched_t['API_Category'] = None
                    enriched_t['API_Brand'] = None
                    enriched_t['API_Rating'] = None
                    enriched_t['API_Match'] = False
            else:
                enriched_t['API_Category'] = None
                enriched_t['API_Brand'] = None
                enriched_t['API_Rating'] = None
                enriched_t['API_Match'] = False
        except (ValueError, KeyError):
            enriched_t['API_Category'] = None
            enriched_t['API_Brand'] = None
            enriched_t['API_Rating'] = None
            enriched_t['API_Match'] = False
        enriched.append(enriched_t)

    # Save to file
    save_enriched_data(enriched)
    return enriched


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
   
    header = 'TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match'
    lines = [header]
    for t in enriched_transactions:
        line = '|'.join([
            t['TransactionID'],
            t['Date'],
            t['ProductID'],
            t['ProductName'],
            str(t['Quantity']),
            str(t['UnitPrice']),
            t['CustomerID'],
            t['Region'],
            str(t.get('API_Category', '')),
            str(t.get('API_Brand', '')),
            str(t.get('API_Rating', '')),
            str(t.get('API_Match', ''))
        ])
        lines.append(line)

    with open(filename, 'w') as f:
        f.write('\n'.join(lines))