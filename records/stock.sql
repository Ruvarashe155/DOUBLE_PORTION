SELECT stock_id,date, user_id_id, records_stock.quantity as stock_quantity, records_allocation.quantity as allo_quantity,(records_stock.quantity-records_allocation.quantity) as stock FROM records_stock join records_allocation on records_allocation.stock_id_id=records_stock.stock_id
group by date,stock_id_id,id;






SELECT stock_id,date,units, user_id_id, records_stock.quantity as stock_quantity, records_allocation.quantity as allo_quantity,sum(records_stock.quantity) as total_quantity, sum(records_allocation.quantity) as allocated_quantity ,(records_stock.quantity-sum(records_allocation.quantity)) as stock FROM records_stock join records_allocation on records_allocation.stock_id_id=records_stock.stock_id
group by stock_id 
order by date

create or replace view stock_view as
SELECT stock_id,date,units, user_id_id, records_stock.quantity as stock_quantity, records_allocation.quantity as allo_quantity,sum(records_stock.quantity) as total_quantity, sum(records_allocation.quantity) as allocated_quantity ,(records_stock.quantity-sum(records_allocation.quantity)) as stock FROM records_stock join records_allocation on records_allocation.stock_id_id=records_stock.stock_id
group by stock_id
order by date


create or replace view stock_view2 as
SELECT stock_id,date, records_stock.quantity as stock_quantity, records_sales.quantity as sold_quantity,sum(records_stock.quantity) as total_quantity, sum(records_sales.quantity) as total_sold_quantity ,(records_stock.quantity-sum(records_sales.quantity)) as stock FROM records_stock join records_sales on records_sales.product_name_id=records_stock.stock_id
group by stock_id

oduct p on mp.product_name_id=p.product_id
LEFT JOIN records_s

create or replace view product_stock as
SELECT p.product_id,p.product_name,p.units,s.stock_id, sum(s.quantity) as total_quantity 
from records_stock s 
join records_manufactured_products mp on s.product_id_id=mp.m_id 
join records_our_product p on mp.product_name_id=p.product_id
group by p.product_name, p.product_id;




create or REPLACE view inventory as
select id, product_id ,product_name, (total_quantity-s.quantity) as stock from product_stock join records_sales s on product_stock.stock_id=s.product_name_id


create or replace view product_stock2 as
SELECT id ,p.product_id,p.product_name,p.units, sum(s.quantity)-COALESCE(SUM(sa.quantity),0) as total_quantity 
from records_stock s 
join records_manufactured_products mp on s.product_id_id=mp.m_id 
join records_our_product p on mp.product_name_id=p.product_id
left join records_sales sa on s.stock_id=sa.product_name_id
group by p.product_name, p.product_id;