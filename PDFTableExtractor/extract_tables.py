import pdfplumber
import pandas as pd
import re

def extract_tables_from_pdf(pdf_path: str, excel_output_path: str):
    structured_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            lines = page.extract_text().split('\n')
            i = 0
            while i < len(lines) - 1:
                line1 = lines[i].strip()
                line2 = lines[i + 1].strip()

                # Check for valid date at start of line
                if re.match(r"\d{2}-[A-Z][a-z]{2}-\d{4}", line1) or re.match(r"\d{2}-[A-Z]{3}-\d{4}", line1):
                    date = line1.split()[0]
                    raw_description = line1[len(date):].strip()

                    # Clean and format description
                    description = re.sub(r'^[TC]\s+', '', raw_description)  # remove leading T/C
                    description = re.sub(r'\s{2,}', ' ', description)       # normalize spacing

                    # Capitalize known keywords
                    keywords = ['by cash', 'imps', 'lien reversal', 'ledger folio charges', 
                                'cgst', 'inspection charges', 'int.coll', 'neft', 'upi', 'to cash', 'from']
                    for kw in keywords:
                        pattern = re.compile(re.escape(kw), re.IGNORECASE)
                        description = pattern.sub(kw.upper(), description)

                    # Classify transaction type
                    if any(k in description for k in ["BY CASH", "CR-", "IMPS", "FROM"]):
                        txn_type = "Credit"
                    else:
                        txn_type = "Debit"

                    # Extract amount and balance from second line
                    amounts = re.findall(r"[\d,]+\.\d{2}", line2)
                    if len(amounts) == 2:
                        amount = amounts[0].replace(",", "")
                        balance = amounts[1].replace(",", "").replace("Dr", "")
                        structured_data.append([date, description, amount, balance, txn_type])
                        i += 2
                        continue
                    elif len(amounts) == 1:
                        amount = amounts[0].replace(",", "")
                        balance_match = re.search(r"[\d,]+\.\d{2}Dr", line2)
                        balance = balance_match.group(0).replace(",", "").replace("Dr", "") if balance_match else ""
                        structured_data.append([date, description, amount, balance, txn_type])
                        i += 2
                        continue
                i += 1

    # Convert to DataFrame and save
    df = pd.DataFrame(structured_data, columns=["Date", "Description", "Amount", "Balance", "Transaction Type"])
    df.to_excel(excel_output_path, index=False)
    print(f"✅ Extracted {len(df)} transactions to {excel_output_path}")


# Example usage
if __name__ == "__main__":
    extract_tables_from_pdf("sample1.pdf", "output1.xlsx")
