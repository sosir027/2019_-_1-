import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import pandas as pd

# Databasae Attributes
columns = ['FIELD', 'SUBNAME', 'SUBCODE', 'CREDIT']
datas = []


# web crawling
def crawling(urls):
    for url in urls:
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        subs = soup.select('tbody > tr')

        for sub in subs:
            codefilter = re.compile('\(L[A-Z][0-9]{6}\)')
            text = list(filter(lambda x: x not in ('', ' ', '  '), re.split('\t|\n| {2,}$', sub.text)))
            subcode = list(filter(lambda x: x != '', re.split('\(|\)', codefilter.findall(sub.text)[0])))[0]

            text[1] = text[1].replace(f'({subcode})  ', '')
            text.insert(2, subcode)
            datas.append(text[:-2])



# sqlite3 database construct
def db_construct():
    print("== database constructing ==")
    conn = sqlite3.connect('subjects.db')
    c = conn.cursor()
    sql = "insert or ignore into subjects (field, subname, subcode, credit) values (?,?,?,?)"
    c.execute('CREATE TABLE if not exists subjects (FIELD text, SUBNAME text, SUBCODE text unique, CREDIT integer)')
    for data in datas:
        print(data)
        c.execute(sql, (data[0], data[1], data[2], int(data[3])))

    conn.commit()
    conn.close()

# csv file create
def create_csv():
    dataFrame = pd.DataFrame([columns] + datas)
    dataFrame.to_csv('./datas.csv', encoding='euc-kr', index=False, header=False)

# Web URL registration
links = []

'''
 * 단과대
 인문과학대(hmnt), 사회과학대(ss), 법학대(law), 자연과학대(ns), 지식서비스공대(infoen), 헬웰대(hw), 뷰티생활산업국제대(bli), 사범대(instr), 미술대(art), 음대(mus),
 간호대(nurs), 융합문화예술대(cvart), 교양교대(refm)
'''

hmnt = []       # 인문과학대
ss = []         # 사회과학대
law = []        # 법학대
ns = []         # 자연과학대
infoen = []     # 지식서비스공대
hw = []         # 헬웰대
bli = []        # 뷰티생활선업국제대
instr = []      # 사범대
art = []        # 미대
mus = []        # 음대
nurs = []       # 간호대
cvart = []      # 융합문화예술대
refm = []       # 교양교대

# 인문과학대
# 국어국문
hmnt += ['http://www.sungshin.ac.kr/korean/11157/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZrb3JlYW4lMkYwMSUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
       'http://www.sungshin.ac.kr/korean/11157/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZrb3JlYW4lMkYwMiUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
       'http://www.sungshin.ac.kr/korean/11157/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZrb3JlYW4lMkYwMyUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
       'http://www.sungshin.ac.kr/korean/11157/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZrb3JlYW4lMkYwNCUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2']

# 영어영문
hmnt += ['http://www.sungshin.ac.kr/english/11187/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZlbmdsaXNoJTJGMDElMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none',
         'http://www.sungshin.ac.kr/english/11187/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZlbmdsaXNoJTJGMDIlMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none',
         'http://www.sungshin.ac.kr/english/11187/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZlbmdsaXNoJTJGMDMlMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none',
         'http://www.sungshin.ac.kr/english/11187/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZlbmdsaXNoJTJGMDQlMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none']

# 독일어문
hmnt += ['http://www.sungshin.ac.kr/german/11218/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZnZXJtYW4lMkYwMSUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
         'http://www.sungshin.ac.kr/german/11218/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZnZXJtYW4lMkYwMiUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
         'http://www.sungshin.ac.kr/german/11218/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZnZXJtYW4lMkYwMyUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
         'http://www.sungshin.ac.kr/german/11218/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZnZXJtYW4lMkYwNCUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none']

# 불어불문
hmnt += ['http://www.sungshin.ac.kr/france/11248/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZmcmFuY2UlMkYwMSUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
         'http://www.sungshin.ac.kr/france/11248/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZmcmFuY2UlMkYwMiUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
         'http://www.sungshin.ac.kr/france/11248/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZmcmFuY2UlMkYwMyUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
         'http://www.sungshin.ac.kr/france/11248/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZmcmFuY2UlMkYwNCUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none']

# 일본어문
hmnt += ['http://www.sungshin.ac.kr/japanese/11284/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZqYXBhbmVzZSUyRjAxJTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none',
         'http://www.sungshin.ac.kr/japanese/11284/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZqYXBhbmVzZSUyRjAyJTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none',
         'http://www.sungshin.ac.kr/japanese/11284/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZqYXBhbmVzZSUyRjAzJTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none',
         'http://www.sungshin.ac.kr/japanese/11284/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZqYXBhbmVzZSUyRjA0JTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none']

