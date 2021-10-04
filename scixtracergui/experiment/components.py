import qtpy
from qtpy.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QToolButton, QPushButton, QLabel, QLineEdit,
                            QCheckBox, QComboBox, QFileDialog, QProgressBar,
                            QTableWidget, QTableWidgetItem, QSpinBox,
                            QScrollArea, QTabWidget, QAbstractItemView,
                            QHeaderView)

import scixtracer as sx
from scixtracergui.framework import SgComponent, SgAction
from scixtracergui.widgets import SgTagWidget, SgButton
from scixtracergui.experiment.containers import (SgExperimentCreateContainer,
                                                 SgExperimentContainer,
                                                 SgExperimentHomeContainer)
from scixtracergui.experiment.states import (SgExperimentCreateStates,
                                             SgExperimentStates,
                                             SgExperimentHomeStates)


class SgExperimentHomeComponent(SgComponent):
    def __init__(self, container: SgExperimentHomeContainer):
        super().__init__()
        self._object_name = 'SgExperimentCreateComponent'
        self.container = container
        self.container.register(self)

        self.widget = QWidget()
        self.widget.setObjectName("SgWidget")
        layout = QVBoxLayout()
        self.widget.setLayout(layout)

        newButton = QPushButton("New experiment")
        newButton.setObjectName('btnDefault')
        newButton.released.connect(self.newClicked)
        openButton = QPushButton("Open experiment")
        openButton.setObjectName('btnDefault')
        openButton.released.connect(self.openClicked)

        layout.addWidget(QWidget(), 1)
        layout.addWidget(newButton, 0)
        layout.addWidget(openButton, 0)
        layout.addWidget(QWidget(), 1)

    def openClicked(self):
        self.container.emit(SgExperimentHomeStates.OpenClicked)

    def newClicked(self):
        self.container.emit(SgExperimentHomeStates.NewClicked)

    def update(self, action):
        pass

    def get_widget(self):
        return self.widget


