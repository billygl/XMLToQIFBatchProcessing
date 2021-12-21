import sys
from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET

arguments = len(sys.argv) - 1
folderpath = ""
if arguments == 1:
    folderpath = sys.argv[1]
else:
    print("usar: XMLtoQIF.py %FOLDER_PATH%")
    sys.exit()

db_categories_csv = "db/categories.csv"
db_products_csv = "db/products.csv"
output_path = "output.qif"
errors_path = "db/error.csv"

tpl_ini = "!Type:Cash\n"
tpl = """D%s
T-%s
P%s
L%s
^
"""

def findPayee(code):
    with open(db_products_csv, 'r', encoding="utf-8-sig") as read_obj:
        for line in read_obj:
            data = line.split(",")
            if data[0].strip() == code:
                return data[2].strip()
    return ""

def findCategory(payee):
    with open(db_categories_csv, 'r', encoding="utf-8-sig") as read_obj:
        for line in read_obj:
            data = line.split(",")
            if data[0].strip().lower() == payee.lower():
                return data[1].strip()
    return ""

def getExpenses(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    ns = {'ns': 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2', 
        'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2', 
        'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}
    details = []
    errors_payee = []
    errors_category = []
    date = root.findall('cbc:IssueDate', ns)[0].text
    print(date)
    total_amount = 0
    for line in root.findall('cac:InvoiceLine', ns):
        quantity = line.findall('cbc:InvoicedQuantity', ns)
        price = line.findall('cac:PricingReference', ns)
        alternative = price[0].findall('cac:AlternativeConditionPrice', ns)
        price_amount = alternative[0].findall('cbc:PriceAmount', ns)
        amount = round(float(quantity[0].text) * float(price_amount[0].text), 2)
        total_amount = total_amount + amount
        
        item = line.findall('cac:Item', ns)
        identification = item[0].findall('cac:SellersItemIdentification', ns)    
        id = identification[0].findall('cbc:ID', ns)
        
        description = item[0].findall('cbc:Description', ns)
        
        code = id[0].text
        desc = description[0].text
        
        payee = findPayee(code)
        if payee == "":
            errors_payee.append({'code': code, 'desc': desc})
        category = findCategory(payee)
        if category == "":
            errors_category.append(payee)        
        text = code + "\t" + desc + "\t" + str(amount) + "\t" + payee + "\t" + category 
        print(text)
        details.append({'code': code, 'category': category, 'payee': payee, 'amount': amount})
    print(total_amount)
    content = {
        'date': date,
        'details': details,
        'errors': {
            'payee': errors_payee,
            'category': errors_category
        }
    }
    return content

def toQif(content, output):
    date_parts = content['date'].split("-")
    #date = "MM/DD/YYYY"
    date = date_parts[1] + "/" + date_parts[2] + "/" + date_parts[0]
    details = content['details']
    
    for detail in details:
        #d t p l
        text = tpl % (date, detail['amount'], detail['payee'], detail['category'])
        output.write( text )

def showErrors(content):
    errors = content['errors']
    if len(errors['payee']) or len(errors['category']):
        with open (errors_path, 'w+') as errors_file:
            for error in errors['payee']:
                errors_file.write( "%s,%s\n" % (error['code'], error['desc']))
            for error in errors['category']:
                errors_file.write( error + "\n")
        errors_file.close()
        return True        
    return False

with open (output_path, 'w+') as output: #, encoding="utf-8-sig"
    output.write( tpl_ini )
    for f in listdir(folderpath):
        filepath = join(folderpath, f)
        if isfile(filepath):
            content = getExpenses(filepath)
            if showErrors(content):
                print("check errors in " + errors_path)
                break
            #output.write(content)
            toQif(content, output)
output.close()