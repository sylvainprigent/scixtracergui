import os
import qtpy.QtCore
from qtpy.QtWidgets import (QHBoxLayout, QWidget, QVBoxLayout, QTableWidget,
                               QTableWidgetItem, QLabel, QAbstractItemView)


import scixtracer as sx

from scixtracergui.framework import SgComponent, SgAction
from scixtracergui.widgets import SgFlowLayout
from scixtracergui.home.containers import SgHomeContainer
from scixtracergui.home.states import SgHomeStates
from scixtracergui.home.widgets import SgHomeTile
from scixtracergui.widgets import SgThemeAccess
from scixtracer.config import ConfigAccess


class SgHomeComponent(SgComponent):
    def __init__(self, container: SgHomeContainer):
        super().__init__()
        self._object_name = 'SgHomeComponent'
        self.container = container
        self.container.register(self)  

        # Widget
        self.widget = QWidget()
        self.widget.setObjectName('SgWidget')
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.widget.setLayout(layout)

        # main tiles
        btnsWidget = QWidget()
        btnsLayout = QHBoxLayout()
        btnsWidget.setLayout(btnsLayout)
        
        openNewExperimentTile = SgHomeTile('New \n experiment', SgThemeAccess.instance().icon('plus-black-symbol'), 'OpenNewExperiment')
        openBrowserTile = SgHomeTile('Open \n experiment', SgThemeAccess.instance().icon('open-folder_negative'), 'OpenBrowser')
        openDesignerTile = SgHomeTile('Pipeline \n designer', SgThemeAccess.instance().icon('workflow'), 'OpenDesigner')
        openBatchTile = SgHomeTile('Batch \n processing', SgThemeAccess.instance().icon('play'), 'OpenBatch')
        #openSettingsTile = BiHomeTile('Settings', SgThemeAccess.instance().icon('cog-wheel-silhouette'), 'OpenSettings')
        
        openNewExperimentTile.clickedSignal.connect(self.tileClicked)
        openBrowserTile.clickedSignal.connect(self.tileClicked)
        openDesignerTile.clickedSignal.connect(self.tileClicked)
        openBatchTile.clickedSignal.connect(self.tileClicked)
        btnsLayout.addWidget(openNewExperimentTile, 1, qtpy.QtCore.Qt.AlignRight)
        btnsLayout.addWidget(openBrowserTile,  0, qtpy.QtCore.Qt.AlignCenter)
        btnsLayout.addWidget(openDesignerTile,  0, qtpy.QtCore.Qt.AlignCenter)
        btnsLayout.addWidget(openBatchTile,  1, qtpy.QtCore.Qt.AlignLeft)
        #btnsLayout.addWidget(openSettingsTile,  1, qtpy.QtCore.Qt.AlignLeft)

        experimentsTitle = QLabel('Experiments')
        experimentsTitle.setObjectName('SgLabelFormHeader1')

        self.shortcutsWidget = QTableWidget()
        self.shortcutsWidget.setAlternatingRowColors(True)
        self.shortcutsWidget.setColumnCount(4)
        self.shortcutsWidget.verticalHeader().setVisible(False)
        self.shortcutsWidget.horizontalHeader().setStretchLastSection(True)
        self.shortcutsWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.shortcutsWidget.cellDoubleClicked.connect(self.cellDoubleClicked)
        self.shortcutsWidget.cellClicked.connect(self.cellClicked)
        self.shortcutsWidget.setHorizontalHeaderLabels(['', 'Name', 'Date', 'Author'])
        self.shortcutsWidget.verticalHeader().setDefaultSectionSize(12)
        
        self.emptyshortcutsWidget = QLabel("Your workspace is empty. \n Start creating a new experiment !")
        self.emptyshortcutsWidget.setObjectName('SgHomeEmpty')
        
        layout.addWidget(btnsWidget, 0)
        layout.addWidget(experimentsTitle, 0)
        layout.addWidget(self.shortcutsWidget, 1)
        layout.addWidget(self.emptyshortcutsWidget, 1, qtpy.QtCore.Qt.AlignCenter)

        self.fill_experiments()
    
    def fill_experiments(self):

        req = sx.Request()    
        workspace_dir = ConfigAccess.instance().config['workspace']
        self.container.experiments = req.experiments(workspace_dir)
        if len(self.container.experiments) == 0:
            self.shortcutsWidget.setVisible(False)
            self.emptyshortcutsWidget.setVisible(True)
        else:
            self.shortcutsWidget.setRowCount(len(self.container.experiments))
            i = -1
            for exp in self.container.experiments:
                i += 1
                iconLabel = QLabel(self.shortcutsWidget)
                iconLabel.setObjectName("SgBrowserExperimentIcon")
                self.shortcutsWidget.setCellWidget(i, 0, iconLabel)  
                self.shortcutsWidget.setItem(i, 1, QTableWidgetItem(exp['info'].name))  
                self.shortcutsWidget.setItem(i, 2, QTableWidgetItem(exp['info'].date))  
                self.shortcutsWidget.setItem(i, 3, QTableWidgetItem(exp['info'].author))  
            self.shortcutsWidget.setVisible(True)
            self.emptyshortcutsWidget.setVisible(False)    
        
    def tileClicked(self, action: str):
        if action == 'OpenNewExperiment':
            self.container.emit(SgHomeStates.OpenNewExperiment)
        elif action == 'OpenBrowser':
            self.container.emit(SgHomeStates.OpenBrowser)     
        elif action == 'OpenDesigner':
            self.container.emit(SgHomeStates.OpenDesigner)    
        elif action == 'OpenBatch':
            self.container.emit(SgHomeStates.OpenBatch)

    def cellClicked(self, row: int, col: int):
        for col in range(0, self.shortcutsWidget.columnCount()):
            self.shortcutsWidget.setCurrentCell(row, col, qtpy.QtCore.QItemSelectionModel.Select) 

    def cellDoubleClicked(self, row: int, col: int):
        self.container.clicked_experiment = self.container.experiments[row]['md_uri']
        self.container.emit(SgHomeStates.OpenExperiment)

    def update(self, action: SgAction):
        pass

    def get_widget(self):
        return self.widget
