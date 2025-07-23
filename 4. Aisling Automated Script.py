""" importing the modules"""
 
import pandas as pd # data cleaning

from datetime import datetime # today()
from dateutil.relativedelta import relativedelta # number of years

import psycopg2
from io import StringIO

from shutil import move # move files
from datetime import datetime


print("Module are imported !")

""" importing the data """

# CSV need to be renamed the right way and put in the 'aisling_input_data' every week to be imported and cleaned
# The CSV need to have the same structure, do not change the structure from one week to another without sending a notice
# The tables must have the same column names as the first CSV

missing_values = ["-", "--", "n/a", "na", "NA", "N/A", "?", "None", "null", "NULL", ""]

buyers = pd.read_csv(r"C:\Users\Desktop\aisling_script\aisling_input_data\buyers.csv", na_values=missing_values)
print("BUYERS table imported 1/5")
products = pd.read_csv(r"C:\Users\Desktop\aisling_script\aisling_input_data\products.csv", na_values=missing_values)
print("PRODUCTS table imported 2/5")
reviews = pd.read_csv(r"C:\Users\Desktop\aisling_script\aisling_input_data\reviews.csv", na_values=missing_values)
print("REVIEWS table importe 3/5")
sellers = pd.read_csv(r"C:\Users\Desktop\aisling_script\aisling_input_data\sellers.csv", na_values=missing_values)
print("SELLERS table imported 4/5")
transactions = pd.read_csv(r"C:\Users\Desktop\aisling_script\aisling_input_data\transactions.csv", na_values=missing_values)
print("TRANSACTIONS table imported 5/5")

""" cleaning the tables """

##################################################
# BUYERS  table
##################################################

print("Cleaning BUYERS table...")

with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
    f.write('Cleaning BUYERS table \n')
    f.write('\n')

# BUYERS dtypes

buyers_object_columns = ['buyer_id', 'name', 'country', 'customer_type', 'gender']

for col in buyers_object_columns:
    buyers[col] = buyers[col].astype('object')

buyers['birthdate'] = pd.to_datetime(buyers['birthdate'], errors="coerce")

# BUYERS null values

buyer_id_null_rows = buyers['name'].loc[buyers['buyer_id'].isnull()].tolist()
buyers = buyers.dropna(subset='buyer_id')

buyer_name_null_rows = buyers['buyer_id'].loc[buyers['name'].isnull()].tolist()
buyers = buyers.dropna(subset='name')

with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
    f.write(f'Deleted customers without ID: {buyer_id_null_rows}\n')
    f.write(f'Deleted customers without name: {buyer_name_null_rows}\n')

buyers_null_gender = buyers['gender'].isnull().sum()
buyers['gender'] = buyers['gender'].fillna(buyers['gender'].mode()[0])
buyers_null_gender_two = buyers['gender'].isnull().sum()

buyers_null_birthdate = buyers['birthdate'].isnull().sum()
buyers['birthdate'] = buyers['birthdate'].fillna(buyers['birthdate'].median())
buyers_null_birthdate_two = buyers['birthdate'].isnull().sum()

buyers_null_country = buyers['country'].isnull().sum()
buyers['country'] = buyers['country'].fillna(buyers['country'].mode()[0])
buyers_null_country_two = buyers['country'].isnull().sum()

buyers_null_customer_type = buyers['customer_type'].isnull().sum()
buyers['customer_type'] = buyers['customer_type'].fillna(buyers['customer_type'].mode()[0])
buyers_null_customer_type_two = buyers['customer_type'].isnull().sum()

with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
    f.write(f'Number of null values in gender: {buyers_null_gender}, after update: {buyers_null_gender_two} \n')
    f.write(f'Number of null values in birthdate: {buyers_null_birthdate}, after update: {buyers_null_birthdate_two} \n')
    f.write(f'Number of null values in country: {buyers_null_country}, after update: {buyers_null_country_two} \n')
    f.write(f'Number of null values in customer_type: {buyers_null_customer_type}, after update: {buyers_null_customer_type_two} \n')
    f.write(f'\n')

# BUYERS duplicates

buyers = buyers.loc[~buyers.duplicated(subset='buyer_id')].reset_index().copy()
                         
# BUYERS string cleaning

