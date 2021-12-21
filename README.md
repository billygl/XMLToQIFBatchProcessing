# PURPOSE
- It transforms many xml files to a file of QIF format.
- QIF could be imported in Quicken Intuit Program.
- It matches the EAN codes to the products database.
- The products match the cateegories database.

# PREPARE
- It uses 'boletas' folder as input data
- Export the xml file from the electronic invoice.

# DATABASE
- It uses
  - products.csv
  ````
  EAN,Product,Payee
  ````
  - categories.csv
  ````
  Payee,Category
  ````

# REQUIRMENTS
- python > 3.x

# RUN
````
XMLtoQIF.bat
````

# ERRORS
- It creates a db/error.csv to add missing products or categories not found in csv files


