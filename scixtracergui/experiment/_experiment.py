import qtpy
from qtpy.QtWidgets import (QWidget, QVBoxLayout, QMessageBox, QTabWidget,
                            QLabel)

from scixtracergui.framework import SgComponent, SgAction

from scixtracergui.metadata.containers import (SgMetadataExperimentContainer,
                                               SgRawDataContainer,
                                               SgProcessedDataContainer,
                                               SgRunContainer)
from scixtracergui.metadata.models import (SgMetadataExperimentModel,
                                           SgRawDataModel,
                                           SgProcessedDataModel,
                                           SgRunModel)
from scixtracergui.metadata.components import (SgMetadataExperimentComponent,
                                               SgRawDataComponent,
                                               SgProcessedDataComponent,
                                               SgMetadataRunComponent)
from scixtracergui.metadata.states import (SgMetadataExperimentStates,
                                           SgRawDataStates,
                                           SgProcessedDataStates,
                                           SgRunStates)

from ._components import (SgExperimentToolbarComponent,
                         SgExperimentTableComponent,
                         SgExperimentImportComponent,
                         SgExperimentTagComponent,
                         SgExperimentMetaToolbarComponent
                         )
from ._containers import (SgExperimentContainer)
from ._states import (SgExperimentStates)   
from ._models import SgExperimentModel


