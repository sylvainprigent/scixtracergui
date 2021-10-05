import os

import scixtracer as sx
from scixtracer import RawData, ProcessedData, Run

from scixtracergui.framework import SgModel, SgAction
from scixtracergui.metadata.states import (SgRawDataStates,
                                           SgProcessedDataStates,
                                           SgMetadataExperimentStates,
                                           SgRunStates)
from scixtracergui.metadata.containers import (SgRawDataContainer,
                                               SgProcessedDataContainer,
                                               SgMetadataExperimentContainer,
                                               SgRunContainer)


class SgRawDataModel(SgModel):
    def __init__(self, container: SgRawDataContainer):
        super().__init__()
        self._object_name = 'SgRawDataModel'
        self.container = container
        self.container.register(self)
        self.req = sx.Request()

    def update(self, action: SgAction):
        if action.state == SgRawDataStates.URIChanged:
            self.container.rawdata = self.req.get_rawdata(self.container.md_uri)
            self.container.emit(SgRawDataStates.Loaded)
            return

        if action.state == SgRawDataStates.SaveClicked:
            self.req.update_rawdata(self.container.rawdata)
            self.container.emit(SgRawDataStates.Saved)
            return


class SgProcessedDataModel(SgModel):
    def __init__(self, container: SgProcessedDataContainer):
        super().__init__()
        self._object_name = 'SgProcessedDataModel'
        self.container = container
        self.container.register(self)
        self.req = sx.Request()

    def update(self, action: SgAction):
        if action.state == SgProcessedDataStates.URIChanged:
            self.container.processeddata = \
                self.req.get_processeddata(self.container.md_uri)
            self.container.processed_origin = \
                self.req.get_origin(self.container.processeddata)
            self.container.processed_parent = \
                self.req.get_parent(self.container.processeddata)
            self.container.emit(SgProcessedDataStates.Loaded)
            return    


class SgRunModel(SgModel):
    def __init__(self, container: SgRunContainer):
        super().__init__()
        self._object_name = 'SgRunModel'
        self.container = container
        self.container.register(self)
        self.req = sx.Request()

    def update(self, action: SgAction):
        if action.state == SgRunStates.URIChanged:
            self.container.run = self.req.get_run(self.container.md_uri)
            self.container.emit(SgRunStates.Loaded)
            return  


class SgMetadataExperimentModel(SgModel):
    def __init__(self, container: SgMetadataExperimentContainer):
        super().__init__()
        self._object_name = 'SgMetadataExperimentModel'
        self.container = container
        self.container.register(self)
        self.req = sx.Request()

    def update(self, action: SgAction):
        if action.state == SgMetadataExperimentStates.SaveClicked:
            self.req.update_experiment(self.container.experiment)
            self.container.emit(SgMetadataExperimentStates.Saved)
            return
