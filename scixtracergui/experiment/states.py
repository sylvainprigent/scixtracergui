from scixtracergui.framework import SgStates


class SgExperimentStates(SgStates):
    ExperimentLoad = "SgExperimentStates.ExperimentLoad"
    ExperimentLoaded = "SgExperimentStates.ExperimentLoaded"
    EditInfoClicked = "SgExperimentStates.EditInfoClicked"
    DatasetChanged = "SgExperimentStates.DatasetChanged"
    ImportClicked = "SgExperimentStates.ImportClicked"
    TagClicked = "SgExperimentStates.TagClicked"
    RefreshClicked = "SgExperimentStates.RefreshClicked"
    DataSetLoaded = "SgExperimentStates.DataSetLoaded"
    DataDoubleClicked = "SgExperimentStates.DataDoubleClicked"
    RawDataClicked = "SgExperimentStates.RawDataClicked"
    ProcessedDataClicked = "SgExperimentStates.ProcessedDataClicked"
    NewImportFile = "SgExperimentStates.NewImportFile"
    NewImportDir = "SgExperimentStates.NewImportDir"
    Progress = "SgExperimentStates.Progress"
    TagsModified = "SgExperimentStates.TagsModified"
    TagUsingSeparators = "SgExperimentStates.TagUsingSeparators"
    TagUsingName = "SgExperimentStates.TagUsingName"
    DataImported = "SgExperimentStates.DataImported"
    TagsSaved = "SgExperimentStates.TagsSaved"
    DataTagged = "SgExperimentStates.DataTagged"


class SgExperimentCreateStates(SgStates):
    CreateClicked = "SgExperimentCreateStates.CreateClicked"
    CancelClicked = "SgExperimentCreateStates.CancelClicked"
    ExperimentCreated = "SgExperimentCreateStates.ExperimentCreated"
    ExperimentCreationError = "SgExperimentCreateStates.ExperimentCreationError"
