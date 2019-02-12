#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def handel_element(soup, name, treated_elt, liste_children):

    """
    :param name: ref name or element name
    :return: list of childrens
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
                handel_element(soup, name_ref, treated_elt, liste_children)

    # print(liste_children)
    return liste_children