class SgExperimentCreateComponent(SgComponent):
    def __init__(self, container: SgExperimentCreateContainer,
                 default_destination: str = ""):
        super().__init__()
        self._object_name = 'SgExperimentCreateComponent'
        self.container = container
        self.container.register(self)

        self.widget = QWidget()
        self.widget.setObjectName("SgWidget")
        layout = QGridLayout()
        self.widget.setLayout(layout)

        # title
        title = QLabel(self.widget.tr("Create experiment"))
        title.setObjectName("SgLabelFormHeader1")
        title.setMaximumHeight(50)

        destinationLabel = QLabel(self.widget.tr("Destination"))
        destinationLabel.setObjectName("SgLabel")
        self.destinationEdit = QLineEdit()
        self.destinationEdit.setText(default_destination)
        browseButton = QPushButton(self.widget.tr("..."))
        browseButton.setObjectName("SgBrowseButton")
        browseButton.released.connect(self.browseButtonClicked)

        nameLabel = QLabel(self.widget.tr("Experiment name"))
        nameLabel.setObjectName("SgLabel")
        self.nameEdit = QLineEdit()

        authorLabel = QLabel(self.widget.tr("Author"))
        authorLabel.setObjectName("SgLabel")
        self.authorEdit = QLineEdit()

        createButton = QPushButton(self.widget.tr("Create"))
        createButton.setObjectName("btnPrimary")
        createButton.released.connect(self.createButtonClicked)

        cancelButton = QPushButton(self.widget.tr("Cancel"))
        cancelButton.setObjectName("btnDefault")
        cancelButton.released.connect(self.cancelButtonClicked)

        layout.addWidget(title, 0, 0, 1, 3)
        layout.addWidget(destinationLabel, 1, 0)
        layout.addWidget(self.destinationEdit, 1, 1)
        layout.addWidget(browseButton, 1, 2)
        layout.addWidget(nameLabel, 2, 0)
        layout.addWidget(self.nameEdit, 2, 1, 1, 2)
        layout.addWidget(authorLabel, 3, 0)
        layout.addWidget(self.authorEdit, 3, 1, 1, 2)
        layout.addWidget(cancelButton, 4, 1, 1, 1, qtpy.QtCore.Qt.AlignRight)
        layout.addWidget(createButton, 4, 2, 1, 1, qtpy.QtCore.Qt.AlignRight)
        layout.addWidget(QWidget(), 5, 0, 1, 1, qtpy.QtCore.Qt.AlignTop)

    def browseButtonClicked(self):
        directory = QFileDialog.getExistingDirectory(
            self.widget, self.widget.tr("Select Directory"),
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.destinationEdit.setText(directory)

    def createButtonClicked(self):
        self.container.experiment_destination_dir = self.destinationEdit.text()
        self.container.experiment_name = self.nameEdit.text()
        self.container.experiment_author = self.authorEdit.text()
        self.container.emit(SgExperimentCreateStates.CreateClicked)

    def cancelButtonClicked(self):
        self.container.emit(SgExperimentCreateStates.CancelCreateClicked)

    def reset(self):
        self.destinationEdit.setText('')
        self.nameEdit.setText('')
        self.authorEdit.setText('')

    def setDestination(self, path: str):
        self.destinationEdit.setText(path)

    def update(self, action: SgAction):
        pass

    def get_widget(self):
        return self.widget


class SgExperimentToolbarComponent(SgComponent):
    def __init__(self, container: SgExperimentContainer):
        super().__init__()
        self._object_name = 'SgExperimentToolbarComponent'
        self.container = container
        self.container.register(self)

        # init the widget
        self.widget = QWidget()
        self.widget.setObjectName('SgToolBar')
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        layout = QHBoxLayout()
        layout.setSpacing(1)
        self.widget.setLayout(layout)

        # home
        homeButton = QToolButton()
        homeButton.setObjectName("SgExperimentToolBarHomeButton")
        homeButton.setToolTip(self.widget.tr("Home"))
        homeButton.released.connect(self.homeButtonClicked)
        layout.addWidget(homeButton, 0, qtpy.QtCore.Qt.AlignLeft)

        # info
        infoButton = QToolButton()
        infoButton.setObjectName("SgExperimentToolbarInfoButton")
        infoButton.setToolTip(self.widget.tr("Experiment information"))
        infoButton.released.connect(self.infoButtonClicked)
        layout.addWidget(infoButton, 0, qtpy.QtCore.Qt.AlignLeft)

        # datasets
        self.dataset_box = QComboBox()
        self.dataset_box.currentIndexChanged.connect(self.datasetBoxChanged)
        layout.addWidget(self.dataset_box, 0, qtpy.QtCore.Qt.AlignLeft)

        # import
        importButton = QToolButton()
        importButton.setObjectName("SgExperimentToolbarImportButton")
        importButton.setToolTip(self.widget.tr("Import data"))
        importButton.released.connect(self.importButtonClicked)
        layout.addWidget(importButton, 0, qtpy.QtCore.Qt.AlignLeft)

        # tags
        tagButton = QToolButton()
        tagButton.setObjectName("SgExperimentToolbarTagButton")
        tagButton.setToolTip(self.widget.tr("Tag data"))
        tagButton.released.connect(self.tagButtonClicked)
        layout.addWidget(tagButton, 0, qtpy.QtCore.Qt.AlignLeft)

        # refresh
        refreshButton = QToolButton()
        refreshButton.setObjectName("SgExperimentToolbarRefreshButton")
        refreshButton.setToolTip(self.widget.tr("Refresh"))
        refreshButton.released.connect(self.refreshButtonClicked)
        layout.addWidget(refreshButton, 0, qtpy.QtCore.Qt.AlignLeft)

        layout.addWidget(QWidget(), 1, qtpy.QtCore.Qt.AlignLeft)

    def homeButtonClicked(self):
        self.container.emit(SgExperimentStates.HomeClicked)

    def infoButtonClicked(self):
        self.container.emit(SgExperimentStates.EditInfoClicked)

    def datasetBoxChanged(self):
        self.container.dataset_name = self.dataset_box.currentText()
        self.container.emit(SgExperimentStates.DatasetChanged)

    def importButtonClicked(self):
        self.container.emit(SgExperimentStates.ImportClicked)

    def tagButtonClicked(self):
        self.container.emit(SgExperimentStates.TagClicked)

    def refreshButtonClicked(self):
        self.container.emit(SgExperimentStates.RefreshClicked)

    def update(self, action: SgAction):
        if action.state == SgExperimentStates.ExperimentLoaded:
            # update the list of datasets in the combobox
            current_text = self.dataset_box.currentText
            self.dataset_box.clear()
            self.dataset_box.addItem('data')
            self.dataset_box.currentIndexChanged.disconnect(
                self.datasetBoxChanged)
            for dataset_info in self.container.experiment.processeddatasets:
                self.dataset_box.addItem(dataset_info.name)
                if dataset_info.name == current_text:
                    self.dataset_box.setCurrentText(dataset_info.name)
            self.dataset_box.currentIndexChanged.connect(
                self.datasetBoxChanged)

    def get_widget(self):
        return self.widget


class SgExperimentTableComponent(SgComponent):
    def __init__(self, container: SgExperimentContainer):
        super().__init__()
        self._object_name = 'SgExperimentTableComponent'
        self.container = container
        self.container.register(self)
        self.req = sx.Request()  # this should be moved to model

        self.widget = QWidget()
        self.widget.setObjectName("SgWidget")
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)

        layout = QVBoxLayout()
        layout.setContentsMargins(3, 3, 3, 3)
        self.widget.setLayout(layout)

        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setAlternatingRowColors(True)

        labels = ["", "Name", "Author", "Date"]
        self.tableWidget.setHorizontalHeaderLabels(labels)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidget.verticalHeader().setDefaultSectionSize(36)

        #self.tableWidget.cellClicked.connect(self.cellClicked)
        #self.tableWidget.cellDoubleClicked.connect(self.cellDoubleClicked)

        layout.addWidget(self.tableWidget)

    def update(self, action: SgAction):
        if action.state == SgExperimentStates.DataSetLoaded or \
                action.state == SgExperimentStates.ExperimentLoaded:
            if self.container.dataset_name == "data":
                self.drawRawDataset()
            else:
                self.drawProcessedDataSet()

    def get_widget(self):
        return self.widget

    def drawRawDataset(self):
        # headers
        tags = self.container.experiment.tag_keys
        self.tableWidget.setColumnCount(6 + len(tags))
        labels = ["", "", "Name"]
        for tag in tags:
            labels.append(tag)
        labels.append("Format")
        labels.append("Author")
        labels.append("Date")
        self.tableWidget.setHorizontalHeaderLabels(labels)

        exp_size = self.container.dataset.size()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(exp_size)
        self.tableWidget.verticalHeader().setVisible(False)

        data_list = self.container.dataset.uris

        for i in range(len(data_list)):
            raw_metadata = self.req.get_rawdata(data_list[i].md_uri)

            # view button
            col_idx = 0
            view_btn = SgButton("View")
            view_btn.id = i
            view_btn.setObjectName("btnTablePrimary")
            view_btn.clickedId.connect(self.viewDataClicked)
            self.tableWidget.setCellWidget(i, col_idx, view_btn)

            # metadata button
            col_idx += 1
            edit_btn = SgButton("Metadata")
            edit_btn.id = i
            edit_btn.setObjectName("btnTableDefault")
            edit_btn.clickedId.connect(self.viewMetaDataClicked)
            self.tableWidget.setCellWidget(i, col_idx, edit_btn)

            # name
            col_idx += 1
            self.tableWidget.setItem(i, col_idx, QTableWidgetItem(
                raw_metadata.name))
            # tags
            for tag in tags:
                col_idx += 1
                if tag in raw_metadata.tags:
                    self.tableWidget.setItem(i, col_idx, QTableWidgetItem(
                        raw_metadata.tags[tag]))
            # format
            col_idx += 1
            self.tableWidget.setItem(i, col_idx,
                                     QTableWidgetItem(raw_metadata.format))
            # author
            col_idx += 1
            self.tableWidget.setItem(i, col_idx,
                                     QTableWidgetItem(raw_metadata.author))
            # created date
            col_idx += 1
            self.tableWidget.setItem(i, col_idx,
                                     QTableWidgetItem(raw_metadata.date))

    def drawProcessedDataSet(self):
        # headers
        tags = self.container.experiment.tag_keys
        self.tableWidget.setColumnCount(8 + len(tags))
        labels = ["", "", "Name", "Parent", "Label"]
        for tag in tags:
            labels.append(tag)
        labels.append("Format")
        labels.append("Author")
        labels.append("Date")
        self.tableWidget.setHorizontalHeaderLabels(labels)

        exp_size = self.container.dataset.size()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(exp_size)
        self.tableWidget.verticalHeader().setVisible(False)

        data_list = self.container.dataset.uris

        for i in range(len(data_list)):
            raw_metadata = self.req.get_processeddata(data_list[i].md_uri)
            parent_metadata = self.req.get_parent(raw_metadata)
            origin_metadata = self.req.get_origin(raw_metadata)

            # view button
            col_idx = 0
            view_btn = SgButton("View")
            view_btn.id = i
            view_btn.setObjectName("btnTablePrimary")
            view_btn.clickedId.connect(self.viewDataClicked)
            self.tableWidget.setCellWidget(i, col_idx, view_btn)

            # metadata button
            col_idx += 1
            edit_btn = SgButton("Metadata")
            edit_btn.id = i
            edit_btn.setObjectName("btnTableDefault")
            edit_btn.clickedId.connect(self.viewMetaDataClicked)
            self.tableWidget.setCellWidget(i, col_idx, edit_btn)

            # name
            col_idx += 1
            self.tableWidget.setItem(i, col_idx,
                                     QTableWidgetItem(raw_metadata.name))
            # origin
            col_idx += 1
            self.tableWidget.setItem(i, col_idx,
                                     QTableWidgetItem(parent_metadata.name))
            # label
            col_idx += 1
            self.tableWidget.setItem(i, col_idx, QTableWidgetItem(
                raw_metadata.output['label']))
            # tags
            if origin_metadata:
                # tags
                for tag in tags:
                    col_idx += 1
                    if tag in origin_metadata.tags:
                        self.tableWidget.setItem(i, col_idx, QTableWidgetItem(
                            origin_metadata.tags[tag]))
            else:
                for tag in tags:
                    col_idx += 1
                    self.tableWidget.setItem(i, col_idx, QTableWidgetItem(""))
                    # format
            col_idx += 1
            self.tableWidget.setItem(i, col_idx,
                                     QTableWidgetItem(raw_metadata.format))
            # author
            col_idx += 1
            self.tableWidget.setItem(i, col_idx,
                                     QTableWidgetItem(raw_metadata.author))
            # created date
            col_idx += 1
            self.tableWidget.setItem(i, col_idx,
                                     QTableWidgetItem(raw_metadata.date))

    def datasetClicked(self, name: str):
        self.container.dataset_name = name
        self.container.emit(SgExperimentStates.DatasetChanged)

    def viewDataClicked(self, row: int):
        self.container.selected_data_info = self.container.dataset.uris[row]
        self.container.emit(SgExperimentStates.ViewDataClicked)

    def viewMetaDataClicked(self, row: int):
        self.container.selected_data_info = self.container.dataset.uris[row]
        #self.highlightLine(row)
        if self.container.dataset_name == 'data':
            self.container.emit(SgExperimentStates.ViewRawMetaDataClicked)
        else:
            self.container.emit(SgExperimentStates.ViewProcessedMetaDataClicked)

    def highlightLine(self, row: int):
        for col in range(self.tableWidget.columnCount()):
            if self.tableWidget.item(row, col):
                self.tableWidget.item(row, col).setSelected(True)


