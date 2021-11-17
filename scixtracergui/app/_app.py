from pathlib import Path
import subprocess
from PySide2.QtWidgets import (QVBoxLayout, QWidget, QLabel, QHBoxLayout)

from scixtracer.config import ConfigAccess

from scixtracergui.framework import SgComponent, SgAction
from scixtracergui.widgets import SgThemeAccess, SgAppBar, SgStaticStackedWidget
from scixtracergui.home import SgHomeStates, SgHomeContainer, SgHomeComponent
from scixtracergui.browser import (SgBrowserContainer, 
                                   SgBrowserComponent,
                                   SgBrowserModel,
                                   SgBrowserStates)
from scixtracergui.experiment import (SgExperimentCreateStates,
                                      SgExperimentCreateContainer, 
                                      SgExperimentCreateComponent,
                                      SgExperimentCreateModel,
                                      SgExperimentComponent)


class SciXtracerApp(SgComponent):
    def __init__(self, bar_position='left'):
        super().__init__()

        self.browser_tab_id = -1
        self.toolboxes_tab_id = -1

        # containers    
        self.homeContainer = SgHomeContainer()
        self.experimentCreateContainer = SgExperimentCreateContainer()
        self.browserContainer = SgBrowserContainer()

        # components
        self.homeComponent = SgHomeComponent(self.homeContainer)
        self.experimentCreateComponent =  SgExperimentCreateComponent(self.experimentCreateContainer)
        self.browserComponent = SgBrowserComponent(self.browserContainer)

        # models
        self.experimentCreateModel = SgExperimentCreateModel(self.experimentCreateContainer)
        self.browserModel = SgBrowserModel(self.browserContainer)

        # register
        self.homeContainer.register(self)
        self.experimentCreateContainer.register(self)
        self.browserContainer.register(self)

        # init
        self.browserContainer.currentPath = str(Path.home())
        self.browserContainer.emit(SgBrowserStates.DirectoryModified)

        # widgets
        self.widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.widget.setLayout(layout)
        
        self.mainBar = SgAppBar()
        self.mainBar.setStyleSheet('QLabel{background-color:red;}')
        #self.mainBar.setStyleSheet('QLabel{background-color:#414851;}')
        self.mainBar.close.connect(self.remove_tab)
        self.stackedWidget = SgStaticStackedWidget(self.widget)

        if bar_position == 'left':
            layout.addWidget(self.mainBar)
            layout.addWidget(self.stackedWidget)
        else:
            layout.addWidget(self.stackedWidget) 
            layout.addWidget(self.mainBar)
             

        self.mainBar.open.connect(self.slide_to)


        # home component
        self.mainBar.addButton(SgThemeAccess.instance().icon('home'), "Home", 0, False)
        self.stackedWidget.addWidget(self.homeComponent.get_widget())
        self.mainBar.setChecked(0, True)


    def update(self, action: SgAction):
        print('app update on action:', action.state)
        if action.state == SgHomeStates.OpenNewExperiment:
            self.experimentCreateComponent.get_widget().setVisible(True)
        elif action.state == SgExperimentCreateStates.CancelClicked:
            self.experimentCreateComponent.get_widget().setVisible(False)   
        if action.state == SgExperimentCreateStates.ExperimentCreated:
            uri = self.experimentCreateContainer.experiment_dir
            print('open new experiment from:', uri)
            self.open_experiment(uri)
            self.experimentCreateComponent.get_widget().setVisible(False) 
        elif action.state == SgHomeStates.OpenBrowser:
            self.open_browser()
        elif action.state == SgBrowserStates.OpenExperiment:
             self.open_experiment(self.browserContainer.openExperimentPath)   
        elif action.state == SgHomeStates.OpenExperiment:
            self.open_experiment(self.homeContainer.clicked_experiment)                                 

    def open_experiment(self, uri):
        # instantiate
        print('open experiment:', uri)
        experimentComponent = SgExperimentComponent(uri)
        experimentComponent.experimentContainer.register(self)
        self.add_tab(experimentComponent.get_widget(), 
                     SgThemeAccess.instance().icon('database'), 
                     "Experiment", True)    
                         
    def add_tab(self, widget, icon, name, closable=False):
        # fill tab and widget
        self.stackedWidget.addWidget(widget)
        tab_idx = self.stackedWidget.count()-1
        self.mainBar.addButton(icon,  name, tab_idx, closable)
        # slide to it
        self.stackedWidget.slideInIdx(tab_idx)
        self.mainBar.setChecked(tab_idx, True)
        return tab_idx

    def remove_tab(self, idx):
        self.mainBar.removeButton(idx)
        self.stackedWidget.remove(idx)
        self.stackedWidget.slideInIdx(0)
        self.mainBar.setChecked(0, True)

    def slide_to(self, id: int):
        self.stackedWidget.slideInIdx(id)
        self.mainBar.setChecked(id, False)

    def open_browser(self):
        if self.browser_tab_id < 0:
            self.stackedWidget.addWidget(self.browserComponent.get_widget())
            self.browser_tab_id = self.stackedWidget.count()-1
            self.mainBar.addButton(SgThemeAccess.instance().icon('open-folder_negative'), 
                                   "Browser", 
                                   self.browser_tab_id, False)

        self.stackedWidget.slideInIdx(self.browser_tab_id)
        self.mainBar.setChecked(self.browser_tab_id, True)

    def open_toolboxes(self):
        print("open toolboxes:", self.toolboxes_tab_id)
        if self.toolboxes_tab_id < 0:
            self.stackedWidget.addWidget(self.finderComponent.get_widget())
            self.toolboxes_tab_id = self.stackedWidget.count()-1
            self.mainBar.addButton(SgThemeAccess.instance().icon('tools'), 
                                   "Toolboxes", 
                                   self.toolboxes_tab_id, False)

        self.stackedWidget.slideInIdx(self.toolboxes_tab_id)
        self.mainBar.setChecked(self.toolboxes_tab_id, True)
    
    def get_widget(self):
        return self.widget    
