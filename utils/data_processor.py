from collections import defaultdict


def calculate_total_revenue(transactions):
    return sum(t["Quantity"] * t["UnitPrice"] for t in transactions)


def region_wise_sales(transactions):
    total = calculate_total_revenue(transactions)
    stats = defaultdict(lambda: {"total_sales": 0, "transaction_count": 0})

    for t in transactions:
        sales = t["Quantity"] * t["UnitPrice"]
        stats[t["Region"]]["total_sales"] += sales
        stats[t["Region"]]["transaction_count"] += 1

    for r in stats:
        stats[r]["percentage"] = (stats[r]["total_sales"] / total) * 100

    return dict(sorted(stats.items(), key=lambda x: x[1]["total_sales"], reverse=True))


def top_selling_products(transactions, n=5):
    prod = defaultdict(lambda: {"qty": 0, "rev": 0})

    for t in transactions:
        prod[t["ProductName"]]["qty"] += t["Quantity"]
        prod[t["ProductName"]]["rev"] += t["Quantity"] * t["UnitPrice"]

    sorted_p = sorted(prod.items(), key=lambda x: x[1]["qty"], reverse=True)
    return [(k, v["qty"], v["rev"]) for k, v in sorted_p[:n]]


def customer_analysis(transactions):
    cust = defaultdict(lambda: {"total": 0, "count": 0, "products": set()})

    for t in transactions:
        spent = t["Quantity"] * t["UnitPrice"]
        c = cust[t["CustomerID"]]
        c["total"] += spent
        c["count"] += 1
        c["products"].add(t["ProductName"])

    result = {}
    for cid, v in cust.items():
        result[cid] = {
            "total_spent": v["total"],
            "purchase_count": v["count"],
            "avg_order_value": v["total"] / v["count"],
            "products_bought": list(v["products"])
        }

    return dict(sorted(result.items(), key=lambda x: x[1]["total_spent"], reverse=True))


def daily_sales_trend(transactions):
    daily = defaultdict(lambda: {"revenue": 0, "transaction_count": 0, "customers": set()})

    for t in transactions:
        d = daily[t["Date"]]
        d["revenue"] += t["Quantity"] * t["UnitPrice"]
        d["transaction_count"] += 1
        d["customers"].add(t["CustomerID"])

    return {
        k: {
            "revenue": v["revenue"],
            "transaction_count": v["transaction_count"],
            "unique_customers": len(v["customers"])
        }
        for k, v in sorted(daily.items())
    }


def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)
    peak = max(daily, key=lambda d: daily[d]["revenue"])
    return peak, daily[peak]["revenue"], daily[peak]["transaction_count"]


def low_performing_products(transactions, threshold=10):
    prod = defaultdict(lambda: {"qty": 0, "rev": 0})

    for t in transactions:
        prod[t["ProductName"]]["qty"] += t["Quantity"]
        prod[t["ProductName"]]["rev"] += t["Quantity"] * t["UnitPrice"]

    low = [(k, v["qty"], v["rev"]) for k, v in prod.items() if v["qty"] < threshold]
    return sorted(low, key=lambda x: x[1])