class SgExperimentImportComponent(SgComponent):
    def __init__(self, container: SgExperimentContainer):
        super().__init__()
        self._object_name = 'SgExperimentImportComponent'
        self.container = container
        self.container.register(self)

        self.widget = QWidget()
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        self.widget.setObjectName("SgWidget")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(layout)
        tabWidget = QTabWidget()
        layout.addWidget(tabWidget)

        importSingleComponent = SgExperimentImportSingleDataComponent(container)
        tabWidget.addTab(importSingleComponent.get_widget(),
                         self.widget.tr("Single Data"))

        importDirectoryComponent = SgExperimentImportDirectoryDataComponent(container)
        tabWidget.addTab(importDirectoryComponent.get_widget(),
                         self.widget.tr("Multiple Data"))

    def update(self, action: SgAction):
        pass

    def get_widget(self):
        return self.widget


class SgExperimentImportSingleDataComponent(SgComponent):
    def __init__(self, container: SgExperimentContainer):
        super().__init__()
        self._object_name = 'SgExperimentImportSingleDataComponent'
        self.container = container
        self.container.register(self)

        self.widget = QWidget()
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        self.widget.setObjectName("SgWidget")

        layout = QGridLayout()
        self.widget.setLayout(layout)

        # title
        title = QLabel(self.widget.tr("Import single data"))
        title.setObjectName("SgLabelFormHeader1")

        dataLabel = QLabel(self.widget.tr("Data"))
        dataLabel.setObjectName("SgWidget")
        self.dataPath = QLineEdit()
        browseDataButton = QPushButton(self.widget.tr("..."))
        browseDataButton.setObjectName("SgBrowseButton")
        browseDataButton.released.connect(self.browseDataButtonClicked)

        copyDataLabel = QLabel(self.widget.tr("Copy data"))
        copyDataLabel.setObjectName("SgWidget")
        self.copyDataBox = QCheckBox()
        self.copyDataBox.setChecked(True)

        nameLabel = QLabel(self.widget.tr("Name"))
        nameLabel.setObjectName("SgWidget")
        self.nameEdit = QLineEdit()

        formatLabel = QLabel(self.widget.tr("Format"))
        formatLabel.setObjectName("SgWidget")
        self.formatEdit = QLineEdit()

        authorLabel = QLabel(self.widget.tr("Author"))
        authorLabel.setObjectName("SgWidget")
        self.authorEdit = QLineEdit()

        createddateLabel = QLabel(self.widget.tr("Created date"))
        createddateLabel.setObjectName("SgWidget")
        self.createddateEdit = QLineEdit()

        importButton = QPushButton(self.widget.tr("Import"))
        importButton.setObjectName("btnPrimary")
        importButton.released.connect(self.importButtonClicked)

        cancelButton = QPushButton(self.widget.tr("Cancel"))
        cancelButton.setObjectName("btnDefault")
        cancelButton.released.connect(self.cancelButtonClicked)

        layout.addWidget(title, 0, 0, 1, 3)
        layout.addWidget(dataLabel, 1, 0)
        layout.addWidget(self.dataPath, 1, 1)
        layout.addWidget(browseDataButton, 1, 2)
        layout.addWidget(copyDataLabel, 2, 0)
        layout.addWidget(self.copyDataBox, 2, 1, 1, 2)
        layout.addWidget(nameLabel, 3, 0)
        layout.addWidget(self.nameEdit, 3, 1, 1, 2)
        layout.addWidget(formatLabel, 4, 0)
        layout.addWidget(self.formatEdit, 4, 1, 1, 2)
        layout.addWidget(authorLabel, 5, 0)
        layout.addWidget(self.authorEdit, 5, 1, 1, 2)
        layout.addWidget(createddateLabel, 6, 0)
        layout.addWidget(self.createddateEdit, 6, 1, 1, 2)
        layout.addWidget(cancelButton, 7, 1, qtpy.QtCore.Qt.AlignRight)
        layout.addWidget(importButton, 7, 2, qtpy.QtCore.Qt.AlignRight)
        layout.addWidget(QWidget(), 8, 0)

    def update(self, action: SgAction):
        pass

    def cancelButtonClicked(self):
        self.container.emit(SgExperimentStates.CancelImport)

    def importButtonClicked(self):
        self.container.import_info.file_data_path = self.dataPath.text()
        self.container.import_info.file_copy_data = self.copyDataBox.isChecked()
        self.container.import_info.file_name = self.nameEdit.text()
        self.container.import_info.format = self.formatEdit.text()
        self.container.import_info.author = self.authorEdit.text()
        self.container.import_info.created_date = self.createddateEdit.text()
        self.container.emit(SgExperimentStates.NewImportFile)

    def browseDataButtonClicked(self):
        fileName = QFileDialog.getOpenFileName(self.widget,
                                               self.widget.tr("Import file"),
                                               'Data (*.*)')
        self.dataPath.setText(fileName[0])

    def get_widget(self):
        return self.widget


