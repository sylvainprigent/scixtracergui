import qtpy.QtCore
from qtpy.QtWidgets import (QWidget, QLabel, QVBoxLayout, QScrollArea,
                            QTableWidget, QTableWidgetItem,
                            QAbstractItemView, QGridLayout, QHBoxLayout,
                            QToolButton, QSplitter, QLineEdit, QPushButton,
                            QTextEdit, QMessageBox, QFileDialog)

from scixtracergui.framework import SgComponent, SgAction
from scixtracergui.widgets import SgButton
from scixtracergui.browser.states import SgBrowserStates
from scixtracergui.browser.containers import SgBrowserContainer
from scixtracergui.browser.models import SgBrowserModel


class SgBrowserComponent(SgComponent):
    def __init__(self, container: SgBrowserContainer):
        super().__init__()
        self._object_name = 'SgBrowserComponent'
        self.container = container
        self.container.register(self)  

        self.browserModel = SgBrowserModel(self.container, True)
        self.toolBarComponent = SgBrowserToolBarComponent(self.container)
        self.shortCutComponent = SgBrowserShortCutsComponent(self.container)
        self.tableComponent = SgBrowserTableComponent(self.container)

        self.widget = QWidget()
        self.widget.setObjectName("SgSideBar")
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.widget.setLayout(layout)

        splitter = QSplitter()
        splitter.addWidget(self.shortCutComponent.get_widget())
        splitter.addWidget(self.tableComponent.get_widget())

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        layout.addWidget(self.toolBarComponent.get_widget())
        layout.addWidget(splitter)

    def update(self, action: SgAction):
        pass 

    def get_widget(self): 
        return self.widget  


class SgBrowserToolBarComponent(SgComponent):
    def __init__(self, container: SgBrowserContainer):
        super().__init__()
        self._object_name = 'SgBrowserToolBarComponent'
        self.container = container
        self.container.register(self)

        # build widget
        self.widget = QWidget()
        self.widget.setObjectName("SgToolBar")
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        layout = QHBoxLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(7,0,7,0)
        self.widget.setLayout(layout)

        # previous
        previousButton = QToolButton()
        previousButton.setObjectName("SgBrowserToolBarPreviousButton")
        previousButton.setToolTip(self.widget.tr("Previous"))
        previousButton.released.connect(self.previousButtonClicked)
        layout.addWidget(previousButton, 0, qtpy.QtCore.Qt.AlignLeft)

        # next
        nextButton = QToolButton()
        nextButton.setObjectName("SgBrowserToolBarNextButton")
        nextButton.setToolTip(self.widget.tr("Next"))
        nextButton.released.connect(self.nextButtonClicked)
        layout.addWidget(nextButton, 0, qtpy.QtCore.Qt.AlignLeft)

        # up
        upButton = QToolButton()
        upButton.setObjectName("SgExperimentToolBarUpButton")
        upButton.setToolTip(self.widget.tr("Tags"))
        upButton.released.connect(self.upButtonClicked)
        layout.addWidget(upButton, 0, qtpy.QtCore.Qt.AlignLeft)

        # up
        refreshButton = QToolButton()
        refreshButton.setObjectName("SgExperimentToolBarRefreshButton")
        refreshButton.setToolTip(self.widget.tr("Tags"))
        refreshButton.released.connect(self.refreshButtonClicked)
        layout.addWidget(refreshButton, 0, qtpy.QtCore.Qt.AlignLeft)

        # data selector
        self.pathLineEdit = QLineEdit(self.widget)
        self.pathLineEdit.returnPressed.connect(self.pathEditReturnPressed)
        layout.addWidget(self.pathLineEdit, 1)

        # bookmark
        bookmarkButton = QToolButton()
        bookmarkButton.setObjectName("SgExperimentToolBarBookmarkButton")
        bookmarkButton.setToolTip(self.widget.tr("Bookmark"))
        bookmarkButton.released.connect(self.bookmarkButtonClicked)
        layout.addWidget(bookmarkButton, 0, qtpy.QtCore.Qt.AlignLeft)

    def update(self, action: SgAction):
        if action.state == SgBrowserStates.FilesInfoLoaded:
            self.pathLineEdit.setText(self.container.currentPath)

    def previousButtonClicked(self):
        self.container.emit(SgBrowserStates.PreviousClicked)

    def nextButtonClicked(self):
        self.container.emit(SgBrowserStates.NextClicked)

    def upButtonClicked(self):
        self.container.emit(SgBrowserStates.UpClicked)

    def pathEditReturnPressed(self):
        self.container.setCurrentPath(self.pathLineEdit.text())
        self.container.emit(SgBrowserStates.DirectoryModified)

    def refreshButtonClicked(self):
        self.container.setCurrentPath(self.pathLineEdit.text())
        self.container.emit(SgBrowserStates.RefreshClicked)

    def bookmarkButtonClicked(self):
        msgBox = QMessageBox()
        msgBox.setText("Want to bookmark this directory ?")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)
        ret = msgBox.exec_()
        if ret:
            self.container.emit(SgBrowserStates.BookmarkClicked)

    def get_widget(self): 
        return self.widget            
       

