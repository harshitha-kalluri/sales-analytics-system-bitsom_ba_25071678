import os
from datetime import datetime
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue, region_wise_sales, top_selling_products,
    customer_analysis, daily_sales_trend, find_peak_sales_day, low_performing_products
)
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
  
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    total_records = len(transactions)

    # Overall Summary
    total_rev = calculate_total_revenue(transactions)
    total_trans = len(transactions)
    avg_order = total_rev / total_trans if total_trans > 0 else 0
    dates = sorted(set(t['Date'] for t in transactions))
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    # Region-wise
    region_stats = region_wise_sales(transactions)

    # Top 5 Products
    top_products = top_selling_products(transactions, 5)

    # Top 5 Customers
    cust_analysis = customer_analysis(transactions)
    top_customers = list(cust_analysis.items())[:5]

    # Daily Trend
    daily_trend = daily_sales_trend(transactions)

    # Peak Day
    peak_day = find_peak_sales_day(transactions)

    # Low Performing
    low_products = low_performing_products(transactions)

    # API Enrichment
    enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
    total_enriched = len(enriched_transactions)
    success_rate = (enriched_count / total_enriched * 100) if total_enriched > 0 else 0
    failed_products = [t['ProductName'] for t in enriched_transactions if not t.get('API_Match')]

    # Generate Report
    report = []
    report.append("=" * 50)
    report.append("          SALES ANALYTICS REPORT")
    report.append(f"        Generated: {now}")
    report.append(f"        Records Processed: {total_records}")
    report.append("=" * 50)
    report.append("")

    report.append("OVERALL SUMMARY")
    report.append("-" * 40)
    report.append(f"Total Revenue:        ₹{total_rev:,.2f}")
    report.append(f"Total Transactions:   {total_trans}")
    report.append(f"Average Order Value:  ₹{avg_order:,.2f}")
    report.append(f"Date Range:           {date_range}")
    report.append("")

    report.append("REGION-WISE PERFORMANCE")
    report.append("-" * 40)
    report.append("Region      Sales           % of Total    Transactions")
    for region, stats in region_stats.items():
        report.append(f"{region:<12} ₹{stats['total_sales']:>10,.0f} {stats['percentage']:>8.2f}% {stats['transaction_count']:>12}")
    report.append("")

    report.append("TOP 5 PRODUCTS")
    report.append("-" * 40)
    report.append("Rank  Product Name          Quantity    Revenue")
    for i, (name, qty, rev) in enumerate(top_products, 1):
        report.append(f"{i:<5} {name:<20} {qty:>8} ₹{rev:>10,.0f}")
    report.append("")

    report.append("TOP 5 CUSTOMERS")
    report.append("-" * 40)
    report.append("Rank  Customer ID  Total Spent    Order Count")
    for i, (cid, stats) in enumerate(top_customers, 1):
        report.append(f"{i:<5} {cid:<12} ₹{stats['total_spent']:>10,.0f} {stats['purchase_count']:>11}")
    report.append("")

    report.append("DAILY SALES TREND")
    report.append("-" * 40)
    report.append("Date          Revenue       Transactions  Unique Customers")
    for date, stats in daily_trend.items():
        report.append(f"{date}  ₹{stats['revenue']:>10,.0f} {stats['transaction_count']:>12} {stats['unique_customers']:>15}")
    report.append("")

    report.append("PRODUCT PERFORMANCE ANALYSIS")
    report.append("-" * 40)
    report.append(f"Best Selling Day: {peak_day[0]} (Revenue: ₹{peak_day[1]:,.0f}, Transactions: {peak_day[2]})")
    if low_products:
        report.append("Low Performing Products (Quantity < 10):")
        for name, qty, rev in low_products:
            report.append(f"  {name}: {qty} units, ₹{rev:,.0f}")
    else:
        report.append("No low performing products found.")
    report.append("")

    report.append("API ENRICHMENT SUMMARY")
    report.append("-" * 40)
    report.append(f"Total Products Enriched: {total_enriched}")
    report.append(f"Success Rate: {success_rate:.1f}%")
    if failed_products:
        report.append("Products that couldn't be enriched:")
        for prod in set(failed_products):
            report.append(f"  - {prod}")
    else:
        report.append("All products successfully enriched.")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))


def main():
    
    print("=" * 50)
    print("       SALES ANALYTICS SYSTEM")
    print("=" * 50)
    print()

    try:
        # 1. Read sales data
        print("[1/13] Reading sales data...")
        raw_lines = read_sales_data('data/sales_data.txt')
        if not raw_lines:
            print("No data found. Exiting.")
            return
        print(f"✓ Successfully read {len(raw_lines)} transactions")
        print()

        # 2. Parse and clean
        print("[2/13] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")
        print()

        # 3. Filter options
        print("[3/13] Filter Options Available:")
        valid_transactions, invalid_count, summary = validate_and_filter(transactions)
        print()

        # 4. Ask for filter
        filter_choice = 'n'
        if filter_choice == 'y':
            region = input("Enter region to filter (or press Enter to skip): ").strip()
            min_amt = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_amt = input("Enter maximum amount (or press Enter to skip): ").strip()
            region = region if region else None
            min_amt = float(min_amt) if min_amt else None
            max_amt = float(max_amt) if max_amt else None
            valid_transactions, _, _ = validate_and_filter(valid_transactions, region, min_amt, max_amt)
        print()

        # 5. Validate
        print("[4/13] Validating transactions...")
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")
        print()

        # 6. Analyze
        print("[5/13] Analyzing sales data...")
        # All analyses are done in report generation
        print("✓ Analysis complete")
        print()

        # 7. Fetch API
        print("[6/13] Fetching product data from API...")
        api_products = fetch_all_products()
        print()

        # 8. Enrich
        print("[7/13] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
        success_rate = (enriched_count / len(enriched_transactions) * 100) if enriched_transactions else 0
        print(f"✓ Enriched {enriched_count}/{len(enriched_transactions)} transactions ({success_rate:.1f}%)")
        print()

        # 9. Save enriched
        print("[8/13] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt")
        print()

        # 10. Generate report
        print("[9/13] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions, 'output/report-data')
        print("✓ Report saved to: output/report-data")
        print()

        # 11. Complete
        print("[10/13] Process Complete!")
        print("=" * 50)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your data and try again.")


if __name__ == "__main__":
    main()