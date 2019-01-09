#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import json
from collections import OrderedDict
import csv


def findatt():
    file = open('myTEI-4.rng', mode='r', encoding='UTF-8')
    xml = file.read()
    file.close()
    soup2 = BeautifulSoup(xml, 'xml')
    tab_att = []
    for ref in soup2.find_all('define'):
        """
        reference = ref.find('ref')
        # print(reference)
        if reference:
            attribut = reference.get('name')
            if str(attribut).startswith("tei_att"):
                print(attribut)
        """
        if ref:
            attribut = ref.get('name')
            if str(attribut).startswith("tei_att"):
                tab_att.append(attribut)
    print(tab_att)


def findmodel():
    file = open('myTEI-4.rng', mode='r', encoding='UTF-8')
    xml = file.read()
    file.close()
    soup2 = BeautifulSoup(xml, 'xml')
    tab_model = []
    tab_ref = []
    tab = {}
    content = {'modeles': []}
    for model in soup2.find_all('define'):
        modele = OrderedDict()
        if model:
            mod = model.get('name')
            if str(mod).startswith("tei_model"):
                ref = model.find_all('ref')
                if ref:
                    modele['modele'] = mod
                    content['modeles'].append(modele)
    print(json.dumps(content))
                    # print(mod)
                    # print(ref)
                # tab_model.append(mod)
                # tab_ref.append(ref)
                    #tab[mod] = ref
    # print(tab)
    # print(tab_model)
    """
    with open("sortie_model.csv", 'wb') as modeles:
            sortie = csv.writer(modeles, delimiter=',')
            for key, value in tab.values():
                sortie.writerow(key)
                sortie.writerow(value)
    """


def create_json(rng_file):
    file = open(rng_file, mode='r', encoding='UTF-8')
    xml = file.read()
    file.close()
    content = {'elements': []}
    # att = {'attributs':[]}
    soup = BeautifulSoup(xml, 'xml')
    # print(soup.find_all('element'))

    for link in soup.find_all('element'):
        element = OrderedDict()

        name = link.get('name')
        if name:
            element['tag'] = name
            element['self-closed'] = False
            documentation = link.find('a:documentation')
            if documentation:
                element['documentation'] = documentation.string
            element['attributs'] = []
            for attribut in link.find_all('attribute'):
                attribute = OrderedDict()
                name_att = attribut.get('name')
                if name_att:
                    choice = attribut.find('choice')
                    liste_values = []
                    if choice:
                        type = 'Enumerated'
                        for value in choice.find_all('value'):
                            liste_values.append(value.string)
                    else:
                        type = 'String'
                        liste_values.append('NONE')
                    attribute['key'] = name_att
                    attribute['type'] = type
                    attribute['required'] = False
                    documentation = attribut.find('a:documentation')
                    if documentation:
                        attribute['documentation'] = documentation.string
                    attribute['value'] = liste_values
                element['attributs'].append(attribute)
            element['childrens'] = []
        content['elements'].append(element)
    print(json.dumps(content))
    # print(tab_ref)
    with open("sortie.json", mode='w', encoding='UTF-8') as output:
        output.write(json.dumps(content, indent=4, sort_keys=False))


if __name__ == '__main__':
    # create_json('myTEI-4.rng')
    findatt()
    # findmodel()
