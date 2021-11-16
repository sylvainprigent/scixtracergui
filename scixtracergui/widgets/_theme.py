import os.path


class SgTheme:
    """Utilisies for GUI theme"""
    def __init__(self, theme_dir=''):
        if theme_dir == "":
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.theme_dir = os.path.join(current_dir, '..', '..', 'theme', 'napari')
        else:
            self.theme_dir =  theme_dir   
        print('theme dir=', self.theme_dir)    

    def icon(self, name):
        return os.path.join(self.theme_dir, f'{name}.svg')     


class SgThemeAccess:
    """Singleton to access the theme

    Parameters
    ----------
    config_file
        JSON file where the config is stored

    Raises
    ------
    Exception: if multiple instantiation of the Config is tried

    """

    __instance = None

    def __init__(self, theme=''):
        """ Virtually private constructor. """
        SgThemeAccess.__instance = SgTheme(theme)

    @staticmethod
    def instance():
        """ Static access method to the Config. """
        if SgThemeAccess.__instance is None:
            SgThemeAccess.__instance = SgTheme()
        return SgThemeAccess.__instance    
    