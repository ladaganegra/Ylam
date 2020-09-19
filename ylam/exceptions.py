# -*- coding: utf-8 -*-
import click


class FCInvalidConfException(Exception):

    def __init__(self, path=None, verbose=False):
        self.msg = 'Invalid configuration, check it at {}'.format(path)
        super(FCInvalidConfException, self).__init__(self.msg)
        self.path = path
        if verbose:
            click.secho(self.msg, fg='yellow')


class FCFileNotFoundException(Exception):

    def __init__(self, path=None, verbose=False):
        self.msg = 'No configuration file found at {}.'.format(path)
        super(FCFileNotFoundException, self).__init__(self.msg)
        self.path = path
        if verbose:
            click.secho(self.msg, fg='yellow')


class FCNoPreviousConfigException(Exception):

    def __init__(self, path=None, verbose=False):
        self.msg = 'No previous config file at {}.'.format(path)
        super(FCNoPreviousConfigException, self).__init__(self.msg)
        self.path = path
        if verbose:
            click.secho(self.msg, fg='yellow')


class FCSavingErrorException(Exception):

    def __init__(self, path=None, verbose=False):
        self.msg = 'Error while saving file {}.'.format(path)
        super(FCSavingErrorException, self).__init__(self.msg)
        self.path = path
        if verbose:
            click.secho(self.msg, fg='yellow')


class FCNoFileAccessException(Exception):

    def __init__(self, path=None, verbose=False):
        self.msg = 'The file {} doesn\'t exists or don\'t have permissions.'.format(
            path)
        super(FCNoFileAccessException, self).__init__(self.msg)
        self.path = path
        if verbose:
            click.secho(self.msg, fg='yellow')


class FCNoFileProvidedException(Exception):

    def __init__(self, verbose=False):
        self.msg = 'You must especify a file'
        super(FCNoFileProvidedException, self).__init__(self.msg)
        if verbose:
            click.secho(self.msg, fg='yellow')


class FCMNullKey(Exception):
    ''' Excepción lanzada cuando se pide al manager una configuración sin clave '''

    def __init__(self):
        self.msg = 'No se ha proporcionado clave para recuperar'
        super(FCMNullKey, self).__init__(self.msg)


class FCMInvalidKey(Exception):
    ''' Excepción lanzada cuando se pide al manager una configuración sin clave '''

    def __init__(self, key):
        self.msg = 'No se ha encontrado un valor con la clave {}'.format(key)
        super(FCMInvalidKey, self).__init__(self.msg)
