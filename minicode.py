import smtplib
import requests
from bs4 import BeautifulSoup as BS
from smtplib import SMTP
from email.message import EmailMessage
import re
import json
from threading import Timer
import tkinter as tk
from tkinter import simpledialog


# Define the static information


url = simpledialog.askstring(title="Input", prompt="Enter the URL:")
price = int(simpledialog.askstring(title="Input",prompt= "Enter the affordable price:"))
email = simpledialog.askstring(title="Input", prompt="Enter your Gmail address:")
# Amazon, Flipkart, Myntra, Nykaa, Snapdeal functions as before
def amaze():
    ind = url.find('?')
    urll = url[:ind]
    urll = str(urll)
    return urll
def amazon():
    global price
    global name
    urll = amaze()
    page = requests.get(urll, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"})
    soup = BS(page.content, "html.parser")
    name =soup.find(id='productTitle').text
    try:
        s = soup.find(class_="a-price-whole").text.split()[0].replace(".", "").replace(",", "")
        price = int(s)
        return price
    except AttributeError:
        price=2**31
        return price
page=requests.get(url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"})
#<-------------------------------Flipkart--------------------------------------->
def flipkart():
    global name
    global price
    soup = BS(page.content, "html.parser")
    try:
        name = soup.find(class_='B_NuCI').text
    except AttributeError:
        print()
    try:
        s = soup.find(class_="_30jeq3 _16Jk6d").text.split()[0].replace(",", "")
        price = int(s[1:])
        return price
    except AttributeError:
        price=2**31
        return price
#<-----------------------------------Myntra----------------------------------------->
def myntra():
    global name
    global price
    try:
        match = re.findall(r"<script>window.__myx = (.+?)</script>", page.text)
        json_data = json.loads(match[0])
        name = product_name = json_data['pdpData']['name']
        price = json_data['pdpData']['price']['discounted']
        return price
    except:
        price=2**31
        return price
#<-----------------------------Nykaa------------------------>
def nykaa():
    global name
    global price
    soup = BS(page.content, "html.parser")
    name = soup.find(class_="css-1gc4x7i").text
    try:
        s = soup.find(class_="css-1jczs19").text.split()[0].replace(",", "")
        price = int(s[1:])
        return price
    except AttributeError:
        price= 2**31
        return price

#<-----------------------------Snapdeal------------------------------------>
def snapdeal():
    global name
    global price
    soup = BS(page.content, "html.parser")
    name = soup.find(class_="pdp-e-i-head").text
    try:
        s = soup.find(class_="payBlkBig").text.split()[0]
        price = int(s[0:])
        return price
    except AttributeError:
        price=2**31
        return price


# Email function as before
def notify():
    email_id = 'battumittu98@gmail.com'
    email_pass = 'ldssnddvwiiartqs'

    msg = EmailMessage()
    msg['Subject'] = 'Price Drop Alert!'
    msg['From'] = email_id
    msg['To'] = email  # receiver address
    msg.set_content(f'Hey, price of product dropped!\n{url}')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_id, email_pass)
        smtp.send_message(msg)

# Delete function as before

# Get function with static data
def get():
    if (url.find("amazon") >= 0 and amazon() <= price):
        notify()
        print('Mail sent!')
    if (url.find("flipkart") >= 0 and flipkart() <= price):
        notify()
        print('Mail sent!')
    elif (url.find("myntra") >= 0 and myntra() <= price):
        notify()
        print('Mail sent!')
    elif (url.find("nykaa") >= 0 and nykaa() <= price):
        notify()
        print('Mail sent!')
    elif (url.find("snapdeal") >= 0 and snapdeal() <= price):
        notify()
        print('Mail sent!')
    else:
        print(' the mail Will be sent soon !')
        print('happy shopping')
    Timer(10, get).start()

get()
root = tk.Tk()

# Create a button that triggers the input dialog
input_button = tk.Button(root, text="Input", command=get_user_input)
input_button.pack()

# Start the Tkinter main loop
root.mainloop()