class SgBrowserShortCutsComponent(SgComponent):
    def __init__(self, container: SgBrowserContainer):
        super(SgBrowserShortCutsComponent, self).__init__()
        self._object_name = 'SgBrowserPreviewComponent'
        self.container = container
        self.container.register(self)

        self.widget = QWidget()
        
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)
        self.widget.setLayout(mainLayout)

        self.wwidget = QWidget()
        mainLayout.addWidget(self.wwidget)
        self.wwidget.setObjectName("SgLeftBar")
        self.wwidget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)

        layout = QVBoxLayout()
        self.wwidget.setLayout(layout)

        addExpermentbutton = QPushButton(self.wwidget.tr("New Experiment"))
        addExpermentbutton.setObjectName("SgBrowserShortCutsNewButton")
        addExpermentbutton.released.connect(self.newExperimentClicked)
        layout.addWidget(addExpermentbutton, 0, qtpy.QtCore.Qt.AlignTop)

        separatorLabel = QLabel(self.wwidget.tr("Bookmarks"), self.wwidget)
        layout.addWidget(separatorLabel, 0, qtpy.QtCore.Qt.AlignTop)
        separatorLabel.setObjectName("SgBrowserShortCutsTitle")

        bookmarkWidget = QWidget(self.wwidget)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        bookmarkWidget.setLayout(self.layout)

        layout.addWidget(bookmarkWidget, 0, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(QWidget(), 1, qtpy.QtCore.Qt.AlignTop)

    def reloadBookmarks(self):

        # free layout
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().deleteLater()

        # load
        for entry in self.container.bookmarks.bookmarks["bookmarks"]:

            button = SgButton(entry['name'], self.widget)
            button.setObjectName("SgBrowserShortCutsButton")
            button.content = entry['url']
            button.setCursor(qtpy.QtCore.Qt.PointingHandCursor)
            button.clickedContent.connect(self.buttonClicked)
            self.layout.insertWidget(self.layout.count()-1, button, 0,
                                     qtpy.QtCore.Qt.AlignTop)

    def update(self, action: SgAction):
        if action.state == SgBrowserStates.BookmarksModified:
            self.reloadBookmarks()

    def newExperimentClicked(self):
        self.container.emit(SgBrowserStates.NewExperimentClicked)

    def buttonClicked(self, path: str):
        self.container.bookmarkPath = path
        self.container.emit(SgBrowserStates.BookmarkOpenClicked)

    def get_widget(self): 
        return self.widget


class SgBrowserTableComponent(SgComponent):
    def __init__(self, container: SgBrowserContainer):
        super(SgBrowserTableComponent, self).__init__()
        self._object_name = 'SgBrowserTableComponent'
        self.container = container
        self.container.register(self)
        self.buildWidget()

    def buildWidget(self):

        self.widget = QWidget()
        self.widget.setObjectName("SgWidget")

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.widget.setLayout(layout)

        self.tableWidget = QTableWidget()
        layout.addWidget(self.tableWidget)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.cellDoubleClicked.connect(self.cellDoubleClicked)
        self.tableWidget.cellClicked.connect(self.cellClicked)

        labels = ['', 'Name', 'Date', 'Type']
        self.tableWidget.setHorizontalHeaderLabels(labels)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)

    def update(self, action : SgAction):
        if action.state == SgBrowserStates.FilesInfoLoaded:
            i = -1
            self.tableWidget.setRowCount(len(self.container.files))
            for fileInfo in self.container.files:
                i += 1
                # icon depends on type
                iconLabel = QLabel(self.tableWidget)
                if fileInfo.type == "dir":
                    iconLabel.setObjectName("SgBrowserDirIcon")
                elif fileInfo.type == "run":
                    iconLabel.setObjectName("SgBrowserRunIcon")
                elif fileInfo.type == "experiment":
                    iconLabel.setObjectName("SgBrowserExperimentIcon")
                elif fileInfo.type == "rawdataset":
                    iconLabel.setObjectName("SgBrowserRawDatSetIcon")
                elif fileInfo.type == "processeddataset":
                    iconLabel.setObjectName("SgBrowserProcessedDataSetIcon")
                elif fileInfo.type == "rawdata":
                    iconLabel.setObjectName("SgBrowserRawDatIcon")
                elif fileInfo.type == "processeddata":
                    iconLabel.setObjectName("SgBrowserProcessedDataIcon")

                # icon
                self.tableWidget.setCellWidget(i, 0, iconLabel)
                # name
                self.tableWidget.setItem(i, 1, QTableWidgetItem(fileInfo.name))
                # date
                self.tableWidget.setItem(i, 2, QTableWidgetItem(fileInfo.date))
                # type
                self.tableWidget.setItem(i, 3, QTableWidgetItem(fileInfo.type))
            self.container.emit(SgBrowserStates.TableLoaded)
            
    def cellDoubleClicked(self, row: int, col: int):
        self.container.doubleClickedRow = row
        self.container.emit(SgBrowserStates.ItemDoubleClicked)
        self.highlightLine(row)

    def cellClicked(self, row: int, col: int):
        self.container.clickedRow = row
        self.container.emit(SgBrowserStates.ItemClicked)
        self.highlightLine(row)

    def highlightLine(self, row: int):
        for col in range(4):
            if self.tableWidget.item(row, col):
                self.tableWidget.item(row, col).setSelected(True)    

    def get_widget(self): 
        return self.widget   
