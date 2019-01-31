#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import requests


def test():
    modules_tei = ['core', 'header', 'textstructure', 'analysis', 'certainty',  'corpus', 'dictionaries', 'drama',
                   'figures', 'gaiji', 'iso-fs', 'linking', 'msdescription', 'namesdates', 'nets', 'spoken',
                   'tagdocs', 'textcrit', 'transcr', 'verse']
    modules = {}
    for name in modules_tei:
        url2 = 'http://roma.tei-c.org/startroma.php?mode=changeModule&module='+name
        r2 = requests.get(url2)
        data2 = r2.text
        soup2 = BeautifulSoup(data2, features='lxml')
        tbody = soup2.find('table')
        if tbody:
            tr_module = tbody.find('tr')
            td = tr_module.find('td').get_text()
            liste = td.split(':')
            module = liste[1]
            tr = tbody.find_all('tr')
            for t in tr:
                td = t.find('td').get_text()
                modules[td] = module
    return modules
