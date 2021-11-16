import os
import sys

import qtpy.QtCore
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QApplication

from scixtracergui.app import SciXtracerApp

from scixtracer.config import ConfigAccess
from scixtracergui.widgets import SgThemeAccess


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    # connect to the configurations databases
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path_parent = os.path.abspath(os.path.join(dir_path, os.pardir))
    ConfigAccess(os.path.join(dir_path_parent, 'config.json'))
    SgThemeAccess(os.path.join(dir_path, 'theme', 'napari'))
    #FormatsAccess(ConfigAccess.instance().get('formats')['file'])

    # Create and show the component
    dir_path = os.path.dirname(os.path.realpath(__file__))
    component = SciXtracerApp(bar_position='right')

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
    icon_path = os.path.join(dir_path, "theme", "napari", "logo.png")
    app.setWindowIcon(QIcon(icon_path))
    sys.exit(app.exec_())