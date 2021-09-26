import qtpy
from qtpy.QtWidgets import (QWidget, QVBoxLayout, QMessageBox, QTabWidget)

from scixtracergui.experiment.containers import (SgExperimentContainer)
from scixtracergui.experiment.states import (SgExperimentStates)
from scixtracergui.framework import SgComponent, SgAction

from scixtracergui.metadata.containers import SgMetadataExperimentContainer
from scixtracergui.metadata.models import SgMetadataExperimentModel
from scixtracergui.metadata.components import SgMetadataExperimentComponent
from scixtracergui.metadata.states import SgMetadataExperimentStates

from .components import (SgExperimentToolbarComponent,
                         SgExperimentTableComponent,
                         SgExperimentImportComponent,
                         SgExperimentTagComponent
                         )
from .models import SgExperimentModel


class SgExperimentComponent(SgComponent):
    def __init__(self):
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
        self.infoContainer.register(self)

        # create the widget
        self.widget = QWidget()
        self.widget.setObjectName('SgWidget')
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.widget.setLayout(layout)

        layout.addWidget(self.toolbarComponent.get_widget())
        layout.addWidget(self.tableComponent.get_widget())
        layout.addWidget(self.infoComponent.get_widget())
        layout.addWidget(self.importComponent.get_widget())
        layout.addWidget(self.tagComponent.get_widget())

        # widget parenting
        self.infoComponent.get_widget().setVisible(False)
        self.importComponent.get_widget().setVisible(False)
        self.tagComponent.get_widget().setVisible(False)

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
            self.toolbarComponent.get_widget().setVisible(False)
            self.tableComponent.get_widget().setVisible(False)
        if action.state == SgExperimentStates.TagClicked:
            self.tagComponent.get_widget().setVisible(True)
            self.toolbarComponent.get_widget().setVisible(False)
            self.tableComponent.get_widget().setVisible(False)
        if action.state == SgExperimentStates.ExperimentLoaded:
            self.infoContainer.md_uri = self.expContainer.experiment_uri
            self.infoContainer.experiment = self.expContainer.experiment
            self.infoContainer.emit(SgMetadataExperimentStates.Loaded)
        if action.state == SgExperimentStates.TagsSaved or \
                action.state == SgExperimentStates.DataTagged:
            self.tagComponent.get_widget().setVisible(False)
            self.toolbarComponent.get_widget().setVisible(True)
            self.tableComponent.get_widget().setVisible(True)
            msgBox = QMessageBox()
            msgBox.setText("Tags saved")
            msgBox.exec()
            self.tableComponent.datasetClicked('data')
            return
        if action.state == SgExperimentStates.ImportClicked:
            self.importComponent.get_widget().setVisible(True)
            self.toolbarComponent.get_widget().setVisible(False)
            self.tableComponent.get_widget().setVisible(False)
            return
        if action.state == SgExperimentStates.DataImported:
            self.importComponent.get_widget().setVisible(False)
            msgBox = QMessageBox()
            msgBox.setText("Data imported")
            msgBox.exec()
            self.tableComponent.datasetClicked('data')
            self.toolbarComponent.get_widget().setVisible(True)
            self.tableComponent.get_widget().setVisible(True)
            return
        if action.state == SgMetadataExperimentStates.Saved:
            self.infoComponent.get_widget().setVisible(False)
            self.toolbarComponent.get_widget().setVisible(True)
            self.tableComponent.get_widget().setVisible(True)
        if action.state == SgExperimentStates.CancelImport:
            self.importComponent.get_widget().setVisible(False)
            self.toolbarComponent.get_widget().setVisible(True)
            self.tableComponent.get_widget().setVisible(True)
        if action.state == SgExperimentStates.CancelTag:
            self.tagComponent.get_widget().setVisible(False)
            self.toolbarComponent.get_widget().setVisible(True)
            self.tableComponent.get_widget().setVisible(True)

    def get_widget(self):
        return self.widget

    def load_experiment(self, experiment_uri):
        self.expContainer.experiment_uri = experiment_uri
        self.expContainer.emit(SgExperimentStates.ExperimentLoad)
