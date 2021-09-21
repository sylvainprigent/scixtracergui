import sys
import os

import qtpy.QtCore
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (QApplication, QWidget, QVBoxLayout, QMessageBox)

from scixtracergui.framework import SgAction, SgComponent

from scixtracergui.experiment.states import SgExperimentCreateStates
from scixtracergui.experiment.containers import SgExperimentCreateContainer
from scixtracergui.experiment.components import SgExperimentCreateComponent
from scixtracergui.experiment.models import SgExperimentCreateModel


class SgCreateExperimentApp(SgComponent):
    def __init__(self):
        super().__init__()

        # container
        self.expContainer = SgExperimentCreateContainer()

        # components
        self.createComponent = SgExperimentCreateComponent(self.expContainer)

        # models
        self.experimentModel = SgExperimentCreateModel(self.expContainer)

        # connections
        self.expContainer.register(self)

        # create the widget
        self.widget = QWidget()
        self.widget.setObjectName('SciXtracer create experiment demo')
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.widget.setLayout(layout)

        layout.addWidget(self.createComponent.get_widget())

    def update(self, action: SgAction):
        if action.state == SgExperimentCreateStates.ExperimentCreated:
            msgBox = QMessageBox()
            msgBox.setText("Experiment has been created")
            msgBox.exec()

    def get_widget(self):
        return self.widget


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the component
    dir_path = os.path.dirname(os.path.realpath(__file__))

    component = SgCreateExperimentApp()

    rec = QApplication.desktop().screenGeometry()
    component.get_widget().resize(int(rec.width() / 2), int(rec.height() / 2))
    component.get_widget().show()

    # Run the main Qt loop
    stylesheet_path = os.path.join(dir_path, 'theme', 'dark', 'stylesheet.css')
    app.setStyleSheet("file:///" + stylesheet_path)
    icon_path = os.path.join(dir_path, "theme", "dark", "icon.png")
    app.setWindowIcon(QIcon(icon_path))
    sys.exit(app.exec_())
