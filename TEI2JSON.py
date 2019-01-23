#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author : Myriam EL HELOU and Sami BOUHOUCHE :)
"""

from bs4 import BeautifulSoup
import json
from collections import OrderedDict
import sys


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
        # récupération du nom de l'élément
        name = link.get('name')
        if name:
            # attribuer à l'élement tag du json le nom de l'élement comme valeur
            element['tag'] = name
            print(name)
            # chercher la documentation de l'élement
            documentation = link.find('a:documentation')
            if documentation:
                # ajouter la documentation à l'élement
                element['documentation'] = documentation.string
            element['attributs'] = []
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
                                                                                            type2 = 'Enumerated'
                                                                                            for value in choice.find_all(
                                                                                                    'value'):
                                                                                                liste_values.append(
                                                                                                    value.string)
                                                                                        else:
                                                                                            type2 = 'String'
                                                                                        attribute3['key'] = name_attr
                                                                                        attribute3['type'] = type2
                                                                                        attribute3['required'] = False
                                                                                        documentation = attr.find(
                                                                                            'a:documentation')
                                                                                        if documentation:
                                                                                            attribute3['documentation'] = documentation.string
                                                                                        attribute3['value'] = liste_values
                                                                                    element['attributs'].append(attribute3)
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
                                                                            type2 = 'Enumerated'
                                                                            for value in choice.find_all('value'):
                                                                                liste_values.append(value.string)
                                                                        else:
                                                                            type2 = 'String'
                                                                        attribute2['key'] = name_attr
                                                                        attribute2['type'] = type2
                                                                        attribute2['required'] = False
                                                                        documentation = attr.find('a:documentation')
                                                                        if documentation:
                                                                            attribute2['documentation'] = documentation.string
                                                                        attribute2['value'] = liste_values
                                                                    element['attributs'].append(attribute2)
            # récupération des attributs qui se trouvent dans l'élement
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
                    attribute['key'] = name_att
                    attribute['type'] = type
                    attribute['required'] = False
                    documentation = attribut.find('a:documentation')
                    if documentation:
                        attribute['documentation'] = documentation.string
                    attribute['value'] = liste_values
                # ajout de l'ensemble de l'élément attribute à l'élément attributs du json
                element['attributs'].append(attribute)
            # création de l'élement childrens dans le json

            '''récupération des "enfants" '''
            # création de l'élement childrens dans le json
            element['childrens'] = []
            children0 = link.find_all('zeroOrMore')
            children1 = link.find_all('oneOrMore')
            # children = []
            ''' enfants contenus dans les balises "zeroOrMore" '''
            for child in children0:
                refs = child.find_all('ref')
                ''' refs contenus dans les balises "zero or more" des attrbuts'''
                for ref in refs:
                    child_ref_name = ref.get('name')
                    ''' traitement des models '''
                    if child_ref_name.startswith("tei_model"):
                        ''' récupération des balises contenus dans les modèles '''
                        for defz in soup.find_all("define"):
                            defs_name = defz.get('name')
                            if defs_name:
                                if defs_name == child_ref_name:
                                    for def_ref in defz.find_all('ref'):
                                        def_ref_name = def_ref.get('name')
                                        if def_ref_name:
                                            ''' récupération des balises des modèles utilisés pour définir d'autres modèles contenu dans le défine d'autre modèle '''
                                            if def_ref_name.startswith("tei_model"):
                                                for defzz in soup.find_all("define"):
                                                    defs_name2 = defzz.get('name')
                                                    if defs_name2:
                                                        if defs_name2.startswith("tei_model"):
                                                            pass
                                                        elif defs_name2.startswith("tei_att"):
                                                            if defs_name2.endswith('attributes'):
                                                                for att_child in soup.find_all('define'):
                                                                    att_child_name = att_child.get('name')
                                                                    if att_child_name == defs_name2:
                                                                        for deff in att_child.find_all('ref'):
                                                                            deff_name = deff.get('name')
                                                                            for define_att_ref_2 in soup.find_all(
                                                                                    'define'):
                                                                                if define_att_ref_2:
                                                                                    define_att_ref_name2 = define_att_ref_2.get(
                                                                                        'name')
                                                                                    if define_att_ref_name2 == deff_name:
                                                                                        opt = define_att_ref_2.find('optional')
                                                                                        if opt:
                                                                                            attr = opt.find('attribute')
                                                                                            if attr:
                                                                                                name_attr = attr.get('name')
                                                                                                element['childrens'].append(name_attr)
                                                            else:
                                                                for att_child in soup.find_all('define'):
                                                                    att_child_name = att_child.get('name')
                                                                    if att_child_name == defs_name2:
                                                                        opt = att_child.find('optional')
                                                                        if opt:
                                                                            attr = opt.find('attribute')
                                                                            if attr:
                                                                                name_attr = attr.get('name')
                                                                                element['childrens'].append(name_attr)
                                                        elif defs_name2.startswith("tei_macro"):
                                                            pass
                                                            ''' récupération des balises pour les modèles utilisés pour définir d'autres modèles et ajout à la liste des enfants '''
                                                        else:
                                                            element['childrens'].append(defs_name2[4:])
                                            else:
                                                element['childrens'].append(def_ref_name[4:])


            ''' enfants contenus dans les balises "oneOrMore" selon le même principe'''
            for child in children1:
                refs = child.find_all('ref')
                for ref in refs:
                    child_ref_name = ref.get('name')
                    ''' traitement des models '''
                    if child_ref_name.startswith("tei_model"):
                        ''' récupération des balises contenus dans les modèles '''
                        for defz in soup.find_all("define"):
                            defs_name = defz.get('name')
                            if defs_name:
                                if defs_name == child_ref_name:
                                    for def_ref in defz.find_all('ref'):
                                        def_ref_name = def_ref.get('name')
                                        if def_ref_name:
                                            ''' récupération des balises des modèles utilisés pour définir d'autres modèles contenu dans le défine d'autre modèle '''
                                            if def_ref_name.startswith("tei_model"):
                                                for defzz in soup.find_all("define"):
                                                    defs_name2 = defzz.get('name')
                                                    if defs_name2:
                                                        if defs_name2.startswith("tei_model"):
                                                            pass
                                                        elif defs_name2.startswith("tei_att"):
                                                            if defs_name2.endswith('attributes'):
                                                                for att_child in soup.find_all('define'):
                                                                    att_child_name = att_child.get('name')
                                                                    if att_child_name == defs_name2:
                                                                        for deff in att_child.find_all('ref'):
                                                                            deff_name = deff.get('name')
                                                                            for define_att_ref_2 in soup.find_all(
                                                                                    'define'):
                                                                                if define_att_ref_2:
                                                                                    define_att_ref_name2 = define_att_ref_2.get(
                                                                                        'name')
                                                                                    if define_att_ref_name2 == deff_name:
                                                                                        opt = define_att_ref_2.find('optional')
                                                                                        if opt:
                                                                                            attr = opt.find('attribute')
                                                                                            if attr:
                                                                                                name_attr = attr.get('name')
                                                                                                element['childrens'].append(name_attr)
                                                            else:
                                                                for att_child in soup.find_all('define'):
                                                                    att_child_name = att_child.get('name')
                                                                    if att_child_name == defs_name2:
                                                                        opt = att_child.find('optional')
                                                                        if opt:
                                                                            attr = opt.find('attribute')
                                                                            if attr:
                                                                                name_attr = attr.get('name')
                                                                                element['childrens'].append(name_attr)
                                                        elif defs_name2.startswith("tei_macro"):
                                                            pass
                                                            ''' récupération des balises pour les modèles utilisés pour définir d'autres modèles et ajout à la liste des enfants '''
                                                        else:
                                                            element['childrens'].append(defs_name2[4:])
                                            else:
                                                element['childrens'].append(def_ref_name[4:])
            for text in link.find_all('text'):
                if text:
                    element['childrens'].append("PCDATA")
            """
            '''élimination des doublons'''
            children = list(set(children))
            children = sorted(children,  key=str.lower)
            ''' ajout de l'ensemble des balises à element'''
            element['childrens'].append(children)
            """
        # ajout de la totalité du contenu de l'élement dans le json
        content['elements'].append(element)
    # print(json.dumps(content))
    # création du json
    with open("sortie_{0}".format(rng_file)+".json", mode='w', encoding='UTF-8') as output:
        output.write(json.dumps(content, indent=4, sort_keys=False))

if __name__ == '__main__':
    create_json("myTEI-3.rng")
    #create_json(sys.argv[1])
