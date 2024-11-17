import pandas as pd
import requests
from bs4 import BeautifulSoup

url="https://dealsheaven.in/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

page=requests.get(url)
page

soup=BeautifulSoup(page.content)
soup


orginalprice=[]
discountprice=[]
description=[]
discount=[]

names=soup.find_all('div',class_="discount")
for i in names:
    name=i.text
    discount.append(name)
discount=discount[0:40]
print(discount)
len(discount)

desc = soup.find_all('div',class_='deatls-inner')
description = []
for element in desc:
    name = element.get_text(strip=True)  # Extract and clean text
    description.append(name)  # Append the text to the list
description = description[:40]
print(description)
print(len(description))


orginalprice_elements = soup.find_all('p', class_="price") 
orginalprice = [] 
for price_element in orginalprice_elements:
    price = price_element.get_text(strip=True)  
    orginalprice.append(price) 
orginalprice = orginalprice[:40]  
print(orginalprice) 
print(len(orginalprice)) 


discountprice_elements = soup.find_all('p', class_="spacail-price")
discountprice = []
for element in discountprice_elements:
    price = element.get_text(strip=True) 
    discountprice.append(price) 
discountprice = discountprice[:40]
print(discountprice)
print(len(discountprice))

df=pd.DataFrame({"Description":description,"orginal prices":orginalprice,"Discount price":discountprice,"discount":discount})
print(df)

filename = "Deals.csv"
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Description", "Original Price", "Discounted Price","Discount"])
    for i in range(len(discount)):
        writer.writerow([description[i], orginalprice[i], discountprice[i],discount[i]])
print(f"Data has been written to {filename}")