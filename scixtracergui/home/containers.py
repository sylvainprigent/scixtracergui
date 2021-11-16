from scixtracergui.framework import SgContainer


class SgHomeContainer(SgContainer):
    def __init__(self):
        super().__init__()
        self._object_name = 'SgHomeContainer'

        # data
        self.experiments = []
        self.clicked_experiment = ''
