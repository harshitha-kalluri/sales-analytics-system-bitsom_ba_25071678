# Sales Analytics System 

A comprehensive Python-based system for processing sales data, performing analytics, integrating with external APIs, and generating detailed reports.

## Project Structure
sales-analytics-system/
│
├── data/
│ ├── sales_data.txt
│ └── enriched_sales_data.txt # Generated after execution
│
├── utils/
│ ├── file_handler.py
│ ├── data_processor.py
│ ├── api_handler.py
│ └── init.py
│
├── output/
│ └── sales_report.txt # Generated after execution
│
├── main.py
├── requirements.txt
└── README.md

## Prerequisites
- Python 3.8 or higher
- Internet connection (required for API-based product enrichment)


## Features

- **Data Processing**: Reads and cleans messy sales transaction files with encoding handling
- **Data Validation**: Validates transactions and applies optional filters
- **Analytics**: Performs various sales analyses including revenue, region-wise sales, top products, customer analysis, and daily trends
- **API Integration**: Enriches sales data with real-time product information from DummyJSON API
- **Reporting**: Generates comprehensive text reports with all key metrics

## Setup Instructions

### Clone the Repository
```bash
git clone https://github.com/harshitha-kalluri/sales-analytics-system.git
cd sales-analytics-system

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

The program performs the following steps:
1.Reads raw sales data from data/sales_data.txt
2.Parses and validates transaction records.
3. Allow optional data filtering, filters out invalid or incomplete entries.
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

## Generated Output Files

Enriched Sales Data
Path:
data/enriched_sales_data.txt
Contains validated and enriched transaction-level sales data.

Sales Report
Path:
output/sales_report.txt
Contains:
-Revenue summary
-Product and customer insights
-Regional and daily sales trends

## Notes
-All file paths used in the project are relative (no hardcoded local paths).
-The application runs end-to-end without manual intervention.
-Ensure the repository remains public until evaluation is completed.

## Error Handling

The system includes comprehensive error handling for:
- File reading with multiple encoding support
- API connection failures
- Data validation and parsing errors
- Invalid data formats

## Author
Harshitha Kalluri