buyers['customer_type'] = buyers['customer_type'].astype(str).str.replace('regulier', 'regular')
buyers['customer_type'] = buyers['customer_type'].astype(str).str.replace('nouveau', 'new')

buyers_string_list = ['buyer_id', 'name', 'country', 'customer_type', 'gender']

for col in buyers_string_list: 
    buyers[col] = buyers[col].astype(str).str.strip()

# BUYERS business consistency validation

""" Maximum age = 100 & minimum age = 13 """

minumum_age = datetime.today() - relativedelta(years=13)
[(buyers['birthdate'] > '1925-01-01') & (buyers['birthdate'] < minumum_age)]

print("BUYERS table cleaned")

##################################################
# PRODUCTS table
##################################################

print("Cleaning PRODUCTS table...")

with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
    f.write('Cleaning PRODUCTS table \n')
    f.write('\n')

# rename 'book ID' to 'book_id' and deleting the rating column in the CSV template

if 'rating' in products.columns:
    products = products.drop(columns=['rating'], errors='ignore')

#  PRODUCTS dtypes

products_object_columns = ['book_id', 'name', 'category', 'summary', 'seller_id']

for col in products_object_columns:
    products[col] = products[col].astype(object)

products['price'] = products['price'].astype(float)

print('Data types are updated')

# PRODUCTS null values

product_book_id_null_rows = products['name'].loc[products['book_id'].isnull()].tolist()
products = products.dropna(subset='book_id')

product_name_null_rows = products['book_id'].loc[products['name'].isnull()].tolist()
products = products.dropna(subset='name')

product_price_null_rows = products['book_id'].loc[products['price'].isnull()].tolist()
products = products.dropna(subset='price')

product_seller_id_null_rows = products['book_id'].loc[products['seller_id'].isnull()].tolist()
products = products.dropna(subset='seller_id')

products_null_category = products['category'].isnull().sum()
products['category'] = products['category'].fillna('No category submitted')
products_null_category_two = products['category'].isnull().sum()

products_null_summary = products['summary'].isnull().sum()
products['summary'] = products['summary'].fillna('No summary submitted')
products_null_summary_two = products['summary'].isnull().sum()


with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
    f.write(f'Deleted books without ID: {product_book_id_null_rows}\n')
    f.write(f'Deleted ID without names: {product_name_null_rows}\n')
    f.write(f'Deleted ID without price: {product_price_null_rows}\n')
    f.write(f'Deleted ID without seller_id: {product_seller_id_null_rows}\n')
    f.write(f'Number of null values in category: {products_null_category}, after update: {products_null_category_two} \n')
    f.write(f'Number of null values in summary: {products_null_summary}, after update: {products_null_summary_two} \n')
    f.write(f'\n')

print("Null values are deleted or replaced")

# PRODUCTS duplicates

products = products.loc[~products.duplicated(subset='book_id')].reset_index(drop=True).copy()

print("Duplicated rows are deleted")
                         
# PRODUCTS string cleaning

products_string_list = ['book_id', 'name', 'category', 'summary', 'seller_id']

for col in products_string_list:
    products[col] = products[col].astype(str).str.strip()

print("PRODUCTS table cleaned")

##################################################
# REVIEWS table
##################################################

print("Cleaning REVIEWS table...")

with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
    f.write('Cleaning REVIEWS table \n')
    f.write('\n')

#  REVIEWS dtypes

reviews_object_columns = ['review_id', 'book_id', 'review_text', 'author']

for col in reviews_object_columns:
    reviews[col] = reviews[col].astype(object)

reviews = reviews[reviews['rating'].isin([1,2,3,4,5])]

reviews['rating'] = reviews['rating'].astype(int)

reviews['review_date'] = pd.to_datetime(reviews['review_date'], errors='coerce')

print('Data types are updated')

# REVIEWS null values

reviews_null_review_id = reviews['review_id'].isnull().sum()
reviews = reviews.dropna(subset='review_id')
reviews_null_review_id_two = reviews['review_id'].isnull().sum()

reviews_null_book_id = reviews['book_id'].isnull().sum()
reviews = reviews.dropna(subset='book_id')
reviews_null_book_id_two = reviews['book_id'].isnull().sum()


reviews_null_review_text = reviews['review_text'].isnull().sum()
reviews = reviews.dropna(subset='review_text')
reviews_null_review_text_two = reviews['review_text'].isnull().sum()

