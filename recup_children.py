#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def handle_element(soup, name, treated_elt, liste_children):
    """
        **Extraction des enfants**
        
        Fonction permettant de récupèrer les enfants de chaque élément. 
        
        Paramètres 

            * soup: (beautiful soup object) le rng traité 
            * name: (string) nom de l'élément traité
            * treated_elt:(list) liste des éléments déja traités (permet d'éviter de traiter plusieurs fois le même élément)
            * liste_children: (list) liste vide 
        
        :return: liste_children: (list) liste contenant les enfants
    
    """

    link = soup.find("define", {"name": name})

    if name not in treated_elt:
        treated_elt.add(name)
        not_allowed = link.find("notAllowed")
        if not_allowed:
            # print("dead")
            return liste_children

        element = link.find("element")
        if element:
            name_elt = element.get('name')
            # ajouter à la liste des enfants
            liste_children.append(name_elt)
            return liste_children

        for ref in link.find_all("ref"):
            name_ref = ref.get("name")
            if not name_ref.startswith("tei_att"):
                handle_element(soup, name_ref, treated_elt, liste_children)

    # print(liste_children)
    return liste_children
