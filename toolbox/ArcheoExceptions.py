# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArcheoCAD
                                 A QGIS plugin
 Génération d'une couche vectorielle de Polygone, Rectangle, Cercle et Ellipse.
                             -------------------
        begin                : 2014-04-08
        copyright            : (C) 2014 by Nariman Hatami - INRAP
        email                : nariman.hatami@inrap.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

#using Unicode for all strings
from __future__ import unicode_literals

from PyQt4 import QtGui

class FileDeletionError(Exception):
    """Exception raised when a file can't be deleted."""
    
    def __init__(self, fileName):
        self.fileName = fileName
        self.message = self.__str__()
        
    def __str__(self):
        msg = QtGui.QApplication.translate("Messages","Erreur lors de la suppression du fichier shapefile {0}", None, QtGui.QApplication.UnicodeUTF8)
        return msg.format(repr(self.fileName))
            
class UnknownAttributeError(Exception):
    """Exceptions raised when a feature attribute (field) is not found"""
    
    def __init__(self, layer, fieldName):
        self.layerName = layer
        self.fieldName = fieldName       
        self.message = self.__str__()
        
    def __str__(self):
        msg = QtGui.QApplication.translate("Exceptions", "L'attribut {0} n'existe pas sur la couche {1} ou la table d'attribut pas associée.", None, QtGui.QApplication.UnicodeUTF8) 
        return msg.format(repr(self.fieldName), repr(self.layerName))
        
class NoFeatureCreatedError(Exception):
    """Exception raised when no feature were created"""
    
    def __init__(self, filename):
        self.filename= filename
        self.message = self.__str__()
    
    def __str__(self):
        msg = QtGui.QApplication.translate("Exceptions", "Aucune frome n'a été créée. Tentative de suppression du fichier shapefile.{}\n.", None, QtGui.QApplication.UnicodeUTF8)
        return msg.format(self.filename)
