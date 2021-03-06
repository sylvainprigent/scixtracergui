import sys
import os

import qtpy.QtCore
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (QApplication, QWidget, QVBoxLayout, QFileDialog,
                            QLabel, QTabWidget, QHBoxLayout, QMessageBox)

from scixtracergui.framework import SgAction, SgComponent

from scixtracergui.experiment.states import (SgExperimentHomeStates,
                                             SgExperimentCreateStates,
                                             SgExperimentStates)
from scixtracergui.experiment.containers import (SgExperimentHomeContainer,
                                                 SgExperimentCreateContainer)
from scixtracergui.experiment.components import (SgExperimentHomeComponent,
                                                 SgExperimentCreateComponent)
from scixtracergui.experiment.experiment import SgExperimentComponent
from scixtracergui.experiment.models import SgExperimentCreateModel


class SgExperimentApp(SgComponent):
    def __init__(self):
        super().__init__()

        # container
        self.expHomeContainer = SgExperimentHomeContainer()
        self.expCreateContainer = SgExperimentCreateContainer()
        
        # components
        self.homeComponent = SgExperimentHomeComponent(self.expHomeContainer)
        self.experimentComponent = SgExperimentComponent()
        self.createComponent = SgExperimentCreateComponent(
            self.expCreateContainer)

        # models
        self.experimentModel = SgExperimentCreateModel(self.expCreateContainer)

        # connections
        self.expHomeContainer.register(self)
        self.expCreateContainer.register(self)
        self.experimentComponent.expContainer.register(self)

        # create the widget
        self.widget = QWidget()
        self.widget.setObjectName('SgWidget')
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.widget.setLayout(layout)

        self.tabWidget = QTabWidget()
        layout.addWidget(self.createComponent.get_widget())
        layout.addWidget(self.homeComponent.get_widget())
        layout.addWidget(self.experimentComponent.get_widget())
        self.createComponent.get_widget().setVisible(False)
        self.experimentComponent.get_widget().setVisible(False)

    def update(self, action: SgAction):
        if action.state == SgExperimentStates.ViewDataClicked:
            print('You double clicked:',
                  self.experimentComponent.expContainer.selected_data_info.md_uri)
        if action.state == SgExperimentStates.ViewRawMetaDataClicked:
            print('You clicked the RAW data:',
                  self.experimentComponent.expContainer.selected_data_info.md_uri)
        if action.state == SgExperimentStates.ViewProcessedMetaDataClicked:
            print('You clicked the PROCESSED data:',
                  self.experimentComponent.expContainer.selected_data_info.md_uri)
        if action.state == SgExperimentHomeStates.NewClicked:
            self.createComponent.get_widget().setVisible(True)
            self.homeComponent.get_widget().setVisible(False)
        if action.state == SgExperimentHomeStates.OpenClicked:
            dir_ = QFileDialog.getExistingDirectory(
                    self.widget,
                    "Open an Experiment folder",
                    os.path.expanduser("~"),
                    QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
                   )
            self.experimentComponent.load_experiment(
                os.path.join(dir_, 'experiment.md.json'))
            self.homeComponent.get_widget().setVisible(False)
            self.experimentComponent.get_widget().setVisible(True)
        if action.state == SgExperimentCreateStates.ExperimentCreated:
            self.createComponent.get_widget().setVisible(False)
            self.experimentComponent.get_widget().setVisible(True)
        if action.state == SgExperimentCreateStates.CancelCreateClicked:
            self.homeComponent.get_widget().setVisible(True)
            self.createComponent.get_widget().setVisible(False)
            self.experimentComponent.get_widget().setVisible(False)
        if action.state == SgExperimentCreateStates.ExperimentCreationError:
            msgBox = QMessageBox()
            msgBox.setText(self.expCreateContainer.errorMessage)
            msgBox.exec()
        if action.state == SgExperimentStates.HomeClicked:
            self.homeComponent.get_widget().setVisible(True)
            self.createComponent.get_widget().setVisible(False)
            self.experimentComponent.get_widget().setVisible(False)

    def get_widget(self):
        return self.widget


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the component
    dir_path = os.path.dirname(os.path.realpath(__file__))
    component = SgExperimentApp()

    rec = app.primaryScreen().size()
    component.get_widget().resize(int(3*rec.width() / 4), int(3*rec.height() / 4))

    component.get_widget().setGeometry(
        qtpy.QtWidgets.QStyle.alignedRect(
            qtpy.QtCore.Qt.LeftToRight,
            qtpy.QtCore.Qt.AlignCenter,
            component.get_widget().size(),
            qtpy.QtGui.QGuiApplication.primaryScreen().availableGeometry(),
        ),
    )
    component.get_widget().show()

    # Run the main Qt loop
    stylesheet_path = os.path.join(dir_path, 'theme', 'napari', 'stylesheet.css')
    app.setStyleSheet("file:///" + stylesheet_path)
    icon_path = os.path.join(dir_path, "theme", "napari", "icon.png")
    app.setWindowIcon(QIcon(icon_path))
    sys.exit(app.exec_())