reviews_null_rating = reviews['rating'].isnull().sum()
reviews['rating'] = reviews['rating'].fillna(
    reviews.groupby('book_id')['rating'].transform('mean'))
reviews_null_rating_two = reviews['rating'].isnull().sum()

reviews_null_review_date = reviews['review_date'].isnull().sum()
reviews['review_date'] = reviews['review_date'].fillna(reviews['review_date'].median())
reviews_null_review_date_two = reviews['review_date'].isnull().sum()

reviews_null_author = reviews['author'].isnull().sum()

with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
    f.write(f'Number of null values in review_id: {reviews_null_review_id}, after update: {reviews_null_review_id_two}\n')
    f.write(f'Number of null values in book_id: {reviews_null_book_id}, after update: {reviews_null_book_id_two}\n')
    f.write(f'Number of null values in review_text: {reviews_null_review_text}, after update: {reviews_null_review_text_two}\n')
    f.write(f'Number of null values in rating: {reviews_null_rating}, after update: {reviews_null_rating_two}\n')
    f.write(f'Number of null values in review_date: {reviews_null_review_date}, after update: {reviews_null_review_date_two}\n')
    f.write(f'Number of null values in author: {reviews_null_author}\n')
    f.write(f'\n')

print("Null values are deleted or replaced")

# REVIEWS duplicates

reviews = reviews[~reviews.duplicated(subset='review_id')].reset_index(drop=True).copy()

print("Duplicated rows are deleted")
                         
# REVIEWS string cleaning

reviews_string_list = ['review_id', 'book_id', 'review_text', 'author']

for col in reviews_string_list:
    reviews[col] = reviews[col].astype(str).str.strip()

# REVIEWS filtering

book_list = products['book_id'].tolist()

reviews = reviews[reviews['book_id'].isin(book_list)]

# REVIEWS business consistency validation

""" Maximum date for review is today """

reviews[(reviews['review_date'] >= '2017-01-01') & (reviews['review_date'] <= datetime.today())]

print("REVIEWS table cleaned")

##################################################
# SELLERS table
##################################################

print("Cleaning SELLERS table...")

with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
    f.write('Cleaning SELLERS table \n')
    f.write('\n')

#  SELLERS dtypes

sellers_object_columns = ['seller_id', 'author_name', 'country', 'seller_type']

for col in sellers_object_columns:
    sellers[col] = sellers[col].astype(object)

sellers['birthdate'] = pd.to_datetime(sellers['birthdate'], errors='coerce')

print('Data types are updated')

# SELLERS null values

sellers['seller_type'] = sellers['seller_type'].replace({
    "Maison d'édition": 'Publishing house',
    'Indépendant': 'Independent'
})

seller_id_null_rows = sellers['author_name'].loc[sellers['seller_id'].isnull()].tolist()
sellers = sellers.dropna(subset='seller_id')

seller_name_null_rows = sellers['seller_id'].loc[sellers['author_name'].isnull()].tolist()
sellers = sellers.dropna(subset='author_name')

sellers_null_birthdate = sellers['birthdate'].isnull().sum()
sellers_null_country = sellers['country'].isnull().sum()
sellers_null_seller_type = sellers['seller_type'].isnull().sum()

with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
    f.write(f'Deleted sellers without ID: {seller_id_null_rows}\n')
    f.write(f'Deleted sellers without name: {seller_name_null_rows}\n')
    f.write(f'Number of null values in birthdate: {sellers_null_birthdate}\n')
    f.write(f'Number of null values in country: {sellers_null_seller_type}\n')
    f.write(f'\n')

print("Null values are deleted or replaced")

# SELLERS duplicates

sellers = sellers.loc[~sellers.duplicated(subset='seller_id')]

print("Duplicated rows are deleted")
                         
# SELLERS string cleaning

sellers_string_list = ['seller_id', 'author_name', 'country', 'seller_type']

for col in sellers_string_list:
    sellers[col] = sellers[col].astype(str).str.strip()

print("SELLERS table cleaned")

# SELLERS business consistency validation

""" Maximum age = 100 & minimum age = 13 """

minumum_age_sellers = datetime.today() - relativedelta(years=13)
sellers = sellers[(sellers['birthdate'] > '1925-01-01') & (sellers['birthdate'] < minumum_age_sellers)]

