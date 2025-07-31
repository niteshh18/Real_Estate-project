from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import datetime
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt #use to visualize dataset vallues

global username

def ViewMagicbrick(request):
    if request.method == 'GET':
        prices = []
        properties = []
        output = ""
        output+='<table border=1 align=center width=100%><tr><th><font size="3" color="black">Owner Name</th>'
        output+='<th><font size="3" color="black">Property Title</th><th><font size="3" color="black">Price</th>'
        output+='<th><font size="3" color="black">Property Details</th><th><font size="3" color="black">Image</th></tr>'
        dataset = pd.read_csv("ScrapeApp/static/magic.csv")
        dataset = dataset.values
        for i in range(1,len(dataset)):
            arr = dataset[i,2].strip("\n").strip().split(" ")
            for j in range(len(arr)):
                try:
                    value = arr[j].strip()
                    value = float(value.strip())
                    prices.append(value)
                    properties.append(dataset[i,1])
                except Exception:
                    pass    
            output+='<td><font size="3" color="black">'+str(dataset[i,0])+'</td>'
            output+='<td><font size="3" color="black">'+str(dataset[i,1])+'</td>'
            output+='<td><font size="3" color="black">'+str(dataset[i,2])+'</td>'
            output+='<td><font size="3" color="black">'+str(dataset[i,3])+'</td>'
            output+='<td><a href=\''+str(dataset[i,4])+'\ target = "_blank"><font size="3" color="black">View Image</a></td></tr>'
        plt.plot(properties, prices)
        plt.title("Magicbrick Prices")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()    
        context= {'data':output}
        return render(request, 'ViewOutput.html', context)

def ViewNoBroker(request):
    if request.method == 'GET':
        output = ""
        prices = []
        properties = []
        output+='<table border=1 align=center width=100%><tr><th><font size="3" color="black">Owner Name</th>'
        output+='<th><font size="3" color="black">Property Title</th><th><font size="3" color="black">Price</th>'
        output+='<th><font size="3" color="black">Property Details</th><th><font size="3" color="black">Image</th></tr>'
        dataset = pd.read_csv("ScrapeApp/static/nobroker.csv")
        dataset = dataset.values
        for i in range(len(dataset)):
            if len(prices) < 15:
                arr = str(dataset[i,2]).strip()
                value = arr
                try:
                    value = float(value.strip())
                    prices.append(value)
                    properties.append(dataset[i,1])
                except Exception:
                    pass  
            output+='<td><font size="3" color="black">'+str(dataset[i,0])+'</td>'
            output+='<td><font size="3" color="black">'+str(dataset[i,1])+'</td>'
            output+='<td><font size="3" color="black">'+str(dataset[i,2])+'</td>'
            output+='<td><font size="3" color="black">'+str(dataset[i,3])+'</td>'
            output+='<td><a href=\''+str(dataset[i,4])+'\ target = "_blank"><font size="3" color="black">View Image</a></td></tr>'
        plt.plot(properties, prices)
        plt.title("Nobroker Prices")
        plt.xticks(rotation=90)
        plt.show()       
        context= {'data':output}
        return render(request, 'ViewOutput.html', context)    

def scrapeMagic(url, headers, total):
    save_data = []
    for i in range(0, total):
        page = i + 1
        page_url = url + str(page)
        request = requests.get(page_url, headers=headers)
        html_soup = BeautifulSoup(request.text, 'html.parser')
        house_container = html_soup.find_all("div", {"class":"mb-srp__card__container"})
        for house in house_container:
            owner = house.find('div', attrs={'class':"mb-srp__card__ads--name"})
            availability = house.find_all('div', attrs={'class':"mb-srp__card__summary--label"})
            price = house.find('div', attrs={'class':"mb-srp__card--desc--text"})
            details = ""
            for avail in availability:
                details += avail.text+", "
            if owner is not None:
                owner = owner.text
            image = house.select("img")
            if len(image) > 0:
                image = image[0]
                if image.has_attr("title") and image.has_attr("data-src"):
                    title = image["title"]
                    image = image["data-src"]
                    save_data.append([owner, title, price.text, details, image])
    data = pd.DataFrame(save_data, columns=['owner', 'Title', 'Price', 'Details', 'Image'])
    data.to_csv("ScrapeApp/static/magic.csv", index=False)

