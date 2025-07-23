# Aisling Data Cleaning & Import Automation

This Python script automates the entire data cleaning and import pipeline for the Aisling Bookstore weekly data feed.

## ✅ Features

- Cleans five input CSV tables: `buyers`, `products`, `reviews`, `sellers`, `transactions`
- Handles:
  - Missing values
  - Duplicates
  - Type casting
  - Business logic (age ranges, discounts, etc.)
- Cross-field consistency checks (`book_id`, `seller_id`, `buyer_id`)
- Automatically disables and re-enables PostgreSQL constraints for safe import
- Exports to PostgreSQL using `psycopg2` and `copy_expert`
- Archives input files with timestamp
- Logs every deletion/modification to `deleted_data_logs.txt`

## 📂 Folder Structure

```
aisling_script/
├── aisling_input_data/
│   ├── buyers.csv
│   ├── products.csv
│   ├── ...
├── aisling_output_data/
│   └── buyers_YYYYMMDD_HHMMSS.csv
├── asiling_script.py
├── deleted_data_logs.txt
```

## 🚀 How to Use

1. Place your cleaned input CSVs into the `aisling_input_data/` folder.
2. Make sure the structure matches the original template.
3. Run the script:
```bash
python asiling_script.py
```
4. The cleaned data will be:
   - Inserted into your PostgreSQL `AISLING (Book Store)` database
   - Logged to `deleted_data_logs.txt`
   - Archived in `aisling_output_data/`

## 🛑 Important Notes

- Do not change the structure of the input CSVs without notice
- All missing, duplicated, or invalid entries are logged
- The script **truncates** PostgreSQL tables before re-inserting data
- PostgreSQL credentials must be correct in the script

## 📦 Dependencies

- `pandas`
- `psycopg2`
- `dateutil`
