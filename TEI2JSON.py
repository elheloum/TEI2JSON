#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author : Myriam EL HELOU and Sami BOUHOUCHE :D
"""

from bs4 import BeautifulSoup
import json
from collections import OrderedDict
import sys
import requests


def file_tag(rng_file):
    """
    Ceci est l'étape 1 du traitement ! à lancer impérativement seule et en premier !!
    :param rng_file:
    :return:
    """
    file = open(rng_file, mode='r', encoding='UTF-8')
    xml = file.read()
    file.close()
    file_out = open("element.txt", mode='w', encoding='UTF-8')
    soup = BeautifulSoup(xml, 'xml')
    for link in soup.find_all('element'):
        # récupération du nom de l'élément
        name = link.get('name')
        if name:
            # écrire les éléments dans un fichier de sortie
            file_out.write(name + "\n")
    file_out.close()


def create_json(rng_file):
    """
    Ceci est l'étape 2 du traitement. A lancer impérativement après l'étape 1 !!
    :param rng_file:
    :return:
    """
    # création de  liste qui contiendra tous les tag trouvé dans le fichier .rng
    file_in = open("element.txt", mode='r', encoding='UTF-8')
    element = file_in.read()
    elements = element.split("\n")
    file_in.close()

    # début du traitement du rng
    file = open(rng_file, mode='r', encoding='UTF-8')
    xml = file.read()
    file.close()
    content = {'elements': []}
    soup = BeautifulSoup(xml, 'xml')

    for link in soup.find_all('element'):
        element = OrderedDict()
        # récupération du nom de l'élément
        name = link.get('name')
        if name:
            # attribuer à l'élement tag du json le nom de l'élement comme valeur
            element['tag'] = name
            # chercher la documentation de l'élement
            documentation = link.find({"a:documentation"})
            if documentation:
                # ajouter la documentation à l'élement
                element['documentation'] = documentation.string
                print("bye")
            element['attributes'] = []
            # récupération des attributs externes
            for att in link.find_all('ref'):
                if att:
                    attributs = att.get('name')
                    if str(attributs).startswith("tei_att"):
                        for define_att in soup.find_all('define'):
                            if define_att:
                                att_def = define_att.get('name')
                                if att_def.startswith('tei_att'):
                                    if att_def == attributs:
                                        for ref_att in define_att.find_all('ref'):
                                            if ref_att:
                                                ref_name = ref_att.get('name')
                                                if ref_name.endswith('.attributes'):
                                                    for define_atts in soup.find_all('define'):
                                                        if define_atts:
                                                            define_atts_name = define_atts.get('name')
                                                            if define_atts_name == ref_name:
                                                                for deff in define_atts.find_all('ref'):
                                                                    deff_name = deff.get('name')
                                                                    attribute3 = OrderedDict()
                                                                    for define_att_ref_2 in soup.find_all('define'):
                                                                        if define_att_ref_2:
                                                                            define_att_ref_name2 = define_att_ref_2.get('name')
                                                                            if define_att_ref_name2 == deff_name:
                                                                                opt = define_att_ref_2.find('optional')
                                                                                if opt:
                                                                                    attr = opt.find('attribute')
                                                                                    if attr:
                                                                                        name_attr = attr.get('name')
                                                                                        choice = attr.find('choice')
                                                                                        liste_values = []
                                                                                        if choice:
                                                                                            type2 = 'enumerated'
                                                                                            for value in choice.find_all(
                                                                                                    'value'):
                                                                                                if value.string == None:
                                                                                                    pass
                                                                                                else:
                                                                                                    liste_values.append(
                                                                                                        value.string)
                                                                                        else:
                                                                                            type2 = 'string'
                                                                                        attribute3['key'] = name_attr
                                                                                        attribute3['type'] = type2
                                                                                        attribute3['required'] = False
                                                                                        documentation = attr.find(
                                                                                            {"a:documentation"})
                                                                                        if documentation:
                                                                                            attribute3['documentation'] = documentation.string
                                                                                        attribute3['values'] = liste_values
                                                                                    element['attributes'].append(attribute3)
                                                # obtenir les noms des attribute que contiennet les grands "attributes'
                                                else:
                                                    attribute2 = OrderedDict()
                                                    for define_att_ref in soup.find_all('define'):
                                                        if define_att_ref:
                                                            define_att_ref_name = define_att_ref.get('name')
                                                            if define_att_ref_name == ref_name:
                                                                opt = define_att_ref.find('optional')
                                                                if opt:
                                                                    attr = opt.find('attribute')
                                                                    if attr:
                                                                        name_attr = attr.get('name')
                                                                        choice = attr.find('choice')
                                                                        liste_values = []
                                                                        if choice:
                                                                            type2 = 'enumerated'
                                                                            for value in choice.find_all('value'):
                                                                                if value.string == None:
                                                                                    pass
                                                                                else:
                                                                                    liste_values.append(value.string)
                                                                        else:
                                                                            type2 = 'string'
                                                                        attribute2['key'] = name_attr
                                                                        attribute2['type'] = type2
                                                                        attribute2['required'] = False
                                                                        documentation = attr.find({"a:documentation"})
                                                                        if documentation:
                                                                            attribute2['documentation'] = documentation.string
                                                                        attribute2['values'] = liste_values
                                                                    element['attributes'].append(attribute2)
            # récupération des attributs qui se trouvent dans l'élement
            for attribut in link.find_all('attribute'):
                attribute = OrderedDict()
                name_att = attribut.get('name')
                if name_att:
                    choice = attribut.find('choice')
                    liste_values = []
                    if choice:
                        type = 'enumerated'
                        for value in choice.find_all('value'):
                            if value.string == None:
                                pass
                            else:
                                liste_values.append(value.string)
                    else:
                        type = 'string'
                    attribute['key'] = name_att
                    attribute['type'] = type
                    attribute['required'] = False
                    documentation = attribut.find({"a:documentation"})
                    if documentation:
                        attribute['documentation'] = documentation.string
                    attribute['values'] = liste_values
                # ajout de l'ensemble de l'élément attribute à l'élément attributs du json
                element['attributes'].append(attribute)
            # création de l'élement childrens dans le json

            '''récupération des "enfants" '''
            # création de l'élement childrens dans le json
            element['childrens'] = []
            url = 'http://www.tei-c.org/release/doc/tei-p5-doc/fr/html/ref-' + name + '.html'

            r = requests.get(url)
            data = r.text
            soup2 = BeautifulSoup(data, features='lxml')
            for tr in soup2.find_all('tr'):
                label = tr.find("span", class_="label")
                if label:
                    if label.get_text() == "Peut contenir":
                        for td in tr.find('td', class_="wovenodd-col2"):
                            for childrenz in td.find_all('span', class_="specChildElements"):
                                childrenz_split = childrenz.get_text().split(' ')
                                for child in childrenz_split:
                                    if child in elements:
                                        element['childrens'].append(child)
            element['childrens'] = list(set(element['childrens']))

            # ajout de la totalité du contenu de l'élement dans le json
            content['elements'].append(element)

    # création du json
    with open("sortie_{0}".format(rng_file)+".json", mode='w', encoding='UTF-8') as output:
        output.write(json.dumps(content, indent=4, sort_keys=False))


if __name__ == '__main__':
    """
        Etape 1 
    """
    # file_tag("myTEI-3.rng")
    """
        Etape 2 
    """
    create_json("myTEI-3.rng")
    #create_json(sys.argv[1])
