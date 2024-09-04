Description 
Created a grocery store web application having multiple user and one manager role.  
Manager has CRUD access/privilege whereas user can only buy and review the orders he/she 
made along with ability to view the shopping cart history. 

Technologies used. 
1.Flask – request,session,url_for,render_template,redirect, current_app, flash,flask 
purpose: to redirect the html pages, to fetch the values from database and display messages. 
2.Flask-SQLAlchemy : SQLAlchemy 
purpose: to store the data. 
3.sqlalchemy : text 
purpose: to fetch values using SQL queries written in text format. 
 
Default features for User role  -  
1. Adding product to the cart 
2. Updating/removing product from the cart 
3. Previous orders placed can be viewed. 
4. When the product is out of stock, user is not able to click on add to cart button 
5. Search bar to quickly search for any product. 
Default features for Manager role  -  
1. Adding/updating/deleting category 
2. Adding/updating/deleting product 
3. If already existing category or product is added then error message is displayed.  
Additional features  -  
1. Expiry date for the products. 
2. Product quantity selection cannot be negative or more than the available quantity. 
3. If login credentials are wrong throw error message. 
4. Summary is added which display sales bar graph of all categories and products. 
