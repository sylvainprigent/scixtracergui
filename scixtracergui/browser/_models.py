import os
import json

from qtpy.QtCore import QObject, QDir, QFileInfo

from scixtracer import Experiment, Run, Dataset, RawData

from scixtracergui.framework import SgModel, SgAction
from ._states import SgBrowserStates
from ._containers import (SgBrowserContainer,
                          SgBrowserFileInfo)


class SgBrowserModel(SgModel):
    def __init__(self, container: SgBrowserContainer):
        super().__init__()
        self._object_name = 'SgBrowserModel'
        self.container = container
        self.container.register(self)
        self.files = list

    def update(self, action: SgAction):
        if action.state == SgBrowserStates.DirectoryModified or \
                action.state == SgBrowserStates.RefreshClicked:
            self.loadFiles()
            return
    
        if action.state == SgBrowserStates.ItemDoubleClicked:
            
            row = self.container.doubleClickedRow
            dcFile = self.container.files[row]
            self.browse(dcFile)
            return   

        if action.state == SgBrowserStates.PreviousClicked:
            self.container.moveToPrevious()
            self.container.emit(SgBrowserStates.DirectoryModified)
            return

        if action.state == SgBrowserStates.NextClicked:
            self.container.moveToNext()
            self.container.emit(SgBrowserStates.DirectoryModified)
            return

        if action.state == SgBrowserStates.UpClicked:
            dir = QDir(self.container.currentPath)
            dir.cdUp()
            upPath = dir.absolutePath()
            self.container.setCurrentPath(upPath)
            self.container.emit(SgBrowserStates.DirectoryModified)
            return

    def browse(self, fileInfo: SgBrowserFileInfo):
        experiment_file = os.path.join(fileInfo.path, fileInfo.fileName,
                                      'experiment.md.json')
        if os.path.isfile(experiment_file):
            self.container.openExperimentPath = os.path.join(fileInfo.path,
                                                             fileInfo.fileName,
                                                             'experiment.md.json')
            self.container.emit(SgBrowserStates.OpenExperiment)
        elif fileInfo.type == "dir":    
            self.container.setCurrentPath(os.path.join(fileInfo.path,
                                                       fileInfo.fileName))
            self.container.emit(SgBrowserStates.DirectoryModified)

    def loadFiles(self):
        dir = QDir(self.container.currentPath)
        files = dir.entryInfoList()
        self.files = []

        for i in range(len(files)):
            if files[i].fileName() != "." and files[i].fileName() != "..":
                if files[i].isDir():
                    experiment_file = os.path.join(files[i].absoluteFilePath(),
                                                   'experiment.md.json')
                    if os.path.isfile(experiment_file):
                        fileInfo = SgBrowserFileInfo(files[i].fileName(),
                                           files[i].path(),
                                           files[i].fileName(),
                                           'experiment',
                                           files[i].lastModified().toString(
                                               "yyyy-MM-dd"))
                    else:    
                        fileInfo = SgBrowserFileInfo(files[i].fileName(),
                                           files[i].path(),
                                           files[i].fileName(),
                                           'dir',
                                           files[i].lastModified().toString(
                                               "yyyy-MM-dd"))

                    self.files.append(fileInfo)

                elif files[i].fileName().endswith("experiment.md.json"):
                    experiment = Experiment(files[i].absoluteFilePath())

                    fileInfo = SgBrowserFileInfo(files[i].fileName(),
                                            files[i].path(),
                                            experiment.metadata.name,
                                            "experiment",
                                            experiment.metadata.date)
                    self.files.append(fileInfo)
                    del experiment
        
                elif files[i].fileName().endswith("run.md.json"):
                    run = Run(files[i].absoluteFilePath())
    
                    fileInfo = SgBrowserFileInfo(files[i].fileName(),
                                            files[i].path(),
                                            run.metadata.process_name,
                                            "run",
                                            files[i].lastModified().toString(
                                                "yyyy-MM-dd"))
                    self.files.append(fileInfo)
                    del run
                
                elif files[i].fileName().endswith("rawdataset.md.json"):
                    rawDataSet = Dataset(files[i].absoluteFilePath())

                    fileInfo = SgBrowserFileInfo(files[i].fileName(),
                                            files[i].path(),
                                            rawDataSet.metadata.name,
                                            "rawdataset",
                                            files[i].lastModified().toString(
                                                "yyyy-MM-dd"))
                    self.files.append(fileInfo)
                    del rawDataSet
        
                elif files[i].fileName().endswith("processeddataset.md.json"):
                    processedDataSet = Dataset(
                        files[i].absoluteFilePath())

                    fileInfo = SgBrowserFileInfo(files[i].fileName(),
                                            files[i].path(),
                                            processedDataSet.metadata.name,
                                            "processeddataset",
                                            files[i].lastModified().toString(
                                                "yyyy-MM-dd"))
                    self.files.append(fileInfo)
                    del processedDataSet
        
                elif files[i].fileName().endswith(".md.json"):
                    # test type of file raw/processed
                    metadata = None 
                    if os.path.getsize(files[i].absoluteFilePath()) > 0:
                        with open(files[i].absoluteFilePath()) as json_file:  
                            metadata = json.load(json_file)

                    name = ''
                    if 'common' in metadata:
                        if 'name' in metadata['common']:
                            name = metadata['common']['name'] 

                    type = ''
                    if 'origin' in metadata:
                        if 'type' in metadata['origin']:
                            type = metadata['origin']['type']               

                    fileInfo = SgBrowserFileInfo(files[i].fileName(),
                                            files[i].path(),
                                            name,
                                            type + "data",
                                            files[i].lastModified().toString(
                                                "yyyy-MM-dd"))
                    self.files.append(fileInfo)

        self.container.files = self.files
        self.container.emit(SgBrowserStates.FilesInfoLoaded)
