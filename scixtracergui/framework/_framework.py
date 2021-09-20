class SgObject:
    def __init__(self):
        self._object_name = 'SgObject'

   
class SgAction(SgObject):
    def __init__(self, state: str = ""):
        super().__init__()
        self._object_name = "SgAction"
        self.state = state
        self.parent_container = None


class SgStates:
    DEFAULT = "States.DEFAULT"


class SgContainer(SgObject):
    def __init__(self, parent: SgObject = None):
        super().__init__()
        self._object_name = 'SgContainer'
        self._observers = []

        self.states = None
        self.current_state = SgStates.DEFAULT

        self._children = []
        self._parent = parent
        if parent:
            parent.add_child(self)

    def add_child(self, child: SgObject):
        self._children.append(child)

    def register(self, observer):
        self._observers.append(observer)

    def emit(self, state_name: str):
        self.current_state = state_name
        action = SgAction(state_name)
        action.parent_container = self
        self.emit_action(action)

    def emit_action(self, action: SgAction):
        for observer in self._observers:
            observer.update(action)


class SgActuator(SgObject):
    def __init__(self):
        super().__init__()
        self._object_name = 'SgObserver'

    def update(self, action: SgAction):
        raise NotImplementedError("Please implement SgObserver update method")


class SgComponent(SgActuator):
    def __init__(self):
        super().__init__()
        self._object_name = 'SgComponent'

    def update(self, action: SgAction):
        raise NotImplementedError("Please implement ", self._object_name,
                                  " update method")

    def get_widget(self):  
        return None   


class SgModel(SgActuator):
    def __init__(self):
        super().__init__()
        self._object_name = 'SModel'

    def nowarning(self):
        pass    

    def update(self, action: SgAction):
        raise NotImplementedError("Please implement ", self._object_name,
                                  " update method")
