# -*- config: utf-8 -*-
''' Módulo de excepciones personalizadas de Ylam '''


class YlamException(Exception):
    def __init__(self):
        self.msg = 'Excepción genérica de Ylam'
        super(InvalidConfException, self).__init__(self.msg)


class InvalidConfException(YlamException):
    ''' Excepción lanzada cuando la configuración no es válida '''

    def __init__(self, full_path):
        self.msg = 'La configuracion es invalida revisala en {}'.format(
            full_path)
        super(InvalidConfException, self).__init__(self.msg)


class NotFoundConfigException(YlamException):
    ''' Excepción lanzada cuando no se encuentra el fichero de configuración '''

    def __init__(self, application):
        self.msg = 'No se ha encontrado la configuracion para {}'.format(
            application)
        super(NotFoundConfigException, self).__init__(self.msg)


class CantSaveConfig(YlamException):
    ''' Excepción lanzada cuando no se puede guardar el archivo de configuración '''

    def __init__(self, full_path):
        self.msg = 'Ha ocurrido un error en el guardado de la configuracion en {}'.format(
            full_path)
        super(CantSaveConfig, self).__init__(self.msg)


class CantTouchConfig(YlamException):
    ''' Excepción lanzada cuando no se puede crear el archivo de configuración '''

    def __init__(self, full_path):
        self.msg = 'Ha ocurrido un error al crear el archivo de configuracion en {}'.format(
            full_path)
        super(CantTouchConfig, self).__init__(self.msg)


class InvalidConfException(YlamException):
    ''' Excepción lanzada cuando la configuración no es válida '''

    def __init__(self, full_path):
        self.msg = 'La configuracion es invalida revisala en {}'.format(
            full_path)
        super(InvalidConfException, self).__init__(self.msg)
