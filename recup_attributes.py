#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict


def get_attributs(att, attribute_dict):
    """
        **Extraction des attributs**

        Cette fonction permet de récupèrer les attributs ainsi que leurs caractéristiques

        Paramètres :

            * att: (string) nom de l'attribut dont les valeurs sont récupèrées
            * attribute_dict: (OrderedDict) dictionnaire vide 

        Caractéristiques des attributs: 

            * Clé
            * Type
            * Required 
            * Documentation en FR ou en EN
        
        :return: attribute_dict: (OrderedDict) dictionnaire contenant les caractéristiques des attributs de l'élément traité
        
    """
    name_att = att.get('name')
    if name_att:
        choice = att.find('choice')
        liste_values = []
        if choice:
            type = 'Enumerated'
            for value in choice.find_all('value'):
                if value.string == None:
                    pass
                else:
                    liste_values.append(value.string)
        else:
            type = 'String'
        attribute_dict['key'] = name_att
        attribute_dict['type'] = type
        attribute_dict['required'] = False
        documentation = att.find({"a:documentation"})
        if documentation:
            attribute_dict['documentation'] = documentation.string
        attribute_dict['values'] = liste_values
    return attribute_dict
