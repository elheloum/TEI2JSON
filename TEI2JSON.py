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
import csv
from recup_children import *
from recup_attributes import *


def create_json(rng_file):
    """
    Ceci est l'étape de conversion TEI en JSON.
    :param rng_file:
    :return:
    """

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
            print("-- traitement de l'élément", name, "--")
            # attribuer à l'élement tag du json le nom de l'élement comme valeur
            element['tag'] = name

            # chercher le module auquel appartient l'élément
            element['module'] = []
            print("## traitement du module de l'élément", name, "##")
            with open('file_modules.csv', 'r') as csvfile:
                file_modules = csv.reader(csvfile, delimiter='\t')
                for row in file_modules:
                    if row[0] == name:
                        element['module'] = row[1]

            # chercher la documentation de l'élement
            element['documentation'] = []
            documentation = link.find({"a:documentation"})
            if documentation:
                element['documentation'] = documentation.string

            element['attributes'] = []
            print(" ~~ traitement des attributs de l'élément:", name, "~~")
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
                                                                    attribute = OrderedDict()
                                                                    for define_att_ref_2 in soup.find_all('define'):
                                                                        if define_att_ref_2:
                                                                            define_att_ref_name2 = define_att_ref_2.get(
                                                                                'name')
                                                                            if define_att_ref_name2 == deff_name:
                                                                                opt = define_att_ref_2.find('optional')
                                                                                if opt:
                                                                                    attribut = opt.find('attribute')
                                                                                    if attribut:
                                                                                        attribute_list = get_attributs(
                                                                                            attribut,
                                                                                            attribute)
                                                                                        # ajout de l'ensemble de l'élément attribute à l'élément attributs du json
                                                                                        element['attributes'].append(
                                                                                            attribute_list)
                                                # obtenir les noms des attribute que contiennet les grands "attributes'
                                                else:
                                                    attribute = OrderedDict()
                                                    for define_att_ref in soup.find_all('define'):
                                                        if define_att_ref:
                                                            define_att_ref_name = define_att_ref.get('name')
                                                            if define_att_ref_name == ref_name:
                                                                opt = define_att_ref.find('optional')
                                                                if opt:
                                                                    attribut = opt.find('attribute')
                                                                    if attribut:
                                                                        attribute_list = get_attributs(attribut,
                                                                                                       attribute)
                                                                        # ajout de l'ensemble de l'élément attribute à l'élément attributs du json
                                                                        element['attributes'].append(attribute_list)
            # récupération des attributs qui se trouvent dans l'élement
            for attribut in link.find_all('attribute'):
                attribute = OrderedDict()
                attribute_list = get_attributs(attribut, attribute)
                # ajout de l'ensemble de l'élément attribute à l'élément attributs du json
                element['attributes'].append(attribute_list)

            '''récupération des "enfants" '''
            # création de l'élement childrens dans le json
            element['childrens'] = []
            treated_elt = set()
            liste_children = []
            resultat = []
            print("** traitement des enfants de l'élément:", name, "**")
            for ref in link.find_all('ref'):
                name_ref = ref.get("name")
                if not name_ref.startswith("tei_att"):
                    resultat = handel_element(soup, name_ref, treated_elt, liste_children)
            if resultat:
                element['childrens'] = resultat

            # ajout de la totalité du contenu de l'élement dans le json
            content['elements'].append(element)

    # création du json
    with open("output/sortie_{0}".format(rng_file) + ".json", mode='w', encoding='UTF-8') as output:
        output.write(json.dumps(content, indent=4, sort_keys=False, ensure_ascii=False))


if __name__ == '__main__':
    """
        Lancement de la méthode
    """
    create_json(sys.argv[1])
