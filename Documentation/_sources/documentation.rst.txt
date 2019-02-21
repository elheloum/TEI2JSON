.. TEI to JSON documentation master file, created by
   sphinx-quickstart on Wed Feb 13 20:26:49 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Le projet 
==========

Description
***********

Comme son nom l'indique, le projet permet de générer des documents au format JSON à partir de documents de définition de la TEI (au format .rng). Ces documents de sortie contiendront :

* Les balises TEI correspondant à un certain module
* Les descriptions/documentations des balises TEI
* Les attributs ainsi que leurs valeurs
* Les enfants autorisés pour chaque balise

Il est composé de 3 modules qui seront détaillés ultérieurement. 

Langage
*******

Ce projet a été entièrement développé en Python 3.5


Configuration de l'environnement
=================================

Processus d'installation et de lancement
******************************************


1. Configurer l'environnement pour un bon fonctionnement ::

	pip install -r requirements.txt

2. Lancer la conversion depuis un terminal ::
	
	python TEI2JSON.py input/<nom_d_un_fichier_rng>


Description des modules
************************

.. toctree::
   :maxdepth: 2
   :caption: Contents:


.. automodule:: TEI2JSON
	:members:


.. automodule:: recup_attributes
	:members:


.. automodule:: recup_children
	:members:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