def scrapeNoBroker(url, headers, total):
    save_data = []
    for i in range(0, total):
        page = i + 1
        page_url = url + str(page)
        request = requests.get(page_url, headers=headers)
        html_soup = BeautifulSoup(request.text, 'html.parser')
        house_container = html_soup.find_all("div", {"class":"flex flex-col flex-2 w-pe mt-1.8px po:justify-center po:p-1p po:mt-0 w-70pe"})
        for house in house_container:
            details= house.select("span", attrs={'class':"capitalize text-defaultcolor mb-0.5p font-semibold no-underline hover:text-primary-color po:overflow-hidden po:overflow-ellipsis po:max-w-95 po:m-0 po:font-normal cd:group-hover:text-primary-color cd:group-hover:nounderline"})
            det = house.find("span",attrs={'class':"flex items-center"})
            det = det.select("img")
            det = det[0]['src']
            all_details = ""
            owner = ""
            price = ""
            title = ""
            for span in details:
                if span.has_attr("itemprop"):
                    if span["itemprop"] == "price":
                        price = span.text
                    if span["itemprop"] == "startDate":
                        all_details += span.text+", "
                    if span["itemprop"] == "name":
                        if len(owner) == 0:
                            owner = span.text
                        else:
                            title = span.text
                    if span["itemprop"] == "streetAddress":
                        all_details += span.text+", "
                    if span["itemprop"] == "areaServed":
                        all_details += span.text+", "
                    if span["itemprop"] == "addressLocality":
                        all_details += span.text+", "
            save_data.append([owner, title, price, all_details, det])        
    data = pd.DataFrame(save_data, columns=['owner', 'Title', 'Price', 'Details', 'Image'])
    data.to_csv("ScrapeApp/static/nobroker.csv", index=False)
    

def ScrapeWebAction(request):
    if request.method == 'POST':
        page = request.POST.get('t1', False)
        total = request.POST.get('t2', False)
        save = request.POST.get('t3', False)
        total = int(total)
        headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        url = ""
        if page == 'Magic Brick':
            url = "https://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment&cityName=Hyderabad&BudgetMin=5000&BudgetMax=50000&page="
        else:
            url = "https://www.nobroker.in/property/rent/hyderabad/Hyderabad/?searchParam=W3sibGF0IjoxMy4wNDM3NjEyODI5MTkyLCJsb24iOjgwLjIwMDA2ODUxNjk2OTMsInNob3dNYXAiOmZhbHNlLCJwbGFjZUlkIjoiQ2hJSllUTjlULXBsVWpvUk05UmphQXVuWVc0IiwicGxhY2VOYW1lIjoiQ2hlbm5haSIsImNpdHkiOiJjaGVubmFpIn1d&sharedAccomodation=0&orderBy=nbRank,desc&radius=2&traffic=true&travelTime=30&propertyType=rent&pageNo="
        if page == 'Magic Brick':
            scrapeMagic(url, headers, total)
        else:
            scrapeNoBroker(url, headers, total)
        output = "Scrapping done for "+page+" & saved inside database"
        if save == "No":
            output = "Scrapping done for "+page
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)     

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})    

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})   

def ScrapeWeb(request):
    if request.method == 'GET':
       return render(request, 'ScrapeWeb.html', {})   
    
def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        status = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'ScrapeApp',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM register where username='"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                status = "exists"
        if status == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'ScrapeApp',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register(username,password,contact,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                context= {'data':'Signup Process Completed'}
                return render(request, 'Register.html', context)
            else:
                context= {'data':'Error in signup process'}
                return render(request, 'Register.html', context)
        else:
            context= {'data':'Username already exists'}
            return render(request, 'Register.html', context) 
        
def UserLogin(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        utype = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'ScrapeApp',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    utype = "success"
                    break
        if utype == 'success':
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        if utype == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)        
        
        
def AdminLoginAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username == 'admin' and password == 'admin':
            context= {'data':'welcome '+username}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'AdminLogin.html', context)


        
