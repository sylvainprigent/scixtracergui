import qtpy.QtCore
from qtpy.QtWidgets import (QWidget, QLabel, QVBoxLayout, QScrollArea,
                            QTableWidget, QTableWidgetItem,
                            QAbstractItemView, QGridLayout, QHBoxLayout,
                            QToolButton, QSplitter, QLineEdit, QPushButton,
                            QTextEdit, QMessageBox, QFileDialog)

from scixtracergui.framework import SgComponent, SgAction
from scixtracergui.metadata.states import (SgRawDataStates,
                                           SgProcessedDataStates,
                                           SgMetadataExperimentStates,
                                           SgRunStates)
from scixtracergui.metadata.containers import (SgRawDataContainer,
                                               SgProcessedDataContainer,
                                               SgMetadataExperimentContainer,
                                               SgRunContainer)


class SgRawDataComponent(SgComponent):
    def __init__(self, container: SgRawDataContainer):
        super().__init__()
        self._object_name = 'SgMetadataRawDataComponent'
        self.container = container
        self.container.register(self)

        self.widget = QScrollArea()
        self.widget.setObjectName('SgWidget')
        self.widget.setWidgetResizable(True)
        self.widget.setMinimumWidth(150)

        widget = QWidget()
        widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        widget.setObjectName("SgWidget")
        layout = QGridLayout()
        widget.setLayout(layout)
        self.tagWidgets = {}
        self.widget.setWidget(widget)

        uriLabel = QLabel('URI')
        self.uriEdit = QLineEdit()
        self.uriEdit.setEnabled(False)
        self.uriEdit.setAttribute(qtpy.QtCore.Qt.WA_MacShowFocusRect, False)

        nameLabel = QLabel('Name')
        self.nameEdit = QLineEdit()
        self.nameEdit.setAttribute(qtpy.QtCore.Qt.WA_MacShowFocusRect, False)

        formatLabel = QLabel('Format')
        self.formatEdit = QLineEdit()
        self.formatEdit.setAttribute(qtpy.QtCore.Qt.WA_MacShowFocusRect, False)

        dateLabel = QLabel('Date')
        self.dateEdit = QLineEdit()
        self.dateEdit.setAttribute(qtpy.QtCore.Qt.WA_MacShowFocusRect, False)

        authorLabel = QLabel('Author')
        self.authorEdit = QLineEdit()
        self.authorEdit.setAttribute(qtpy.QtCore.Qt.WA_MacShowFocusRect, False)

        tagsWidget = QWidget()
        self.tagsLayout = QGridLayout()
        self.tagsLayout.setContentsMargins(0, 0, 0, 0)
        tagsWidget.setLayout(self.tagsLayout)

        saveButton = QPushButton(self.widget.tr("Save"))
        saveButton.setObjectName("btnPrimary")
        saveButton.released.connect(self.saveButtonClicked)

        descLabel = QLabel('Description')
        descLabel.setObjectName('SgMetadataTitle')
        tagsLabel = QLabel('Tags')
        tagsLabel.setObjectName('SgMetadataTitle')

        layout.addWidget(descLabel, 0, 0, 1, 2)
        layout.addWidget(uriLabel, 1, 0)
        layout.addWidget(self.uriEdit, 1, 1)
        layout.addWidget(nameLabel, 2, 0)
        layout.addWidget(self.nameEdit, 2, 1)
        layout.addWidget(formatLabel, 3, 0)
        layout.addWidget(self.formatEdit, 3, 1)
        layout.addWidget(dateLabel, 4, 0)
        layout.addWidget(self.dateEdit, 4, 1)
        layout.addWidget(authorLabel, 5, 0)
        layout.addWidget(self.authorEdit, 5, 1)
        layout.addWidget(tagsLabel, 6, 0, 1, 2)
        layout.addWidget(tagsWidget, 7, 0, 1, 2)
        layout.addWidget(saveButton, 8, 0, 1, 2)
        layout.addWidget(QWidget(), 9, 0, 1, 2, qtpy.QtCore.Qt.AlignTop)
        layout.setAlignment(qtpy.QtCore.Qt.AlignTop)

    def saveButtonClicked(self):
        self.container.rawdata.name = self.nameEdit.text()
        self.container.rawdata.format = self.formatEdit.text()
        self.container.rawdata.date = self.dateEdit.text()
        self.container.rawdata.author = self.authorEdit.text()

        for key in self.tagWidgets:
            self.container.rawdata.tags[key] = self.tagWidgets[key].text()

        self.container.emit(SgRawDataStates.SaveClicked)

    def update(self, action: SgAction):
        if action.state == SgRawDataStates.Loaded:
            self.nameEdit.setText(self.container.rawdata.name)
            self.formatEdit.setText(self.container.rawdata.format)
            self.dateEdit.setText(self.container.rawdata.date)
            self.authorEdit.setText(self.container.rawdata.author)
            self.uriEdit.setText(self.container.rawdata.uri)

            # tags
            for i in reversed(range(self.tagsLayout.count())): 
                self.tagsLayout.itemAt(i).widget().deleteLater()
            self.tagWidgets = {}
            row_idx = -1    
            for key in self.container.rawdata.tags:
                label = QLabel(key)
                edit = QLineEdit(self.container.rawdata.tags[key])
                row_idx += 1
                self.tagsLayout.addWidget(label, row_idx, 0) 
                self.tagsLayout.addWidget(edit, row_idx, 1)
                self.tagWidgets[key] = edit

        if action.state == SgRawDataStates.Saved:
            msgBox = QMessageBox()
            msgBox.setText("Metadata have been saved")
            msgBox.exec()            

    def get_widget(self): 
        return self.widget  


