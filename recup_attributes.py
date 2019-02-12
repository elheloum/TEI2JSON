#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict


def get_attributs(att, attribute_dict):
    name_att = att.get('name')
    if name_att:
        choice = att.find('choice')
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
        attribute_dict['key'] = name_att
        attribute_dict['type'] = type
        attribute_dict['required'] = False
        documentation = att.find({"a:documentation"})
        if documentation:
            attribute_dict['documentation'] = documentation.string
        attribute_dict['values'] = liste_values
    return attribute_dict