##################################################
# Transactions table
##################################################

print("Cleaning TRANSACTIONS table...")

with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
    f.write('Cleaning TRANSACTIONS table \n')
    f.write('\n')

#  TRANSACTIONS dtypes

transactions_object_columns = ['transaction_id', 'book_id', 'buyer_id']
transactions_float_columns = ['price_paid', 'discount_rate']

for col in transactions_object_columns:
    transactions[col] = transactions[col].astype(object)

for col in transactions_float_columns:
    transactions[col] = transactions[col].astype(float)

transactions['date'] = pd.to_datetime(transactions['date'], errors='coerce')

print('Data types are updated')

# TRANSACTIONS null values

transactions_null_transaction_id = transactions['transaction_id'].isnull().sum()
transactions = transactions.dropna(subset='transaction_id')
transactions_null_transaction_id_two = transactions['transaction_id'].isnull().sum()

transactions = transactions.loc[transactions['book_id'].isin(products['book_id'])]

transactions_null_book_id = transactions['book_id'].isnull().sum()
transactions_null_buyer_id = transactions['buyer_id'].isnull().sum()

transactions_null_price_paid = transactions['price_paid'].isnull().sum()

transactions = transactions.merge(products, on='book_id', how='inner')
transactions = transactions[['transaction_id', 'book_id', 'buyer_id', 'price','discount_rate', 'date']].copy()
transactions['price'] = transactions['price'] - (transactions['price'] * transactions['discount_rate'])
transactions = transactions.rename(columns={'price':'price_paid'})

transactions_null_price_paid_two = transactions['price_paid'].isnull().sum()

transactions_null_discount_rate = transactions['discount_rate'].isnull().sum()
transactions['discount_rate'] = transactions['discount_rate'].fillna(0.0)
transactions_null_discount_rate_two = transactions['discount_rate'].isnull().sum()

transactions_null_date = transactions['date'].isnull().sum()

with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
    f.write(f'Number of null values in transaction_id: {transactions_null_transaction_id}, after update : {transactions_null_transaction_id_two} \n')
    f.write(f'Number of null values in book_id: {transactions_null_book_id} \n')
    f.write(f'Number of null values in buyer_id: {transactions_null_buyer_id} \n')
    f.write(f'Number of null values in price_paid: {transactions_null_price_paid}, after update: {transactions_null_price_paid_two}\n')
    f.write(f'Number of null values in discount_rate: {transactions_null_discount_rate}, after update: {transactions_null_discount_rate_two}\n')
    f.write(f'Number of null values in date: {transactions_null_date} \n')
    f.write(f'\n')

print("Null values are deleted or replaced")

# TRANSACTIONS duplicates

transactions = transactions.loc[~transactions.duplicated(subset='transaction_id')]

print("Duplicated rows are deleted")
                         
# TRANSACTIONS string cleaning

for col in transactions_object_columns:
    transactions[col] = transactions[col].astype(str).str.strip()

# TRANSACTIONS business consistency validation

""" Discount rates are not negative and above 70 %  """

transactions = transactions[(transactions['discount_rate'] >= 0.00) & (transactions['discount_rate'] <= 0.70)]

print("TRANSACTIONS table cleaned")

##################################################
# Additional verifications
##################################################

""" Making sure every seller_id in PRODUCTS is in the SELLERS table as well """

with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
    f.write('Additonial verifications \n')
    f.write('\n')

if False in products['seller_id'].isin(sellers['seller_id']):
    number_false_values_seller_id = (~products['seller_id'].isin(sellers['seller_id'])).sum()

    with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
        f.write(f'Number of seller_id that aren\'t in the SELLERS table {number_false_values_seller_id} \n')

else:

    with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
        f.write('Every seller_id (PRODUCTS) is in the SELLERS table \n')

""" Making sure every book_id in REVIEWS is in the PRODUCTS table as well """

if False in reviews['book_id'].isin(products['book_id']):
    number_false_values_book_id = (~reviews['book_id'].isin(products['book_id'])).sum()

    with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
        f.write(f'Number of book_id (REVIEWS) that aren\'t in the PRODUCTS table {number_false_values_book_id}\n')

else:

    with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
        f.write('Every book_id (REVIEWS) is in the PRODUCTS table\n')

""" Making sure every book_id in TRANSACTIONS is in the PRODUCTS table as well """

