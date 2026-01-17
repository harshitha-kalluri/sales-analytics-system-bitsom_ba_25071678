# Sales Analytics System by Harshitha Kalluri {----}|{Business analytics with gen ai }

A comprehensive Python-based system for processing sales data, performing analytics, integrating with external APIs, and generating detailed reports.

## Features

- **Data Processing**: Reads and cleans messy sales transaction files with encoding handling
- **Data Validation**: Validates transactions and applies optional filters
- **Analytics**: Performs various sales analyses including revenue, region-wise sales, top products, customer analysis, and daily trends
- **API Integration**: Enriches sales data with real-time product information from DummyJSON API
- **Reporting**: Generates comprehensive text reports with all key metrics



## Installation

1. Clone or download the repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main application:

```bash
python main.py
```

The system will:
1. Read and parse sales data
2. Display filter options (regions and amount ranges)
3. Allow optional data filtering
4. Validate transactions
5. Perform comprehensive analysis
6. Fetch product data from API
7. Enrich sales data
8. Generate detailed reports

## Output Files

- `data/enriched_sales_data.txt`: Enriched sales data with API information
- `output/sales_report.txt`: Comprehensive analytics report

## Data Format

Input file (`data/sales_data.txt`) should be pipe-delimited with the following columns:
- TransactionID
- Date
- ProductID
- ProductName
- Quantity
- UnitPrice
- CustomerID
- Region

## Requirements

- Python 3.10+
- requests library (for API integration)

## API Integration

The system integrates with [DummyJSON API](https://dummyjson.com/) to fetch product information and enrich sales data with categories, brands, and ratings.

## Error Handling

The system includes comprehensive error handling for:
- File reading with multiple encoding support
- API connection failures
- Data validation and parsing errors
- Invalid data formats
