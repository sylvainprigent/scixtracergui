import sys
import os

import qtpy.QtCore
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                            QLabel, QTabWidget, QHBoxLayout, QMessageBox)

from scixtracergui.framework import SgAction, SgComponent

from scixtracergui.experiment.states import SgExperimentStates
from scixtracergui.experiment.containers import SgExperimentContainer
from scixtracergui.experiment.components import (SgExperimentToolbarComponent,
                                                 SgExperimentTableComponent,
                                                 SgExperimentImportComponent,
                                                 SgExperimentTagComponent)
from scixtracergui.experiment.models import SgExperimentModel
from scixtracergui.metadata.containers import SgMetadataExperimentContainer
from scixtracergui.metadata.components import SgMetadataExperimentComponent
from scixtracergui.metadata.models import SgMetadataExperimentModel
from scixtracergui.metadata.states import SgMetadataExperimentStates


class SgExperimentApp(SgComponent):
    def __init__(self, experiment_uri: str):
        super().__init__()

        # container
        self.expContainer = SgExperimentContainer()
        self.infoContainer = SgMetadataExperimentContainer()
        
        # components
        self.toolbarComponent = SgExperimentToolbarComponent(self.expContainer)
        self.tableComponent = SgExperimentTableComponent(self.expContainer)
        self.importComponent = SgExperimentImportComponent(self.expContainer)
        self.tagComponent = SgExperimentTagComponent(self.expContainer)

        self.infoComponent = SgMetadataExperimentComponent(self.infoContainer)

        # models
        self.experimentModel = SgExperimentModel(self.expContainer)
        self.infoModel = SgMetadataExperimentModel(self.infoContainer)

        # connections
        self.expContainer.register(self)

        # create the widget
        self.widget = QWidget()
        self.widget.setObjectName('SciXtracer experiment demo')
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.widget.setLayout(layout)

        self.tabWidget = QTabWidget()
        layout.addWidget(self.toolbarComponent.get_widget())
        layout.addWidget(self.tableComponent.get_widget())

        # load the experiment
        self.expContainer.experiment_uri = experiment_uri
        self.expContainer.emit(SgExperimentStates.ExperimentLoad)

    def update(self, action: SgAction):
        if action.state == SgExperimentStates.DataDoubleClicked:
            print('You double clicked:',
                  self.expContainer.selected_data_info.md_uri)
        if action.state == SgExperimentStates.RawDataClicked:
            print('You clicked the RAW data:',
                  self.expContainer.selected_data_info.md_uri)
        if action.state == SgExperimentStates.ProcessedDataClicked:
            print('You clicked the PROCESSED data:',
                  self.expContainer.selected_data_info.md_uri)
        if action.state == SgExperimentStates.EditInfoClicked:
            self.infoComponent.get_widget().setVisible(True)
        if action.state == SgExperimentStates.TagClicked:
            self.tagComponent.get_widget().setVisible(True)
        if action.state == SgExperimentStates.ExperimentLoaded:
            self.infoContainer.md_uri = self.expContainer.experiment_uri
            self.infoContainer.experiment = self.expContainer.experiment
            self.infoContainer.emit(SgMetadataExperimentStates.Loaded)
        if action.state == SgExperimentStates.TagsSaved or \
                action.state == SgExperimentStates.DataTagged:
            self.tagComponent.get_widget().setVisible(False)
            msgBox = QMessageBox()
            msgBox.setText("Tags saved")
            msgBox.exec()
            self.tableComponent.datasetClicked('data')
            return
        if action.state == SgExperimentStates.ImportClicked:
            self.importComponent.get_widget().setVisible(True)

    def get_widget(self):
        return self.widget


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    if len(sys.argv) != 2:
        print("Error: You need to specify the Experiment dir path")
        exit(1)

    experiment_dir = sys.argv[1]
    experiment_uri = os.path.join(experiment_dir, 'experiment.md.json')


    # Create and show the component
    dir_path = os.path.dirname(os.path.realpath(__file__))
    #dir_path_parent = os.path.abspath(os.path.join(dir_path, os.pardir))
    #ConfigAccess(os.path.join(dir_path_parent, 'config.json'))
    #FormatsAccess(ConfigAccess.instance().get('formats')['file'])

    component = SgExperimentApp(experiment_uri)

    rec = QApplication.desktop().screenGeometry()
    component.get_widget().resize(int(rec.width() / 2), int(rec.height() / 2))
    component.get_widget().show()

    # Run the main Qt loop
    stylesheet_path = os.path.join(dir_path, 'theme', 'dark', 'stylesheet.css')
    app.setStyleSheet("file:///" + stylesheet_path)
    icon_path = os.path.join(dir_path, "theme", "dark", "icon.png")
    app.setWindowIcon(QIcon(icon_path))
    sys.exit(app.exec_())
