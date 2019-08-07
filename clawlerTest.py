import requests
import pandas
import json
import sys
import os
from bs4 import BeautifulSoup
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

# get url content
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

# parse try report to json
def parse_try_report_json(content, gender):
    try:
        soup = BeautifulSoup(content,'html.parser')
        row_datas = soup.find(name='tbody').find_all('tr')
        rows = []

        for r in row_datas:
            vals = list(map(lambda h: h.text, r.find_all('td')))
            rows.append(vals)

        heads = rows[0]
        for i in range(len(heads)):
            if "身高" in heads[i]:
                heads[i] = "身高"
            elif "體重" in heads[i]:
                heads[i] = "體重"
            elif "體重" in heads[i]:
                heads[i] = "體重"
            elif "胸圍" in heads[i]:
                heads[i] = "胸圍"
            elif "肩寬" in heads[i]:
                heads[i] = "肩寬"
            elif "腰圍" in heads[i]:
                heads[i] = "腰圍"
            elif "臀圍" in heads[i]:
                heads[i] = "臀圍"
            elif "身高" in heads[i]:
                heads[i] = "身高"

        vals_list = rows[1:]
        result = []

        for vals in vals_list:
            obj = {}
            obj["gender"] = gender
            for i in range(len(heads)):
                obj[heads[i]] = vals[i]
            result.append(obj)

        return result
    except:
        s = sys.exc_info()
        print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))
        return []


def parse_data_for_plot(data):
    try:
        prop_a = "身高"
        prop_b = "肩寬"
        result = []
        for category_data_list in data:
            category_x = []
            category_y = []
            for dic in category_data_list:
                if not(prop_a in dic and prop_b in dic and bool(dic[prop_a].strip()) and bool(dic[prop_b].strip())):
                    continue
                category_x.append(float(dic[prop_a]))
                category_y.append(float(dic[prop_b]))
            result.append([category_x, category_y])

        print(result)
        return result[0], result[1]
    except:
        s = sys.exc_info()
        print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))
        return [], []


def show_scatter_plot(class_a, class_b):
    plt.scatter(class_a[0], class_a[1], color='blue')
    plt.scatter(class_b[0], class_b[1], color='red')
    plt.ylabel('Shoulder width')
    plt.xlabel('bust')

    plt.show()


def main():
    data = []
    if not os.path.isfile('lutiv.json'):
        for category in categorys:
            url_without_page_index = product_list_url + category
            content = ''
            product_list = []
            category_data = []

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
                category_data = category_data + parse_try_report_json(get_content(try_report_url + style_no), category)

            data.append(category_data)

        with open('lutiv.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)
    else:
        with open('lutiv.json', 'r', encoding='utf8') as f:
            data = json.load(f)

    men, women = parse_data_for_plot(data)
    show_scatter_plot(men, women)
    # po = pandas.read_json(json.dumps(data))
    # po.to_csv('/Users/Sean.Tai/PycharmProjects/lutiv_clawler/lutiv.csv', encoding='utf_8_sig')


# 資料 url
product_list_url = 'https://www.lativ.com.tw/Product/GetNewProductCategoryList?MainCategory='
try_report_url = 'https://www.lativ.com.tw/Product/TryReport?styleNo='
categorys = ['MEN', 'WOMEN']

if __name__ == '__main__':
    main()
