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

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from ..ui.ui_archeocad import Ui_ArcheoCAD

from ..toolbox.ArcheoUtilities import Utilities, ArcheoEnconding
from ..core.ArcheoEngine import Engine
from ..toolbox.ArcheoExceptions import *

# superclass factorizing code for the two ArcheoCadDialog classes
class ArcheoCadSuperDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
    
    def selectedLayer(self):
        """Returns the selected layer."""
        
        if self.comboPointLayer.currentText():
            return Utilities.getVectorLayerByName(self.comboPointLayer.currentText())

    # adopted from 'points2one Plugin'
    # Copyright (C) 2010 Pavol Kapusta
    # Copyright (C) 2010, 2013 Goyo
    def populateEncodings(self, names):
        """Populates the combo box of available encodings."""
        
        self.comboEncoding.clear()
        self.comboEncoding.addItems(names)
        index = self.comboEncoding.findText(ArcheoEnconding.getDefaultEncoding('UTF-8'))
        if index == -1:
            index = 0  # Make sure some encoding is selected.
        self.comboEncoding.setCurrentIndex(index)        
      
    def populateLayerList(self):
        
        self.comboPointLayer.clear()  
        layerList = Utilities.getLayerNames([QGis.Point])
        self.comboPointLayer.addItems(layerList)
        self.comboPointLayer.setCurrentIndex(0)        
        
    def updateFieldCombos(self):
        
        self.comboGroup.clear()
        self.comboGeoChoice.clear()
        layer = self.selectedLayer()
        if layer is not None:            
            fields = layer.dataProvider().fields()
            for field in fields:
                name = field.name()
                self.comboGroup.addItem(name)
                self.comboGeoChoice.addItem(name)
    
    # adopted from 'points2one Plugin'
    # Copyright (C) 2010 Pavol Kapusta
    # Copyright (C) 2010, 2013 Goyo            
    def outFile(self):
        """Opens a file save dialog and sets the output file path."""
        
        outFilePath = Utilities.saveFileDialog(self)
        if not outFilePath:
            return
        self.setOutFilePath(outFilePath)
    
    def getOutputFilePath(self):
        """Returns the output file path."""
        
        return self.outFileLine.text()

    def setOutFilePath(self, outFilePath):
        """Sets the output file path."""
        
        self.outFileLine.setText(outFilePath)
        
    def groupAttrName(self):
        """Returns the name of the grouping attribute."""
        
        if self.chkBoxFieldGroup.isChecked():
            return unicode(self.comboGroup.currentText()) 
        
    def outputEncoding(self):
        """Returns the selected encoding for the output Shapefile."""
        
        return unicode(self.comboEncoding.currentText())
    
    def getGeoChoiceAttr(self):
        """Returns the name of the 'geometry choice' attribute """
        
        return unicode(self.comboGeoChoice.currentText())
    
    # adopted from 'points2one Plugin'
    # Copyright (C) 2010 Pavol Kapusta
    # Copyright (C) 2010, 2013 Goyo
    def showWarning(self, engine):
        
        logMsg = '\n'.join(engine.getLogger())
        if logMsg:
            warningBox = QMessageBox(self)
            warningBox.setWindowTitle('ArcheOCAD')
            message = QtGui.QApplication.translate("SDialog","le fichier shapefile de sortie a été créé.", None, QtGui.QApplication.UnicodeUTF8)
            warningBox.setText(message)
            message = QtGui.QApplication.translate("SDialog","Des problèmes ont été rencontrés, certaines formes n'ont peut-être pas pu être créées.", None, QtGui.QApplication.UnicodeUTF8)
            warningBox.setInformativeText(message)
            warningBox.setDetailedText(logMsg)
            warningBox.setIcon(QMessageBox.Warning)
            warningBox.exec_()        
    
    # adopted from 'points2one Plugin'
    # Copyright (C) 2010 Pavol Kapusta
    # Copyright (C) 2010, 2013 Goyo
    def addShapeToCanvas(self):
        message = unicode(QtGui.QApplication.translate("SDialog","Fichier shapefile de sortie créé:", None, QtGui.QApplication.UnicodeUTF8))
        message = '\n'.join([message, unicode(self.getOutputFilePath())])
        message = '\n'.join([message,
            unicode(QtGui.QApplication.translate("SDialog","Voulez-vous ajouter la nouvelle couche à votre projet?", None, QtGui.QApplication.UnicodeUTF8))])
        addToTOC = QMessageBox.question(self, "ArcheoCAD", message,
            QMessageBox.Yes, QMessageBox.No, QMessageBox.NoButton)
        if addToTOC == QMessageBox.Yes:
            Utilities.addShapeToCanvas(unicode(self.getOutputFilePath()))
            
    def hideDialog(self):        
        self.chkBoxFieldGroup.setCheckState(Qt.Unchecked)
        self.chkBoxSelected.setCheckState(Qt.Unchecked)
        self.outFileLine.clear()
        self.hide()
   