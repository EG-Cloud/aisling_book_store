---------------------
-- BUYERS
---------------------

select column_name, data_type 
from information_schema.columns
where table_name = 'buyers';

select *
from buyers;

select -- 0 null values
	sum(case when buyer_id is null then 1 else 0 end) as buyer_id,
	sum(case when name is null then 1 else 0 end) as name,
	sum(case when gender is null then 1 else 0 end) as gender,
	sum(case when birthdate is null then 1 else 0 end) as birthdate,
	sum(case when country is null then 1 else 0 end) as country,
	sum(case when customer_type is null then 1 else 0 end) as customer_type
from buyers;

select 
	sum(case when buyer_id::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as buyer_id,
	sum(case when name::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as name,
	sum(case when gender::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as gender,
	sum(case when birthdate::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as birthdate,
	sum(case when country::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as country,
	sum(case when customer_type::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as customer_type
from buyers;

select count(distinct buyer_id) -- 3000 records // 3000 unique values
from buyers;

select * -- duplicate names but they are different people
from buyers 
where name IN 
(				
	select name
	from buyers
	group by name
	having count(*) > 1				
)
order by name desc;

update buyers -- formatting every record in title case for column "name"
set name = trim(initcap(name));

select distinct gender
from buyers;

select max(birthdate), min(birthdate) -- realistic dates
from buyers;

select distinct country
from buyers;

select distinct customer_type
from buyers;

update buyers
set customer_type = trim(lower(customer_type));

update buyers
set gender = trim(lower(gender));

update buyers
set country = trim(initcap(country));

---------------------
-- PRODUCTS
---------------------

select column_name, data_type
from information_schema.columns
where table_name = 'products';

select *
from products;

select
	sum(case when book_id is null then 1 else 0 end) as book_id,
	sum(case when name is null then 1 else 0 end) as name,
	sum(case when price is null then 1 else 0 end) as price,
	sum(case when category is null then 1 else 0 end) as category,
	sum(case when summary is null then 1 else 0 end) as summary,
	sum(case when rating is null then 1 else 0 end) as rating,
	sum(case when seller_id is null then 1 else 0 end) as seller_id
from products;

select 
	sum(case when book_id::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as book_id,
	sum(case when name::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as name,
	sum(case when price::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as price,
	sum(case when category::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as category,
	sum(case when summary::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as summary,
	sum(case when rating::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as rating,
	sum(case when seller_id::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as seller_id
from products;

select count(distinct book_id)
from products;

update products
set name = trim(initcap(name));

update products
set category = trim(lower(category));

update products
set rating = '1'
where rating = 'One'

update products
set rating = '2'
where rating = 'Two'

update products
set rating = '3'
where rating = 'Three'

update products
set rating = '4'
where rating = 'Four'

update products
set rating = '5'
where rating = 'Five'

update products 
set rating = trim(rating);

---------------------
-- REVIEWS
---------------------

select column_name, data_type
from information_schema.columns
where table_name = 'reviews';

select *
from reviews;

select
	sum(case when review_id is null then 1 else 0 end) as review_id,
	sum(case when book_id is null then 1 else 0 end) as book_id,
	sum(case when review_text is null then 1 else 0 end) as review_text,
	sum(case when rating is null then 1 else 0 end) as rating,
	sum(case when review_date is null then 1 else 0 end) as review_date,
	sum(case when author is null then 1 else 0 end) as author
from reviews;

update reviews
set review_text = 'No review submitted'
where review_text is null;

select 
	sum(case when review_id::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as review_id,
	sum(case when book_id::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as book_id,
	sum(case when review_text::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as review_text,
	sum(case when rating::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as rating,
	sum(case when review_date::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as review_date,
	sum(case when author::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as author
from reviews;

select count(distinct review_id)
from reviews;

select count(distinct book_id)
from reviews;

select distinct rating -- needs to be cleaned 
from reviews;

update reviews
set rating = '1'
where rating = 'Bad'

update reviews 
set rating = '3'
where rating = 'Three'

update reviews
set author = trim(initcap(author));

---------------------
-- SELLERS
---------------------

select column_name, data_type
from information_schema.columns
where table_name = 'sellers';

select *
from sellers;

select
	sum(case when seller_id is null then 1 else 0 end) as seller_id,
	sum(case when author_name is null then 1 else 0 end) as author_name,
	sum(case when birthdate is null then 1 else 0 end) as birthdate,
	sum(case when country is null then 1 else 0 end) as country,
	sum(case when seller_type is null then 1 else 0 end) as seller_type
from sellers;

select 
	sum(case when seller_id::TEXT  then 1 else 0 end) as seller_id,
	sum(case when author_name::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as author_name,
	sum(case when birthdate::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as birthdate,
	sum(case when country::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as country,
	sum(case when seller_type::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as seller_type
from sellers;

select count(distinct seller_id)
from sellers;

select author_name
from sellers 
group by 1 
having count(*) > 1;

update sellers
set author_name = trim(initcap(author_name));

select max(birthdate), min(birthdate)
from sellers;

select distinct country
from sellers;

select distinct seller_type
from sellers;

update sellers
set seller_type = trim(lower(seller_type));

---------------------
-- TRANSACTIONS
---------------------

select column_name, data_type
from information_schema.columns
where table_name = 'transactions';

alter table transactions
rename column price_paid to price;

select
	sum(case when transaction_id is null then 1 else 0 end) as transactions_id,
	sum(case when book_id is null then 1 else 0 end) as book_id,
	sum(case when buyer_id is null then 1 else 0 end) as buyer_id,
	sum(case when price is null then 1 else 0 end) as price,
	sum(case when discount_rate is null then 1 else 0 end) as discount_rate,
	sum(case when date is null then 1 else 0 end) as date
from transactions;

select 
	sum(case when transaction_id::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as transaction_id,
	sum(case when book_id::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as book_id,
	sum(case when buyer_id::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as buyer_id,
	sum(case when price::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as price,
	sum(case when discount_rate::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as discount_rate,
	sum(case when date::TEXT in ('-', '--', 'n/a', 'na', 'NA', 'N/A', '?', 'None', 'null', 'NULL', '') then 1 else 0 end) as date
from transactions;

select *
from transactions;

select count(distinct book_id) -- we only have 13 books, the rest must be cleaned
from transactions;

select * -- 14190 transactions are related to our books
from transactions
where book_id IN (select book_id from products);

delete from transactions
where book_id not in (select book_id from products); 

delete from transactions
where price < 0;

select distinct price
from transactions;

update transactions as t
set price = p.price
from products as p 
where p.book_id = t.book_id;

alter table transactions
add price_paid NUMERIC(10,2);

update transactions
set price_paid = price - (price * discount_rate);

select max(date), min(date)
from transactions;

select count(distinct transaction_id)
from transactions;

select count(distinct book_id)
from transactions;

---------------------
-- checking foreign keys
---------------------

select count(*) as missing_sellers
from products p 
left join sellers s on p.seller_id = s.seller_id
where s.seller_id is null;

select count(*) as missing_books
from reviews r
left join products p on r.book_id = p.book_id
where p.book_id is null;

select count(*) as missing_books
from transactions t
left join products p on t.book_id = p.book_id
where p.book_id is null;

select count(*) as missing_buyers
from transactions t
left join buyers b on t.buyer_id = b.buyer_id
where b.buyer_id is null;