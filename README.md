# pdf2excel

## Overview
This Python script extracts transaction details from a bank statement PDF and converts them into an Excel file. It uses `pdfplumber` for text extraction and `pandas` for data structuring.

## Features
- Extracts transaction details such as date, description, amount, balance, and transaction type.
- Formats and cleans transaction descriptions.
- Saves structured data into an Excel file.

## Requirements
Ensure you have Python installed along with the following dependencies:
```sh
pip install pdfplumber pandas openpyxl
```

## Usage
Run the script with the PDF file as input:
```sh
python extract_tables.py
```
The output will be an Excel file (`output.xlsx`) containing structured transaction data.

## Script Logic
1. Opens the PDF using `pdfplumber`.
2. Extracts text line by line and identifies transaction details.
3. Cleans and formats descriptions, classifies transactions as Credit or Debit.
4. Saves the extracted data to an Excel file.

## Output Format
The script generates an Excel file with the following columns:
- **Date**: Transaction date.
- **Description**: Processed transaction details.
- **Amount**: Transaction amount.
- **Balance**: Updated account balance.
- **Transaction Type**: Credit or Debit.

## Example Output
| Date       | Description       | Amount  | Balance  | Transaction Type |
|------------|------------------|---------|----------|------------------|
| 12-Jan-2024 | BY CASH Deposit  | 5000.00 | 15000.00 | Credit          |
| 15-Jan-2024 | NEFT Transfer    | 2500.00 | 12500.00 | Debit           |

## License
This project is open-source and free to use.

