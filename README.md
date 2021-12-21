# PURPOSE
- It transforms many xml files to a file of QIF format.
- QIF could be imported in Quicken Intuit Program

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


