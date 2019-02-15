#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        **Fonction principale du script**
        
        Cette fonction permet de convertir une documentation de la TEI sous le format Relax NG Schema ou .rng (généré depuis https://roma2.tei-c.org/) en format JSON.
            
        Entrée
            
            * rng-file(fichier .rng): fichier rng à traiter. celui-ci doit être  généré à partir de TEI-ROMA. Il doit contenir au minimum et obligatoirement les 3 modules suivants : 
                * Core
                * Header
                * Textstructure
        
        :return: rng-file.json (fichier .JSON) l'équivalent JSON du contenu du fichier .rng
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
            for references in link.find_all('ref'):
                if references:
                    # reference : nom de la référence dans l'élémént
                    reference = references.get('name')
                    if str(reference).startswith("tei_att"):
                        # recherche du define qui décrit cet attribut
                        for define_att in soup.find_all("define", {"name": reference}):
                            # recherche des attributs qui se trouvent dans la description de l'attribut père
                            for ref_att in define_att.find_all('ref'):
                                # si la référence récupérée correspond à une liste d'attributs
                                if ref_att and ref_att.get('name').endswith('.attributes'):
                                    for define_atts in soup.find_all("define", {"name": ref_att.get('name')}):
                                        for deff in define_atts.find_all('ref'):
                                            deff_name = deff.get('name')
                                            attribute = OrderedDict()
                                            for define_att_ref_2 in soup.find_all("define", {"name": deff_name}):
                                                attribut = define_att_ref_2.find('attribute')
                                                if attribut:
                                                    # gestion du remplissage du dictionnaire contenant les informations
                                                    # sur l'attribut en question
                                                    attribute_list = get_attributs(
                                                        attribut,
                                                        attribute)
                                                    # ajout de l'ensemble de l'élément attribute à l'élément attributs du json
                                                    element['attributes'].append(
                                                        attribute_list)
                                else:
                                    # si la référence récupérée correspond à un seul attribut
                                    attribute = OrderedDict()
                                    for define_att_ref in soup.find_all('define'):
                                        if define_att_ref:
                                            define_att_ref_name = define_att_ref.get('name')
                                            if define_att_ref_name == ref_att.get('name'):
                                                attribut = define_att_ref.find('attribute')
                                                if attribut:
                                                    # gestion du remplissage du dictionnaire contenant les informations
                                                    # sur l'attribut en question
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
                    resultat = handle_element(soup, name_ref, treated_elt, liste_children)
            if resultat:
                element['childrens'] = resultat

            # ajout de la totalité du contenu de l'élement dans le json
            content['elements'].append(element)

    rng_name = rng_file[6:]
    # création du json
    with open("output/sortie_{0}".format(rng_name) + ".json", mode='w', encoding='UTF-8') as output:
        output.write(json.dumps(content, indent=4, sort_keys=False, ensure_ascii=False))


if __name__ == '__main__':
    """
        Lancement de la méthode
    """
    create_json(sys.argv[1])