# 중어중문
hmnt += ['http://www.sungshin.ac.kr/chinese/11320/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjaGluZXNlJTJGMDElMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none',
         'http://www.sungshin.ac.kr/chinese/11320/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjaGluZXNlJTJGMDIlMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none',
         'http://www.sungshin.ac.kr/chinese/11320/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjaGluZXNlJTJGMDMlMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none',
         'http://www.sungshin.ac.kr/chinese/11320/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjaGluZXNlJTJGMDQlMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none']

# 사학과
hmnt += ['http://www.sungshin.ac.kr/history/11349/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZoaXN0b3J5JTJGMDElMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none',
         'http://www.sungshin.ac.kr/history/11349/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZoaXN0b3J5JTJGMDIlMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none',
         'http://www.sungshin.ac.kr/history/11349/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZoaXN0b3J5JTJGMDMlMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none',
         'http://www.sungshin.ac.kr/history/11349/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZoaXN0b3J5JTJGMDQlMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none']

# 사회과학대
# 법학대
# 자연과학대

# 지식서비스공대
# 청정융합에너지공학
infoen += ['http://www.sungshin.ac.kr/clean/11838/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjbGVhbiUyRjAxJTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none',
           'http://www.sungshin.ac.kr/clean/11838/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjbGVhbiUyRjAyJTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none',
           'http://www.sungshin.ac.kr/clean/11838/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjbGVhbiUyRjAzJTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none',
           'http://www.sungshin.ac.kr/clean/11838/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjbGVhbiUyRjA0JTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none']

# 바생공
infoen += ['http://www.sungshin.ac.kr/bte/11874/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZidGUlMkYwMSUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
           'http://www.sungshin.ac.kr/bte/11874/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZidGUlMkYwMiUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
           'http://www.sungshin.ac.kr/bte/11874/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZidGUlMkYwMyUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
           'http://www.sungshin.ac.kr/bte/11874/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZidGUlMkYwNCUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none']

# 바식공
infoen += ['http://www.sungshin.ac.kr/bif/11852/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZiaWYlMkYwMSUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
           'http://www.sungshin.ac.kr/bif/11852/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZiaWYlMkYwMiUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
           'http://www.sungshin.ac.kr/bif/11852/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZiaWYlMkYwMyUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
           'http://www.sungshin.ac.kr/bif/11852/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZiaWYlMkYwNCUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none']

# 융보공
infoen += ['http://www.sungshin.ac.kr/cse/11782/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjc2UlMkYwMSUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
           'http://www.sungshin.ac.kr/cse/11782/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjc2UlMkYwMiUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
           'http://www.sungshin.ac.kr/cse/11782/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjc2UlMkYwMyUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
           'http://www.sungshin.ac.kr/cse/11782/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjc2UlMkYwNCUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none']

# 컴공
infoen += ['http://www.sungshin.ac.kr/ce/11804/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjZSUyRjAxJTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none',
           'http://www.sungshin.ac.kr/ce/11804/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjZSUyRjAyJTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none',
           'http://www.sungshin.ac.kr/ce/11804/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjZSUyRjAzJTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none',
           'http://www.sungshin.ac.kr/ce/11804/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZjZSUyRjA0JTJGYXJ0Y2xMaXN0LmRvJTNGeWVhciUzRDIwMTklMjY%3D#none']

# 정시공
infoen += ['http://www.sungshin.ac.kr/infosys/11819/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZpbmZvc3lzJTJGMDElMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none',
           'http://www.sungshin.ac.kr/infosys/11819/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZpbmZvc3lzJTJGMDIlMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none',
           'http://www.sungshin.ac.kr/infosys/11819/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZpbmZvc3lzJTJGMDMlMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none',
           'http://www.sungshin.ac.kr/infosys/11819/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZpbmZvc3lzJTJGMDQlMkZhcnRjbExpc3QuZG8lM0Z5ZWFyJTNEMjAxOSUyNg%3D%3D#none']

# 서디공
infoen += ['http://www.sungshin.ac.kr/serdesign/11767/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZzZXJkZXNpZ24lMkYwMSUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
           'http://www.sungshin.ac.kr/serdesign/11767/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZzZXJkZXNpZ24lMkYwMiUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
           'http://www.sungshin.ac.kr/serdesign/11767/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZzZXJkZXNpZ24lMkYwMyUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none',
           'http://www.sungshin.ac.kr/serdesign/11767/subview.do?enc=Zm5jdDF8QEB8JTJGY3JjbG0lMkZzZXJkZXNpZ24lMkYwNCUyRmFydGNsTGlzdC5kbyUzRnllYXIlM0QyMDE5JTI2#none']

# 헬웰대
# 뷰티생활선업국제대
# 사범대
# 미대
# 음대
# 간호대
# 융합문화예술대
# 교양교대

crawling(infoen)
db_construct()