class SgExperimentComponent(SgComponent):
    def __init__(self, experiment_uri):
        super().__init__()

        # container
        self.experimentContainer = SgExperimentContainer()
        self.infoContainer = SgMetadataExperimentContainer()
        self.rawDataContainer = SgRawDataContainer()
        self.processedDataContainer = SgProcessedDataContainer()
        self.runContainer = SgRunContainer()

        # components
        self.toolbarComponent = SgExperimentToolbarComponent(self.experimentContainer)
        self.tableComponent = SgExperimentTableComponent(self.experimentContainer)
        self.importComponent = SgExperimentImportComponent(self.experimentContainer)
        self.tagComponent = SgExperimentTagComponent(self.experimentContainer)

        self.metaToolbarComponent = SgExperimentMetaToolbarComponent(self.experimentContainer)
        self.infoComponent = SgMetadataExperimentComponent(self.infoContainer)
        self.rawDataComponent = SgRawDataComponent(self.rawDataContainer)
        self.processedDataComponent = SgProcessedDataComponent(self.processedDataContainer)
        self.runComponent = SgMetadataRunComponent(self.runContainer)

        # models
        self.experimentModel = SgExperimentModel(self.experimentContainer)
        self.infoModel = SgMetadataExperimentModel(self.infoContainer)
        self.rawDataModel = SgRawDataModel(self.rawDataContainer)
        self.processedDataModel = SgProcessedDataModel(self.processedDataContainer)
        self.runModel = SgRunModel(self.runContainer)

        # connections
        self.experimentContainer.register(self)
        self.infoContainer.register(self)
        self.rawDataContainer.register(self)
        self.processedDataContainer.register(self)

        # init
        self.experimentContainer.experiment_uri = experiment_uri
        self.experimentContainer.emit(SgExperimentStates.ExperimentLoad)

        # create the widget
        self.widget = QWidget()
        self.widget.setObjectName('SgWidget')
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self.widget.setLayout(layout)

        self.processedDataWidget = QWidget()
        processedDataLayout = QVBoxLayout()
        title1 = QLabel('Processed data metadata')
        title1.setObjectName('SgLabelFormHeader1')
        processedDataLayout.addWidget(title1)
        processedDataLayout.addWidget(self.processedDataComponent.get_widget())
        title2 = QLabel('Run information')
        title2.setObjectName('SgLabelFormHeader1')
        processedDataLayout.addWidget(title2)
        processedDataLayout.addWidget(self.runComponent.get_widget())
        self.processedDataWidget.setLayout(processedDataLayout)

        layout.addWidget(self.toolbarComponent.get_widget())
        layout.addWidget(self.metaToolbarComponent.get_widget())
        layout.addWidget(self.tableComponent.get_widget())
        layout.addWidget(self.infoComponent.get_widget())
        layout.addWidget(self.importComponent.get_widget())
        layout.addWidget(self.tagComponent.get_widget())
        layout.addWidget(self.rawDataComponent.get_widget())
        layout.addWidget(self.processedDataWidget)

        # widget parenting
        self.metaToolbarComponent.get_widget().setVisible(False)
        self.infoComponent.get_widget().setVisible(False)
        self.importComponent.get_widget().setVisible(False)
        self.tagComponent.get_widget().setVisible(False)
        self.rawDataComponent.get_widget().setVisible(False)
        self.processedDataWidget.setVisible(False)

    def update(self, action: SgAction):
        if action.state == SgExperimentStates.EditInfoClicked:
            self.metaToolbarComponent.get_widget().setVisible(True)
            self.infoComponent.get_widget().setVisible(True)
            self.toolbarComponent.get_widget().setVisible(False)
            self.tableComponent.get_widget().setVisible(False)
        if action.state == SgExperimentStates.TagClicked:
            self.metaToolbarComponent.get_widget().setVisible(True)
            self.tagComponent.get_widget().setVisible(True)
            self.toolbarComponent.get_widget().setVisible(False)
            self.tableComponent.get_widget().setVisible(False)
        if action.state == SgExperimentStates.ExperimentLoaded:
            self.infoContainer.md_uri = self.experimentContainer.experiment_uri
            self.infoContainer.experiment = self.experimentContainer.experiment
            self.infoContainer.emit(SgMetadataExperimentStates.Loaded)
        if action.state == SgExperimentStates.TagsSaved or \
                action.state == SgExperimentStates.DataTagged:
            self.metaToolbarComponent.get_widget().setVisible(False)
            self.tagComponent.get_widget().setVisible(False)
            self.toolbarComponent.get_widget().setVisible(True)
            self.tableComponent.get_widget().setVisible(True)
            msgBox = QMessageBox()
            msgBox.setText("Tags saved")
            msgBox.exec()
            self.tableComponent.datasetClicked('data')
            return
        if action.state == SgExperimentStates.ImportClicked:
            self.metaToolbarComponent.get_widget().setVisible(True)
            self.importComponent.get_widget().setVisible(True)
            self.toolbarComponent.get_widget().setVisible(False)
            self.tableComponent.get_widget().setVisible(False)
            return
        if action.state == SgExperimentStates.DataImported:
            self.metaToolbarComponent.get_widget().setVisible(False)
            self.importComponent.get_widget().setVisible(False)
            msgBox = QMessageBox()
            msgBox.setText("Data imported")
            msgBox.exec()
            self.tableComponent.datasetClicked('data')
            self.toolbarComponent.get_widget().setVisible(True)
            self.tableComponent.get_widget().setVisible(True)
            return
        if action.state == SgMetadataExperimentStates.Saved or \
                action.state == SgMetadataExperimentStates.CancelClicked:
            self.metaToolbarComponent.get_widget().setVisible(False)
            self.infoComponent.get_widget().setVisible(False)
            self.toolbarComponent.get_widget().setVisible(True)
            self.tableComponent.get_widget().setVisible(True)
        if action.state == SgExperimentStates.CancelTag:
            self.metaToolbarComponent.get_widget().setVisible(False)
            self.tagComponent.get_widget().setVisible(False)
            self.toolbarComponent.get_widget().setVisible(True)
            self.tableComponent.get_widget().setVisible(True)
        if action.state == SgExperimentStates.MainPageClicked:
            self.metaToolbarComponent.get_widget().setVisible(False)
            self.tagComponent.get_widget().setVisible(False)
            self.importComponent.get_widget().setVisible(False)
            self.infoComponent.get_widget().setVisible(False)
            self.rawDataComponent.get_widget().setVisible(False)
            self.processedDataWidget.setVisible(False)
            self.toolbarComponent.get_widget().setVisible(True)
            self.tableComponent.get_widget().setVisible(True)
        if action.state == SgExperimentStates.ViewRawMetaDataClicked:
            self.rawDataContainer.md_uri = self.experimentContainer.selected_data_info.md_uri
            self.rawDataContainer.emit(SgRawDataStates.URIChanged)
            self.metaToolbarComponent.get_widget().setVisible(True)
            self.rawDataComponent.get_widget().setVisible(True)
            self.toolbarComponent.get_widget().setVisible(False)
            self.tableComponent.get_widget().setVisible(False)
        if action.state == SgRawDataStates.Saved:
            self.metaToolbarComponent.get_widget().setVisible(False)
            self.rawDataComponent.get_widget().setVisible(False)
            self.toolbarComponent.get_widget().setVisible(True)
            self.tableComponent.get_widget().setVisible(True)
            self.tableComponent.drawRawDataset()
        if action.state == SgExperimentStates.ViewProcessedMetaDataClicked:
            self.processedDataContainer.md_uri = self.experimentContainer.selected_data_info.md_uri
            self.processedDataContainer.emit(SgProcessedDataStates.URIChanged)
            self.metaToolbarComponent.get_widget().setVisible(True)
            self.processedDataWidget.setVisible(True)
            self.toolbarComponent.get_widget().setVisible(False)
            self.tableComponent.get_widget().setVisible(False)
        if action.state == SgProcessedDataStates.Loaded:
            self.runContainer.md_uri = self.processedDataContainer.processeddata.run.md_uri
            self.runContainer.emit(SgRunStates.URIChanged)

    def get_widget(self):
        return self.widget

    def load_experiment(self, experiment_uri):
        self.experimentContainer.experiment_uri = experiment_uri
        self.experimentContainer.emit(SgExperimentStates.ExperimentLoad)
