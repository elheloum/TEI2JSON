#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


def file_tag(rng_file):
    """
    Ceci est l'étape 1 du traitement ! à lancer impérativement en premier !!
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

    # création de  liste qui contiendra tous les tag trouvé dans le fichier .rng
    file_in = open("element.txt", mode='r', encoding='UTF-8')
    element = file_in.read()
    elements = element.split("\n")
    file_in.close()

    return elements
