import scixtracer as sx

from scixtracergui.framework import SgModel, SgAction
from ._states import (SgExperimentCreateStates,
                                             SgExperimentStates)
from ._containers import (SgExperimentCreateContainer,
                                                 SgExperimentContainer)


class SgExperimentModel(SgModel):
    def __init__(self, container: SgExperimentContainer):
        super().__init__()
        self._object_name = 'SgExperimentModel'
        self.container = container
        self.container.register(self)
        self.req = sx.Request()

    def update(self, action: SgAction):
        if action.state == SgExperimentStates.ExperimentLoad:
            self.container.experiment = self.req.get_experiment(
                self.container.experiment_uri)
            self.container.dataset = self.req.get_dataset(
                self.container.experiment, 'data'
            )
            self.container.dataset_name = 'data'
            self.container.emit(SgExperimentStates.ExperimentLoaded)

        if action.state == SgExperimentStates.DatasetChanged or \
                action.state == SgExperimentStates.RefreshClicked:
            self.container.dataset = self.req.get_dataset(
                                 self.container.experiment,
                                 self.container.dataset_name)
            self.container.emit(SgExperimentStates.DataSetLoaded)

        if action.state == SgExperimentStates.NewImportFile:
            self.req.import_data(
                experiment=self.container.experiment,
                data_path=self.container.import_info.file_data_path,
                name=self.container.import_info.file_name,
                author=self.container.import_info.author,
                format_=self.container.import_info.format,
                date=self.container.import_info.created_date,
                tags=dict,
                copy=self.container.import_info.file_copy_data
            )
            self.container.emit(SgExperimentStates.DataImported)

        if action.state == SgExperimentStates.NewImportDir:
            filter_regexp = ''
            if self.container.import_info.dir_filter == 0:
                filter_regexp = '\\' + self.container.import_info.dir_filter_value + '$'
            elif self.container.import_info.dir_filter == 1:
                filter_regexp = self.container.import_info.dir_filter_value
            elif self.container.import_info.dir_filter == 2:
                filter_regexp = '^' + self.container.import_info.dir_filter_value

            self.req.import_dir(
                experiment=self.container.experiment,
                dir_uri=self.container.import_info.dir_data_path,
                filter_=filter_regexp,
                author=self.container.import_info.author,
                format_=self.container.import_info.format,
                date=self.container.import_info.created_date,
                copy_data=self.container.import_info.dir_copy_data
            )
            self.container.emit(SgExperimentStates.DataImported)

        if action.state == SgExperimentStates.TagsModified:
            self.req.set_tag_keys(
                experiment=self.container.experiment,
                keys=self.container.tag_info.tags
            )
            self.container.emit(SgExperimentStates.TagsSaved)

        if action.state == SgExperimentStates.TagUsingSeparators:
            for i in range(len(self.container.tag_info.usingseparator_tags)):

                self.req.tag_using_separator(
                    experiment=self.container.experiment,
                    tag=self.container.tag_info.usingseparator_tags[i],
                    separator=self.container.tag_info.usingseparator_separator[
                        i],
                    value_position=
                    self.container.tag_info.usingseparator_position[i]
                )
            self.container.emit(SgExperimentStates.DataTagged)

        if action.state == SgExperimentStates.TagUsingName:
            self.req.tag_from_name(
                experiment=self.container.experiment,
                tag=self.container.tag_info.usingname_tag,
                values=self.container.tag_info.usingname_search
            )
            self.container.emit(SgExperimentStates.DataTagged)


class SgExperimentCreateModel(SgModel):

    def __init__(self, container: SgExperimentCreateContainer):
        super().__init__()
        self._object_name = 'SgExperimentCreateModel'
        self.container = container
        self.container.register(self)
        self.req = sx.Request()

    def update(self, action: SgAction):
        if action.state == SgExperimentCreateStates.CreateClicked:
            try:
                experiment = self.req.create_experiment(
                    name=self.container.experiment_name,
                    author=self.container.experiment_author,
                    date='now',
                    destination=self.container.experiment_destination_dir)
                self.container.experiment_dir = experiment.md_uri
                self.container.emit(SgExperimentCreateStates.ExperimentCreated)
            except FileNotFoundError as err:
                self.container.errorMessage = err
                self.container.emit(
                    SgExperimentCreateStates.ExperimentCreationError
                )
