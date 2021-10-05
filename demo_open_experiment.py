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

from scixtracergui.experiment.experiment import SgExperimentComponent

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
    component = SgExperimentComponent()
    component.load_experiment(experiment_uri)

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
    stylesheet_path = os.path.join(dir_path, 'theme', 'dark', 'stylesheet.css')
    app.setStyleSheet("file:///" + stylesheet_path)
    icon_path = os.path.join(dir_path, "theme", "dark", "icon.png")
    app.setWindowIcon(QIcon(icon_path))
    sys.exit(app.exec_())
