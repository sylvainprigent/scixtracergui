from scixtracergui.framework import SgContainer


class SgRawDataContainer(SgContainer):

    def __init__(self):
        super().__init__()
        self._object_name = 'SgRawDataContainer'

        # data
        self.md_uri = '' 
        self.rawdata = None     


class SgProcessedDataContainer(SgContainer):

    def __init__(self):
        super().__init__()
        self._object_name = 'SgProcessedDataContainer'

        # data
        self.md_uri = '' 
        self.processeddata = None     


class SgRunContainer(SgContainer):

    def __init__(self):
        super().__init__()
        self._object_name = 'SgRunContainer'

        # data
        self.md_uri = '' 
        self.run = None               


class SgMetadataExperimentContainer(SgContainer):

    def __init__(self):
        super().__init__()
        self._object_name = 'SgMetadataExperimentContainer'

        # data
        self.md_uri = '' 
        self.experiment = None           
