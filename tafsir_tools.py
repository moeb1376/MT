from lxml.html import fromstring
from lxml.html.clean import Cleaner
import re
import requests


def get_tafsir_from_tebyan(AyehID):
    url = "https://zekr.tebyan.net/Webservices/Maref/Quran_v2.asmx/GetTafsir"
    payload = "{'AyehID':%d,'Tafsir':'6'}" % AyehID
    headers = {
        'Cookie': "TebyanWebsiteCookie=UD=5UN1OHB2bgY=&UK=xbPTu7QZyH4kNF5B14LzC/KTAn6Vgs8iBNBiTDHnBxnfsnDI77fCHQ==; ASP.NET_SessionId=fl0xkvrpikfsyynrkugvrtp5; __utma=152943164.856057815.1512813049.1523442561.1523442561.1; __utmc=152943164; __utmz=152943164.1523442561.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); SERVERID=www-teb3; _ga=GA1.2.856057815.1512813049; _gid=GA1.2.353950754.1531243672; __asc=3413eb1d164853c2fdb37d42e75; __auc=37f0860a1603aaf2db3f66e3fa3; StatusILogin=false; ZekrTebyanNet=#SourehID=1&Aye=7&TabIndex=2&ta=6&PageID=1",
        'Accept': "application/json",
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "e0bf9885-3520-41b4-a51c-a7f21108afcc"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text


def get_selected_tafsir(html, aye):
    doc = fromstring(html)
    tags = ['h2', 'h3', 'h4', 'h5', 'h6',
            'div', 'span',
            'img', 'area', 'map', 'p']
    args = {'meta': False, 'safe_attrs_only': False, 'page_structure': False,
            'scripts': True, 'style': True, 'links': True, 'remove_tags': tags}
    cleaner = Cleaner(**args)
    clean_data = cleaner.clean_html(doc).text_content()
    clean_data = str(clean_data).split('\n')
    min_distance = len(aye)
    selected_tafsir = ""
    for i in clean_data:
        if i == 'روایات و احادیث':
            break
        search_obj = re.match(r'[۰-۹]+\ -\ (.*)', i, re.M | re.I)
        if search_obj is None:
            continue
        str_temp = re.sub(r'\[[۰-۹]+\]', "", i, re.M | re.I)
        str_temp2 = re.match(r'[۰-۹]+\ -(.*)\*\*Aye\*\*\((.*)\)\*\*\/Aye\*\*$',
                             str_temp, re.M | re.I)
        if str_temp2 is not None:
            distance = len(aye) - len(str_temp2.group(2).replace('.', ''))
            if selected_tafsir == "":
                selected_tafsir = str_temp2.group(1)
            if min_distance > distance:
                min_distance = distance
                selected_tafsir = str_temp2.group(1)
    # with open('salam.txt', 'w') as f:
    #     f.write(selected_tafsir + ' ' + str(min_distance) +
    #             '\n' + str_temp2.group(2).replace('.', ''))
    #     f.write('\n')
    return selected_tafsir
