from scixtracergui.framework import SgContainer


class SgExperimentImportContainer():
    def __init__(self):
        super().__init__()
        self.dir_data_path = ''
        self.dir_recursive = False
        self.dir_filter = ''
        self.dir_filter_value = ''
        self.dir_copy_data = True
        self.file_data_path = ''
        self.file_copy_data = True
        self.file_name = ''
        self.format = ''
        self.author = ''
        self.created_date = ''


class SgExperimentTagContainer:
    def __init__(self):
        super().__init__()
        self.tags = []
        self.usingname_tag = ''
        self.usingname_search = []
        self.usingseparator_tags = []
        self.usingseparator_separator = []
        self.usingseparator_position = []
        self.usingname_tag = ''
        self.usingname_search = []


class SgExperimentContainer(SgContainer):

    def __init__(self):
        super().__init__()
        self._object_name = 'SgExperimentContainer'

        self.experiment_uri = ''
        self.experiment = None
        self.dataset_name = ''
        self.dataset = None
        self.selected_data_info = None
        self.import_info = SgExperimentImportContainer()
        self.progress = 0
        self.tag_info = SgExperimentTagContainer()


class SgExperimentCreateContainer(SgContainer):

    def __init__(self):
        super().__init__()
        self._object_name = 'SgExperimentCreateContainer'

        # data
        self.experiment_destination_dir = ''
        self.experiment_name = ''
        self.experiment_author = ''
        self.errorMessage = ''
        self.experiment_dir = ''