if False in transactions['book_id'].isin(products['book_id']):
    number_false_values_book_id_two = (~transactions['book_id'].isin(products['book_id'])).sum()

    with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
        f.write(f'Number of book_id (TRANSACTIONS) that aren\'t in the PRODUCTS table {number_false_values_book_id_two}\n')

else:

    with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
        f.write('Every book_id (TRANSACTIONS) is in the PRODUCTS table\n')

""" Making sure every buyer_id in TRANSACTIONS is in the BUYERS table as well """

if False in transactions['buyer_id'].isin(buyers['buyer_id']):
    number_false_values_buyer_id = (~transactions['buyer_id'].isin(buyers['buyer_id'])).sum()

    with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
        f.write(f'Number of buyer_id (TRANSACTIONS) that aren\'t in the BUYERS table {number_false_values_buyer_id}\n')

else:

    with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
        f.write('Every buyer_id (TRANSACTIONS) is in the BUYERS table\n')

##################################################
# Exporting to PostgreSQL
##################################################

print(products.head())
print(products.shape)
print(reviews.head())
print(reviews.shape)
print(sellers.head())
print(sellers.shape)

""" Exporting the CSV in the already created tables in pgAdmin4 """

# Connecting to PostgreSQL

conn = psycopg2.connect(
    host='localhost',
    dbname='AISLING (Book Store)',
    user='postgres',
    password='',
    port='5432'
)

cur = conn.cursor()

def importer(table_name, dataframe):

    # disable constraints because we can't import with the foreign keys active currently 

    cur.execute(f"ALTER TABLE {table_name} DISABLE TRIGGER ALL;")

    # delete the content in the table before importing new data

    cur.execute(f'TRUNCATE TABLE {table_name} CASCADE')

    # dropping index colonne

    if 'index' in dataframe.columns or 'Unnamed: 0' in dataframe.columns:
        dataframe = dataframe.drop(columns=['index'], errors='ignore')
        dataframe = dataframe.drop(columns=['Unnamed: 0'], errors='ignore')
    
    # convert the dataframe in a virtual CSV (memory file)

    buffer = StringIO()
    dataframe.to_csv(buffer, index=False)
    buffer.seek(0)

    # importing the data

    columns = ', '.join(dataframe.columns)
    cur.copy_expert(
        sql=f"COPY {table_name} ({columns}) FROM STDIN WITH CSV HEADER DELIMITER ',';",
        file=buffer
    )

    cur.execute(f"ALTER TABLE {table_name} ENABLE TRIGGER ALL;")

    with open(r'C:\Users\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
        f.write(f'Cleaned {table_name} is successfully imported\n')

    print(f'{table_name} imported in pgAdmin4 successfully !')

importer("buyers", buyers)
importer("products", products)
importer("reviews", reviews)
importer("sellers", sellers)
importer("transactions", transactions)

# commit and close

conn.commit()
cur.close()
conn.close()

##################################################
# Exporting to file to have back-up CSVs
##################################################

now = datetime.now().strftime('%Y%m%d_%H%M%S')

move(r"C:\Users\Desktop\aisling_script\aisling_input_data\buyers.csv", rf"C:\Users\Houssain\Desktop\aisling_script\aisling_output_data\buyers_{now}.csv") 
move(r"C:\Users\Desktop\aisling_script\aisling_input_data\products.csv", rf"C:\Users\Houssain\Desktop\aisling_script\aisling_output_data\products_{now}.csv")
move(r"C:\Users\Desktop\aisling_script\aisling_input_data\reviews.csv", rf"C:\Users\Houssain\Desktop\aisling_script\aisling_output_data\reviews_{now}.csv")
move(r"C:\Users\Desktop\aisling_script\aisling_input_data\sellers.csv", rf"C:\Users\Houssain\Desktop\aisling_script\aisling_output_data\sellers_{now}.csv")
move(r"C:\Users\Desktop\aisling_script\aisling_input_data\transactions.csv", rf"C:\Users\Houssain\Desktop\aisling_script\aisling_output_data\transactions_{now}.csv")   


with open(r'C:\Users\Houssain\Desktop\aisling_script\deleted_data_logs.txt', 'a') as f:
        f.write('Input files were moved to the dedicated folder')
    
print('Input files were moved to the dedicated folder')