class SgProcessedDataComponent(SgComponent):
    def __init__(self, container: SgProcessedDataContainer):
        super().__init__()
        self._object_name = 'SgMetadataProcessedDataComponent'
        self.container = container
        self.container.register(self)

        self.widget = QScrollArea()
        self.widget.setObjectName('SgWidget')
        # self.widget.setBackgroundRole(QPalette.Dark)
        self.widget.setWidgetResizable(True)
        self.widget.setMinimumWidth(150)

        widget = QWidget()
        widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        widget.setObjectName("SgWidget")
        layout = QGridLayout()
        widget.setLayout(layout)
        self.widget.setWidget(widget)

        uriLabel = QLabel('URI')
        self.uriEdit = QLineEdit()
        self.uriEdit.setEnabled(False)

        nameLabel = QLabel('Name')
        self.nameEdit = QLineEdit()
        self.nameEdit.setEnabled(False)

        authorLabel = QLabel('Author')
        self.authorEdit = QLineEdit()
        self.authorEdit.setEnabled(False)

        dateLabel = QLabel('Date')
        self.dateEdit = QLineEdit()
        self.dateEdit.setEnabled(False)

        formatLabel = QLabel('Format')
        self.formatEdit = QLineEdit()
        self.formatEdit.setEnabled(False)

        outlabelLabel = QLabel('Label')
        self.outlabelEdit = QLineEdit()
        self.outlabelEdit.setEnabled(False)

        originLabel = QLabel('Parent')
        self.originEdit = QLineEdit()
        self.originEdit.setEnabled(False)

        descLabel = QLabel('Description')
        descLabel.setObjectName('SgMetadataTitle')
        tagsLabel = QLabel('Tags')
        tagsLabel.setObjectName('SgMetadataTitle')
        originTitleLabel = QLabel('Origin')
        originTitleLabel.setObjectName('SgMetadataTitle')

        tagsWidget = QWidget()
        self.tagsLayout = QGridLayout()
        self.tagsLayout.setContentsMargins(0, 0, 0, 0)
        tagsWidget.setLayout(self.tagsLayout)

        layout.addWidget(descLabel, 0, 0, 1, 2, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(uriLabel, 1, 0, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(self.uriEdit, 1, 1, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(nameLabel, 2, 0, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(self.nameEdit, 2, 1, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(formatLabel, 3, 0, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(self.formatEdit, 3, 1, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(dateLabel, 4, 0, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(self.dateEdit, 4, 1, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(authorLabel, 5, 0, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(self.authorEdit, 5, 1, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(tagsLabel, 6, 0, 1, 2, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(outlabelLabel, 7, 0, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(self.outlabelEdit, 7, 1, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(tagsWidget, 8, 0, 1, 2, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(originTitleLabel, 9, 0, 1, 2,
                         qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(originLabel, 10, 0, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(self.originEdit, 10, 1, qtpy.QtCore.Qt.AlignTop)
        layout.addWidget(QWidget(), 11, 0, 1, 2, qtpy.QtCore.Qt.AlignTop)
        layout.setAlignment(qtpy.QtCore.Qt.AlignTop)

    def emitRun(self):
        self.container.emit(SgProcessedDataStates.RunOpenClicked)

    def update(self, action: SgAction):
        if action.state == SgProcessedDataStates.Loaded:
            metadata = self.container.processeddata

            self.uriEdit.setText(metadata.uri)
            self.nameEdit.setText(metadata.name)
            self.authorEdit.setText(metadata.author)
            self.dateEdit.setText(metadata.date)
            self.formatEdit.setText(metadata.format)
            self.outlabelEdit.setText(metadata.output['label'])

            # tags
            orig = self.container.processed_origin
            if orig:
                origin = orig
                for i in reversed(range(self.tagsLayout.count())): 
                    self.tagsLayout.itemAt(i).widget().deleteLater()
                self.tagWidgets = {}
                row_idx = -1
                for key in origin.tags:
                    label = QLabel(key)
                    edit = QLineEdit(origin.tags[key])
                    edit.setEnabled(False)
                    row_idx += 1
                    self.tagsLayout.addWidget(label, row_idx, 0) 
                    self.tagsLayout.addWidget(edit, row_idx, 1)
                    self.tagWidgets[key] = edit

            parent = self.container.processed_parent
            if parent:
                self.originEdit.setText(parent.name)
            else:
                self.originEdit.setText("")    

    def get_widget(self): 
        return self.widget  


class SgMetadataExperimentComponent(SgComponent):
    def __init__(self, container: SgMetadataExperimentContainer):
        super().__init__()
        self._object_name = 'SgMetadataExperimentComponent'
        self.container = container
        self.container.register(self)

        self.widget = QWidget()
        self.widget.setObjectName('SgWidget')
        self.widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel(self.widget.tr("Experiment information"))
        title.setObjectName("SgLabelFormHeader1")
        title.setMaximumHeight(50)

        nameLabel = QLabel('Name')
        nameLabel.setObjectName('SgLabel')
        self.nameEdit = QLineEdit()
        self.nameEdit.setAttribute(qtpy.QtCore.Qt.WA_MacShowFocusRect, False)

        authorLabel = QLabel('Author')
        authorLabel.setObjectName('SgLabel')
        self.authorEdit = QLineEdit()
        self.authorEdit.setAttribute(qtpy.QtCore.Qt.WA_MacShowFocusRect, False)

        createddateLabel = QLabel('Created date')
        createddateLabel.setObjectName('SgLabel')
        self.createddateEdit = QLineEdit()
        self.createddateEdit.setAttribute(qtpy.QtCore.Qt.WA_MacShowFocusRect,
                                          False)

        saveButton = QPushButton(self.widget.tr("Save"))
        saveButton.setObjectName("btnPrimary")
        saveButton.released.connect(self.saveButtonClicked)

        cancelButton = QPushButton(self.widget.tr("Cancel"))
        cancelButton.setObjectName("btnDefault")
        cancelButton.released.connect(self.cancelButtonClicked)

        btnWidget = QWidget()
        btnLayout = QHBoxLayout()
        btnLayout.setContentsMargins(0, 0, 0, 0)
        btnLayout.setSpacing(2)
        btnLayout.addWidget(cancelButton)
        btnLayout.addWidget(saveButton)
        btnWidget.setLayout(btnLayout)

        layout.addWidget(title, 0, 0, 1, 2)
        layout.addWidget(nameLabel, 1, 0)
        layout.addWidget(self.nameEdit, 1, 1)
        layout.addWidget(authorLabel, 2, 0)
        layout.addWidget(self.authorEdit, 2, 1)
        layout.addWidget(createddateLabel, 3, 0)
        layout.addWidget(self.createddateEdit, 3, 1)
        layout.addWidget(btnWidget, 4, 1, 1, 1, qtpy.QtCore.Qt.AlignRight)

        w = QWidget()
        w.setLayout(layout)

        totallayout = QVBoxLayout()
        totallayout.addWidget(w, 0)
        totallayout.addWidget(QWidget(), 1)
        self.widget.setLayout(totallayout)

    def cancelButtonClicked(self):
        self.nameEdit.setText(self.container.experiment.name)
        self.authorEdit.setText(self.container.experiment.author)
        self.createddateEdit.setText(self.container.experiment.date)
        self.container.emit(SgMetadataExperimentStates.CancelClicked)

    def saveButtonClicked(self):
        self.container.experiment.name = self.nameEdit.text()
        self.container.experiment.author = self.authorEdit.text()
        self.container.experiment.date = self.createddateEdit.text()
        self.container.emit(SgMetadataExperimentStates.SaveClicked)

    def update(self, action: SgAction):
        if action.state == SgMetadataExperimentStates.Loaded:
            self.nameEdit.setText(self.container.experiment.name)
            self.authorEdit.setText(self.container.experiment.author)
            self.createddateEdit.setText(self.container.experiment.date)

        if action.state == SgMetadataExperimentStates.Saved:
            msgBox = QMessageBox()
            msgBox.setText("Information have been saved")
            msgBox.exec()  

    def get_widget(self): 
        return self.widget    


class SgMetadataRunComponent(SgComponent):
    def __init__(self, container: SgRunContainer):
        super().__init__()
        self._object_name = 'SgMetadataRunComponent'
        self.container = container
        self.container.register(self)

        self.widget = QScrollArea()
        self.widget.setObjectName('SgWidget')
        self.widget.setWidgetResizable(True)
        self.widget.setMinimumWidth(150)

        widget = QWidget()
        widget.setAttribute(qtpy.QtCore.Qt.WA_StyledBackground, True)
        widget.setObjectName("SgWidget")
        layout = QGridLayout()
        widget.setLayout(layout)
        self.widget.setWidget(widget)

        toolLabel = QLabel('Tool')
        self.toolEdit = QLineEdit()
        self.toolEdit.setEnabled(False)

        tooluriLabel = QLabel('Name')
        self.tooluriEdit = QLineEdit()
        self.tooluriEdit.setEnabled(False)

        parametersLabel = QLabel('Parameters')
        parametersLabel.setObjectName('SgMetadataTitle')

        self.parametersTable = QTableWidget()
        self.parametersTable.setMinimumHeight(100)

        inputsLabel = QLabel('Inputs')
        inputsLabel.setObjectName('SgMetadataTitle')

        self.inputsTable = QTableWidget()
        self.inputsTable.setMinimumHeight(100)

        tagsWidget = QWidget()
        self.tagsLayout = QGridLayout()
        self.tagsLayout.setContentsMargins(0, 0, 0, 0)
        tagsWidget.setLayout(self.tagsLayout)

        layout.addWidget(toolLabel, 0, 0)
        layout.addWidget(self.toolEdit, 0, 1)
        layout.addWidget(tooluriLabel, 1, 0)
        layout.addWidget(self.tooluriEdit, 1, 1)
        layout.addWidget(parametersLabel, 2, 0, 1, 2)
        layout.addWidget(self.parametersTable, 3, 0, 1, 2)
        layout.addWidget(inputsLabel, 4, 0, 1, 2)
        layout.addWidget(self.inputsTable, 5, 0, 1, 2)
        layout.addWidget(QWidget(), 6, 0, 1, 2, qtpy.QtCore.Qt.AlignTop)

    def update(self, action: SgAction):
        if action.state == SgRunStates.Loaded:
            metadata = self.container.run

            self.toolEdit.setText(metadata.process_name)
            self.tooluriEdit.setText(metadata.process_uri)

            # parameters
            self.parametersTable.setColumnCount(2)
            self.parametersTable.setHorizontalHeaderLabels(["Name", "Value"])
            self.parametersTable.setRowCount(0)
            self.parametersTable.setRowCount(len(metadata.parameters))
            row_idx = 0
            for param in metadata.parameters:
                self.parametersTable.setItem(row_idx, 0,
                                             QTableWidgetItem(param.name))
                self.parametersTable.setItem(row_idx, 1,
                                             QTableWidgetItem(str(param.value)))
                row_idx += 1

            # inputs
            self.inputsTable.setColumnCount(3)
            self.inputsTable.setHorizontalHeaderLabels(["Name", "Dataset",
                                                        "Query"])
            self.inputsTable.setRowCount(0)
            self.inputsTable.setRowCount(len(metadata.inputs))
            row_idx = 0
            for input in metadata.inputs:
                self.inputsTable.setItem(row_idx, 0,
                                         QTableWidgetItem(input.name))
                self.inputsTable.setItem(row_idx, 1,
                                         QTableWidgetItem(input.dataset))
                self.inputsTable.setItem(row_idx, 2,
                                         QTableWidgetItem(input.query))
                row_idx += 1

    def get_widget(self): 
        return self.widget                        
