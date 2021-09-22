import sys
import os

import qtpy.QtCore
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (QApplication, QWidget, QVBoxLayout, QFileDialog,
                            QLabel, QTabWidget, QHBoxLayout, QMessageBox)

from scixtracergui.framework import SgAction, SgComponent

from scixtracergui.experiment.states import (SgExperimentHomeStates,
                                             SgExperimentCreateStates)
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
        if action.state == SgExperimentCreateStates.ExperimentCreationError:
            msgBox = QMessageBox()
            msgBox.setText(self.expCreateContainer.errorMessage)
            msgBox.exec()

    def get_widget(self):
        return self.widget


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the component
    dir_path = os.path.dirname(os.path.realpath(__file__))
    component = SgExperimentApp()

    rec = QApplication.desktop().screenGeometry()
    component.get_widget().resize(int(rec.width() / 2), int(rec.height() / 2))
    component.get_widget().show()

    # Run the main Qt loop
    stylesheet_path = os.path.join(dir_path, 'theme', 'dark', 'stylesheet.css')
    app.setStyleSheet("file:///" + stylesheet_path)
    icon_path = os.path.join(dir_path, "theme", "dark", "icon.png")
    app.setWindowIcon(QIcon(icon_path))
    sys.exit(app.exec_())
