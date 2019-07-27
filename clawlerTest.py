import requests
import pandas
import json
import sys
import os
from bs4 import BeautifulSoup
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')


def get_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/\
            537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        }

        r = requests.get(url=url, headers=headers)
        r.encoding = 'utf-8'
        content = r.text
        return content
    except:
        s = sys.exc_info()
        print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))
        return " ERROR "


def parse_try_report(content):
    try:
        soup = BeautifulSoup(content,'html.parser')
        row_datas = soup.find(name='tbody').find_all('tr')
        rows = []

        for r in row_datas:
            vals = list(map(lambda h: h.text, r.find_all('td')))
            rows.append(vals)

        heads = rows[0]
        vals_list = rows[1:]
        result = []

        # 過濾資料類型
        if not (any("肩寬" in head for head in heads) and any("胸圍" in head for head in heads)):
            return []

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


def parse_try_report_v2(content):
    try:
        soup = BeautifulSoup(content,'html.parser')
        row_datas = soup.find(name='tbody').find_all('tr')
        rows = []

        for r in row_datas:
            vals = list(map(lambda h: h.text, r.find_all('td')))
            rows.append(vals)

        heads = rows[0]
        vals_list = rows[1:]

        head_idx = [-1, -1]
        # 過濾資料類型
        for i in range(len(heads)):
            if "肩寬" in heads[i]:
                head_idx[0] = i
            elif "胸圍" in heads[i]:
                head_idx[1] = i

        if -1 in head_idx:
            return [], []

        x = []
        y = []
        for vals in vals_list:
            x.append(int(vals[head_idx[0]]))
            y.append(int(vals[head_idx[1]]))

        return x, y
    except:
        s = sys.exc_info()
        print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))
        return [], []


def show_scatter_plot(class_a, class_b):
    plt.scatter(class_a[0], class_a[1], color='blue')
    plt.scatter(class_b[0], class_b[1], color='red')

    plt.show()


def main():
    # content = get_content(try_report_url + '43333')
    # print(content)
    # parseTryReport(content)
    # return
    data = []

    for category in categorys:
        url_without_page_index = product_list_url + category
        content = ''
        product_list = []
        category_data = [[], []]

        page_index = 0
        while content != '[]':
            url = url_without_page_index + '&pageIndex=' + str(page_index)
            content = get_content(url)
            products = json.loads(content)
            product_list = product_list + products
            print('Page Index' + str(page_index) + ' - 資料筆數：' + str(len(products)))
            page_index = page_index + 1

        print('總筆數：' + str(len(product_list)))

        for p in product_list:
            style_no = p["image_140"].split("/")[2]
            print('Get Data, Style No: ' + style_no + '...')
            x, y = parse_try_report_v2(get_content(try_report_url + style_no))
            category_data[0] = category_data[0] + x
            category_data[1] = category_data[1] + y
        data.append(category_data)

    with open('data.json', 'w') as f:
        json.dump(data, f)
    show_scatter_plot(data[0], data[1])
    # po = pandas.read_json(json.dumps(data))
    # po.to_csv('/Users/Sean.Tai/PycharmProjects/lutiv_clawler/women.csv', encoding='utf_8_sig')


# 接口地址
product_list_url = 'https://www.lativ.com.tw/Product/GetNewProductCategoryList?MainCategory='
try_report_url = 'https://www.lativ.com.tw/Product/TryReport?styleNo='
categorys = ['MEN', 'WOMEN']

if __name__ == '__main__':
    main()
