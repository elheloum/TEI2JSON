#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author : Myriam EL HELOU
"""
from bs4 import BeautifulSoup
import json
from collections import OrderedDict

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
        #récupération du nom de l'élément
        name = link.get('name')
        if name:
            #attribuer à l'élement tag du json le nom de l'élement comme valeur
            element['tag'] = name
            element['self-closed'] = False
            #chercher la documentation de l'élement
            documentation = link.find('a:documentation')
            if documentation:
                #ajouter la documentation à l'élement
                element['documentation'] = documentation.string
            element['attributs'] = []
            #liste qui contiendra les attributs (attributes)
            list_attributs = []
            # liste qui contiendra les attribut (attribute)
            list_ref = []
            #récupération des attributs externes
            for att in link.find_all('ref'):
                if att:
                    attributs = att.get('name')
                    if str(attributs).startswith("tei_att"):
                        list_attributs.append(attributs)
                    for define_att in soup.find_all('define'):
                        if define_att:
                            att_def = define_att.get('name')
                            if att_def.startswith('tei_att'):
                                if att_def == attributs:
                                    for ref_att in define_att.find_all('ref'):
                                        if ref_att:
                                            ref_name = ref_att.get('name')
                                            if ref_name.endswith('.attributes'):
                                                for ref_att2 in ref_att.find_all('ref'):
                                                    if ref_att2:
                                                        ref_name2 = ref_att2.get('name')
                                                        list_ref.append(ref_name2)
                                            else:
                                                list_ref.append(ref_name)
            print(name)
            print(list_attributs)
            print(list_ref)
            #récupération des attributs qui se trouvent dans l'élement
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
                #ajout de l'ensemble de l'élément attribute à l'élément attributs du json
                element['attributs'].append(attribute)
            #création de l'élement childrens dans le json
            element['childrens'] = []

        #ajout de la totalité du contenu de l'élement dans le json
        content['elements'].append(element)
    #print(json.dumps(content))
    #création du json
    with open("sortie_{0}".format(rng_file)+".json", mode='w', encoding='UTF-8') as output:
        output.write(json.dumps(content, indent=4, sort_keys=False))


if __name__ == '__main__':
    create_json('myTEI-4.rng')