class SgExperimentImportDirectoryDataComponent(SgComponent):
    def __init__(self, container: SgExperimentContainer):
        super().__init__()
        self._object_name = 'SgExperimentImportDirectoryDataComponent'
        self.container = container
        self.container.register(self)

        self.widget = QWidget()
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        self.widget.setObjectName("SgWidget")

        layout = QGridLayout()
        self.widget.setLayout(layout)

        # title
        title = QLabel(self.widget.tr("Import from folder"))
        title.setObjectName("SgLabelFormHeader1")

        dataLabel = QLabel(self.widget.tr("Folder"))
        dataLabel.setObjectName("SgWidget")
        self.dataPath = QLineEdit()
        browseDataButton = QPushButton(self.widget.tr("..."))
        browseDataButton.setObjectName("SgBrowseButton")
        browseDataButton.released.connect(self.browseDataButtonClicked)

        recursiveLabel = QLabel(self.widget.tr("Recursive"))
        recursiveLabel.setObjectName("SgWidget")
        self.recursiveBox = QCheckBox()
        self.recursiveBox.setChecked(True)

        filterLabel = QLabel(self.widget.tr("Filter"))
        filterLabel.setObjectName("SgWidget")
        self.filterComboBox = QComboBox()
        self.filterComboBox.addItem(self.widget.tr('Ends With'))
        self.filterComboBox.addItem(self.widget.tr('Start With'))
        self.filterComboBox.addItem(self.widget.tr('Contains'))
        self.filterEdit = QLineEdit()
        self.filterEdit.setText('.tif')

        copyDataLabel = QLabel(self.widget.tr("Copy data"))
        copyDataLabel.setObjectName("SgWidget")
        self.copyDataBox = QCheckBox()
        self.copyDataBox.setChecked(True)

        formatLabel = QLabel(self.widget.tr("Format"))
        formatLabel.setObjectName("SgWidget")
        self.formatEdit = QLineEdit()

        authorLabel = QLabel(self.widget.tr("Author"))
        authorLabel.setObjectName("SgWidget")
        self.authorEdit = QLineEdit()

        createddateLabel = QLabel(self.widget.tr("Created date"))
        createddateLabel.setObjectName("SgWidget")
        self.createddateEdit = QLineEdit()

        importButton = QPushButton(self.widget.tr("import"))
        importButton.setObjectName("btnPrimary")
        importButton.released.connect(self.importButtonClicked)

        cancelButton = QPushButton(self.widget.tr("Cancel"))
        cancelButton.setObjectName("btnDefault")
        cancelButton.released.connect(self.cancelButtonClicked)

        layout.addWidget(title, 0, 0, 1, 4)
        layout.addWidget(dataLabel, 1, 0)
        layout.addWidget(self.dataPath, 1, 1, 1, 2)
        layout.addWidget(browseDataButton, 1, 3)
        layout.addWidget(recursiveLabel, 2, 0)
        layout.addWidget(self.recursiveBox, 2, 1, 1, 2)
        layout.addWidget(filterLabel, 3, 0)
        layout.addWidget(self.filterComboBox, 3, 1, 1, 1)
        layout.addWidget(self.filterEdit, 3, 2, 1, 2)
        layout.addWidget(copyDataLabel, 4, 0)
        layout.addWidget(self.copyDataBox, 4, 1, 1, 2)
        layout.addWidget(formatLabel, 5, 0)
        layout.addWidget(self.formatEdit, 5, 1, 1, 2)
        layout.addWidget(authorLabel, 6, 0)
        layout.addWidget(self.authorEdit, 6, 1, 1, 2)
        layout.addWidget(createddateLabel, 7, 0)
        layout.addWidget(self.createddateEdit, 7, 1, 1, 2)
        layout.addWidget(cancelButton, 8, 2, qtpy.QtCore.Qt.AlignRight)
        layout.addWidget(importButton, 8, 3, qtpy.QtCore.Qt.AlignRight)
        layout.addWidget(QWidget(), 9, 0)

        self.progressBar = QProgressBar()
        self.progressBar.setVisible(False)
        layout.addWidget(self.progressBar, 8, 1, 1, 3)

    def update(self, action: SgAction):
        if action.state == SgExperimentStates.Progress:
            if 'progress' in self.container.progress:
                self.progressBar.setVisible(True)
                self.progressBar.setValue(self.container.progress)
                if self.container.progress == 100:
                    self.progressBar.setVisible(False)

    def cancelButtonClicked(self):
        self.container.emit(SgExperimentStates.CancelImport)

    def importButtonClicked(self):
        self.container.import_info.dir_data_path = self.dataPath.text()
        self.container.import_info.dir_recursive = self.recursiveBox.isChecked()
        self.container.import_info.dir_filter = self.filterComboBox.currentIndex()
        self.container.import_info.dir_filter_value = self.filterEdit.text()
        self.container.import_info.dir_copy_data = self.copyDataBox.isChecked()
        self.container.import_info.author = self.authorEdit.text()
        self.container.import_info.format = self.formatEdit.text()
        self.container.import_info.created_date = self.createddateEdit.text()
        self.container.emit(SgExperimentStates.NewImportDir)

    def browseDataButtonClicked(self):
        directory = QFileDialog.getExistingDirectory(
            self.widget,
            self.widget.tr("Select Directory"),
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        self.dataPath.setText(directory)

    def get_widget(self):
        return self.widget


class SgExperimentTagComponent(SgComponent):
    def __init__(self, container: SgExperimentContainer):
        super().__init__()
        self._object_name = 'SgExperimentTagComponent'
        self.container = container
        self.container.register(self)

        self.widget = QWidget()
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        self.widget.setObjectName("SgWidget")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(layout)
        tabWidget = QTabWidget()
        layout.addWidget(tabWidget)

        tagsListComponent = SgExperimentTagsListComponent(self.container)
        tagUsingSeparatorComponent = SgExperimentTagsUsingSeparatorsComponent(
            self.container)
        tagUsingNameComponent = SgExperimentTagsUsingNameComponent(self.container)

        tabWidget.addTab(tagsListComponent.get_widget(),
                         self.widget.tr("Tags"))
        tabWidget.addTab(tagUsingSeparatorComponent.get_widget(),
                         self.widget.tr("Tag using separator"))
        tabWidget.addTab(tagUsingNameComponent.get_widget(),
                         self.widget.tr("Tag using name"))

    def update(self, action: SgAction):
        pass

    def get_widget(self):
        return self.widget


class SgExperimentTagsListComponent(SgComponent):
    def __init__(self, container: SgExperimentContainer):
        super().__init__()
        self._object_name = 'SgExperimentTagsListComponent'
        self.container = container
        self.container.register(self)

        self.widget = QWidget()
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        self.widget.setObjectName("SgWidget")

        layout = QVBoxLayout()
        self.widget.setLayout(layout)

        # title
        title = QLabel(self.widget.tr("Tags"))
        title.setObjectName("SgLabelFormHeader1")

        # add widget
        addWidget = QWidget()
        addLayout = QHBoxLayout()
        addWidget.setLayout(addLayout)

        self.addEdit = QLineEdit(self.widget)
        addButton = QPushButton(self.widget.tr("Add"))
        addButton.setObjectName("btnDefault")
        addLayout.addWidget(self.addEdit)
        addLayout.addWidget(addButton)

        self.tagListWidget = QWidget()
        self.tagListWidget.setObjectName("SgWidget")
        self.tagListLayout = QVBoxLayout()
        self.tagListWidget.setLayout(self.tagListLayout)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setObjectName("SgWidget")
        scrollArea.setWidget(self.tagListWidget)

        # button area
        buttonsWidget = QWidget()
        buttonsLayout = QHBoxLayout()
        buttonsLayout.setContentsMargins(0, 0, 0, 0)
        buttonsLayout.setSpacing(2)
        buttonsWidget.setLayout(buttonsLayout)
        cancelButton = QPushButton(self.widget.tr("Cancel"))
        cancelButton.setObjectName("btnDefault")
        saveButton = QPushButton(self.widget.tr("Save"))
        saveButton.setObjectName("btnPrimary")
        buttonsLayout.addWidget(cancelButton, 1, qtpy.QtCore.Qt.AlignRight)
        buttonsLayout.addWidget(saveButton, 0, qtpy.QtCore.Qt.AlignRight)

        layout.addWidget(title, 0, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(addWidget, 0, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(scrollArea, 1)
        layout.addWidget(buttonsWidget, 0, qtpy.QtCore.Qt.AlignBottom)

        addButton.released.connect(self.addButtonClicked)
        cancelButton.released.connect(self.cancelButtonClicked)
        saveButton.released.connect(self.saveButtonClicked)

    def update(self, action: SgAction):
        if action.state == SgExperimentStates.ExperimentLoaded:
            self.reload()
            return

    def reload(self):
        # free layout
        for i in reversed(range(self.tagListLayout.count())):
            self.tagListLayout.itemAt(i).widget().deleteLater()

        # add tags
        for tag in self.container.experiment.tag_keys:
            tagWidget = SgTagWidget()
            tagWidget.setContent(tag)
            tagWidget.remove.connect(self.removeClicked)
            self.tagListLayout.addWidget(tagWidget)
        self.tagListWidget.adjustSize()

    def addButtonClicked(self):
        if self.addEdit.text() != "":
            tagWidget = SgTagWidget()
            tagWidget.setContent(self.addEdit.text())
            tagWidget.remove.connect(self.removeClicked)
            self.tagListLayout.addWidget(tagWidget)
            self.addEdit.setText("")
            self.tagListLayout.update()

    def cancelButtonClicked(self):
        self.reload()
        self.container.emit(SgExperimentStates.CancelTag)

    def saveButtonClicked(self):
        tags = []
        for i in range(self.tagListLayout.count()):
            item = self.tagListLayout.itemAt(i)
            widget = item.widget()
            if widget:
                tags.append(widget.content())
        self.container.tag_info.tags = tags
        self.container.emit(SgExperimentStates.TagsModified)

    def removeClicked(self, tag: str):
        for i in range(self.tagListLayout.count()):
            item = self.tagListLayout.itemAt(i)
            widget = item.widget()
            if widget:
                if widget.content() == tag:
                    itemd = self.tagListLayout.takeAt(i)
                    itemd.widget().deleteLater()
        self.tagListWidget.adjustSize()

    def get_widget(self):
        return self.widget


class SgExperimentTagsUsingSeparatorsComponent(SgComponent):
    def __init__(self, container: SgExperimentContainer):
        super().__init__()
        self._object_name = 'SgExperimentTagsUsingSeparatorsComponent'
        self.container = container
        self.container.register(self)
        self._tagsEdit = []
        self._separatorEdit = []
        self._positionSpinBox = []

        self.widget = QWidget()
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        self.widget.setObjectName("SgWidget")

        layout = QGridLayout()
        self.widget.setLayout(layout)

        # title
        title = QLabel(self.widget.tr("Tag using separator"))
        title.setObjectName("SgLabelFormHeader1")

        gridWidget = QWidget()
        self.gridLayout = QGridLayout()
        gridWidget.setLayout(self.gridLayout)

        tagLabel = QLabel(self.widget.tr("Tag"))
        tagLabel.setObjectName("SgWidget")
        separatorLabel = QLabel(self.widget.tr("Separator"))
        separatorLabel.setObjectName("SgWidget")
        positionLabel = QLabel(self.widget.tr("Position"))
        positionLabel.setObjectName("SgWidget")

        tagsEdit = QLineEdit()
        self._tagsEdit.append(tagsEdit)
        separatorEdit = QLineEdit()
        self._separatorEdit.append(separatorEdit)
        positionSpinBox = QSpinBox()
        self._positionSpinBox.append(positionSpinBox)

        addLineButton = QPushButton(self.widget.tr("Add line"))
        addLineButton.setObjectName('btnDefault')
        addLineButton.released.connect(self.addLine)

        validateButton = QPushButton(self.widget.tr("Validate"))
        validateButton.setObjectName('btnPrimary')
        validateButton.released.connect(self.validated)

        layout.addWidget(title, 0, 0, 1, 3)

        self.gridLayout.addWidget(tagLabel, 0, 0)
        self.gridLayout.addWidget(separatorLabel, 0, 1)
        self.gridLayout.addWidget(positionLabel, 0, 2)

        self.gridLayout.addWidget(tagsEdit, 1, 0)
        self.gridLayout.addWidget(separatorEdit, 1, 1)
        self.gridLayout.addWidget(positionSpinBox, 1, 2)

        layout.addWidget(gridWidget, 1, 0, 1, 3)
        layout.addWidget(addLineButton, 2, 0)
        layout.addWidget(validateButton, 3, 2)
        layout.addWidget(QWidget())

    def validated(self):
        tags = []
        separator = []
        position = []
        for tag in self._tagsEdit:
            tags.append(tag.text())
        for sep in self._separatorEdit:
            separator.append(sep.text())
        for pos in self._positionSpinBox:
            position.append(pos.value())

        self.container.tag_info.usingseparator_tags = tags
        self.container.tag_info.usingseparator_separator = separator
        self.container.tag_info.usingseparator_position = position
        self.container.emit(SgExperimentStates.TagUsingSeparators)

    def addLine(self):
        tagsEdit = QLineEdit()
        self._tagsEdit.append(tagsEdit)
        separatorEdit = QLineEdit()
        self._separatorEdit.append(separatorEdit)
        positionSpinBox = QSpinBox()
        self._positionSpinBox.append(positionSpinBox)

        rowIdx = self.gridLayout.count()
        self.gridLayout.addWidget(tagsEdit, rowIdx, 0)
        self.gridLayout.addWidget(separatorEdit, rowIdx, 1)
        self.gridLayout.addWidget(positionSpinBox, rowIdx, 2)

    def update(self, action: SgAction):
        pass

    def get_widget(self):
        return self.widget


class SgExperimentTagsUsingNameComponent(SgComponent):
    def __init__(self, container: SgExperimentContainer):
        super().__init__()
        self._object_name = 'SgExperimentTagsUsingNameComponent'
        self.container = container
        self.container.register(self)

        self._namesEdit = []

        self.widget = QWidget()
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        self.widget.setObjectName("SgWidget")

        layout = QGridLayout()
        self.widget.setLayout(layout)

        # title
        title = QLabel(self.widget.tr("Tag using name"))
        title.setObjectName("SgLabelFormHeader1")

        tagLabel = QLabel(self.widget.tr("Tag:"))
        tagLabel.setObjectName("SgWidget")
        self.tagEdit = QLineEdit()

        searchLabel = QLabel(self.widget.tr("Search names:"))
        searchLabel.setObjectName("SgWidget")
        searchWidget = QWidget()
        self.searchLayout = QVBoxLayout()
        self.searchLayout.setContentsMargins(0, 0, 0, 0)
        searchWidget.setLayout(self.searchLayout)

        nameEdit = QLineEdit()
        self._namesEdit.append(nameEdit)
        self.searchLayout.addWidget(nameEdit)

        addLineButton = QPushButton(self.widget.tr("Add name"))
        addLineButton.setObjectName('btnDefault')
        addLineButton.released.connect(self.addLine)

        validateButton = QPushButton(self.widget.tr("Validate"))
        validateButton.setObjectName('btnPrimary')
        validateButton.released.connect(self.validated)

        layout.addWidget(title, 0, 0)
        layout.addWidget(tagLabel, 1, 0, 1, 1, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(self.tagEdit, 1, 1)
        layout.addWidget(searchLabel, 2, 0, 1, 1, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(searchWidget, 2, 1)
        layout.addWidget(addLineButton, 3, 1)
        layout.addWidget(validateButton, 4, 2)
        layout.addWidget(QWidget())

    def validated(self):
        names = []
        for name in self._namesEdit:
            names.append(name.text())
        self.container.tag_info.usingname_tag = self.tagEdit.text()
        self.container.tag_info.usingname_search = names
        self.container.emit(SgExperimentStates.TagUsingName)

    def addLine(self):
        nameEdit = QLineEdit()
        self._namesEdit.append(nameEdit)
        self.searchLayout.addWidget(nameEdit)

    def update(self, action: SgAction):
        pass

    def get_widget(self):
        return self.widget
