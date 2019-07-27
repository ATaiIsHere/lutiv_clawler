import requests
import pandas
import json
import sys
import os
from bs4 import BeautifulSoup

def get_content(url):

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        }

        r = requests.get(url=url, headers=headers)
        r.encoding = 'utf-8'
        content = r.text
        return content
    except:
        s = sys.exc_info()
        print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))
        return " ERROR "

def parseTryReport(content):
    try:
        soup = BeautifulSoup(content,'html.parser')
        row_datas = soup.find(name = 'tbody').find_all('tr')
        rows = []

        for r in row_datas:
            vals = list(map(lambda h: h.text, r.find_all('td')))
            rows.append(vals)

        heads = rows[0]
        vals_list = rows[1:]
        result = []

        for vals in vals_list:
            obj = {}
            for i in range(len(heads)):
                obj[heads[i]] = vals[i]
            result.append(obj)

        return result

    except:
        s = sys.exc_info()
        print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))
        return []

def main():
    # content = get_content(try_report_url + '43333')
    # print(content)
    # parseTryReport(content)
    # return

    content = ''
    product_list = []
    all = []

    pageIndex = 0
    while content != '[]':
        url = product_list_url + str(pageIndex)
        content = get_content(url)
        products = json.loads(content)
        product_list = product_list + products
        print('pageIndex' + str(pageIndex) + ' - 資料筆數：' + str(len(products)))
        pageIndex = pageIndex + 1

    print('總筆數：' + str(len(product_list)))

    for p in product_list:
        style_no = p["image_140"].split("/")[2]
        print('Get Data, Style No: ' + style_no + '...')
        parse_result = parseTryReport(get_content(try_report_url + style_no))
        all = all + parse_result

    print(all)
    po = pandas.read_json(json.dumps(all))
    po.to_csv('/Users/Sean.Tai/PycharmProjects/lutiv_clawler/women.csv', encoding='utf_8_sig')


# 接口地址
product_list_url = 'https://www.lativ.com.tw/Product/GetNewProductCategoryList?MainCategory=WOMEN&pageIndex='
try_report_url = 'https://www.lativ.com.tw/Product/TryReport?styleNo='

if __name__ == '__main__':
    main()