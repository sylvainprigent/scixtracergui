from scixtracergui.framework import SgStates


class SgRawDataStates(SgStates):
    URIChanged = "SgRawDataStates.URIChanged"
    Loaded = "SgRawDataStates.Loaded"
    SaveClicked = "SgRawDataStates.SaveClicked"
    Saved = "SgRawDataStates.Saved"


class SgProcessedDataStates(SgStates):
    URIChanged = "SgProcessedDataStates.URIChanged"
    Loaded = "SgProcessedDataStates.Loaded"
    RunOpenClicked = "SgProcessedDataStates.RunOpenClicked"


class SgRunStates(SgStates):
    URIChanged = "SgRunStates.URIChanged"
    Loaded = "SgRunStates.Loaded"


class SgMetadataExperimentStates(SgStates):
    Loaded = "SgMetadataExperimentStates.Loaded"
    SaveClicked = "SgMetadataExperimentStates.SaveClicked"
    Saved = "SgMetadataExperimentStates.Saved"
    CancelClicked = "SgMetadataExperimentStates.CancelClicked"
