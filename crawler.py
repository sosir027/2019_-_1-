import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

grade1_ce = 'http://www2.sungshin.ac.kr/ce/11804/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjZSUyRjAxJTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none'
grade2_ce = 'http://www2.sungshin.ac.kr/ce/11804/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjZSUyRjAyJTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none'
grade3_ce = 'http://www2.sungshin.ac.kr/ce/11804/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjZSUyRjAzJTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none'
grade4_ce = 'http://www2.sungshin.ac.kr/ce/11804/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjZSUyRjA0JTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none'

ce = [grade1_ce, grade2_ce, grade3_ce, grade4_ce]
columns = ['FIELD', 'SUBNAME', 'CREDIT']
ce_datas = [columns]

for url in ce:
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    # subs = soup.select(' tr > td.txt_l > a')
    subs = soup.select('tbody > tr')

    for sub in subs:
        ce_datas.append(list(filter(lambda x: x != '' and x != ' ', re.split('  |\t|\n|\r', sub.text)))[:-2])
        # ce_datas.append(list(filter(None, re.split('  |\t|\n', sub.text)))[:-2])
        print(ce_datas)

dataFrame = pd.DataFrame(ce_datas)
dataFrame.to_csv('./ce_datas.csv', encoding='euc-kr', index=False, header=False)
