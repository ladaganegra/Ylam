# -*- coding: utf-8 -*-
import os
import ruamel.yaml as yaml
import click
import time
from .exceptions import *


class Ylam(object):

    '''YAML configuration Manager
    Checks and access configuration files in YAML, for check and modify in applications.
    Variables:
        path: {path} -- Path where the configuration is.
        verbose: {bool} -- set true to print messages on stdout
    '''

    def __init__(
        self,
        path=None,
        verbose=False
    ):
        super(Ylam, self).__init__()
        self._first_run = False
        self._verbose = verbose
        self.basedir = os.path.dirname(path)
        if path is None:
            raise FCNoFileProvidedException(self._verbose)
        if not os.path.exists(path):
            if not os.access(path, os.W_OK):
                raise FCNoFileAccessException(path, self._verbose)
            self._first_run = True
            if not os.path.exists(self.basedir):
                os.makedirs(self.basedir)
            with open(path, 'a'):
                os.utime(path, None)
        self._full_path = path
        self.config = {}
        self._read_existent_config()

    def _read_existent_config(self):
        if os.path.exists(self._full_path):
            with open(self._full_path) as local_config:
                try:
                    cfg = yaml.load(local_config, Loader=yaml.RoundTripLoader)
                except Exception:
                    raise FCInvalidConfException(
                        self._full_path, self._verbose)
                else:
                    if self._verbose:
                        click.secho(
                            'Configuration found! [{}]'.format(
                                self._full_path),
                            fg='green'
                        )
                    self.config = cfg
        else:
            raise FCFileNotFoundException(self._full_path, self._verbose)

    def _save_w_backup(self, conf_dict):
        try:
            if not self._first_run:
                os.rename(
                    self._full_path,
                    self._full_path + '.' + str(int(time.time()))
                )
        except Exception:
            raise FCNoPreviousConfigException(self._full_path, self._verbose)
        else:
            try:
                with open(self._full_path, 'w') as new_config:
                    yaml.dump(
                        conf_dict,
                        new_config,
                        default_flow_style=False,
                        Dumper=yaml.RoundTripDumper
                    )
            except Exception:
                raise FCSavingErrorException(self._full_path, self._verbose)
        return

    def _save_wo_backup(self, conf_dict):
        try:
            with open(self._full_path, 'w') as new_config:
                yaml.dump(
                    conf_dict,
                    new_config,
                    default_flow_style=False,
                    Dumper=yaml.RoundTripDumper
                )
        except Exception:
            raise FCSavingErrorException(self._full_path, self._verbose)
        return

    def _cpar_to_dict(self, cpar):
        outdict = {}
        for sect in cpar.sections():
            outdict[sect] = {}
            for k, v in cpar.items(sect):
                outdict[sect][k] = v
        return outdict

    def has_section(self, section):
        """Checks if there are a section in config file
        Arguments:
            section {strign} -- Section name (case insensitive)
        Returns:
            bool -- True if exists, False else.
        """
        if self.config is None:
            return False
        if section.upper() in [x.upper() for x in self.config]:
            return True
        return False

    def has_option(self, section, key):
        """Checks if there are a option inside a section.
        If section exists, check the existance of the key inside.
        Arguments:
            section {string} -- Section name (case insensitive)
            key {string} -- Option name (case insensitive)
        Returns:
            bool -- True if exists, False otherwise.
        """
        if section.lower() in [x.lower() for x in self.config]:
            if key.lower() in [x.lower() for x in self.config[section.upper()]]:
                return True
        return False

    def has_suboption(self, section, option, key):
        '''Checks if there are a nested option inside a option
        Arguments:
            section {string} -- Section name (case insensitive)
            option {string} -- Option name (case insensitive)
            key {string} -- Suboption name (case insensitive)
        Returns:
            bool -- True if exists, False otherwise.
        '''
        if self.has_section(section):
            if self.has_option(section, option):
                if key in self.get(section, option):
                    return True
        return False

    def get(self, section, option=None, key=None):
        '''Obtains the value of an option
        If section and option exists, returns the value
        Arguments:
            section {string} -- Section name (case insensitive)
        Keyword Arguments:
            option {string} -- Option name (case insensitve) (default: {None})
            key {string} -- Suboption name (case insensitive) (default: {None})
        Returns:
            {string, list, dict, None} -- Returns the value for the option or None.
        '''
        if not self.has_section(section):
            return None
        if option is None:
            if self.has_section(section):
                return self.config[section.upper()]
            return None
        if self.has_option(section, option):
            if key is None:
                return self.config[section.upper()][option.lower()]
            if self.has_suboption(section, option, key):
                return self.config[section.upper()][option.lower()][key.lower()]
        return None

    def set(self, section, key, value, suboption=None, save=False):
        """Sets a value inside a option, and optionally, saves it.
        Arguments:
            section {string} -- Section name (case insensitve)
            key {string} -- Option name (case insensitive)
            value {string, list, dict} -- Value to set

        Keyword Arguments:
            suboption {string} -- Suboption name (case insensitive) (default: None)
            save {bool} -- Save on set (default: {False})
        """
        if not self.has_section(section):
            if self.config is None:
                self.config = {}
            self.config[section.upper()] = {}
        if suboption is None:
            self.config[section.upper()][key.lower()] = value
        else:
            if not self.has_option(section, key):
                self.set(section, key, {})
            self.config[section.upper()][key.lower()][
                suboption.lower()] = value
        if save:
            self.save(False)
        return self

    def is_path(self, section, key):
        """Checks if the value of an option is an existent path
        Arguments:
            section {string} -- Section name (case insensitive)
            key {string} -- Option name (case insensitive)
        Returns:
            bool -- True if is a file path and exists, False otherwise
        """
        if self.has_option(section, key):
            if os.path.exists(self.get(section, key)):
                return True
        return False

    def is_empty(self, section=None, option=None):
        """Checks if a value is empty.
        Keyword Arguments:
            section {string} -- Section name (case insensitive) (default: {None})
            option {string} -- Option name (case insensitive) (default: {None})
        Returns:
            bool -- True if is empty, null or not defined.
        """
        if section is None:
            return True
        if option is None:
            return True
        if not self.has_section(section):
            return True
        if not self.has_option(section, option):
            return True
        value = self.get(section, option)
        if value is not None and value != '':
            return False
        return False

    def save(self, backup=True):
        """Save virtual config to file
        Can save3 the configo to the file with or without backup.
        Keyword Arguments:
            backup {bool} -- Do a backup of existent file (default: {True})
        """
        if backup:
            self._save_w_backup(self.config)
        else:
            self._save_wo_backup(self.config)
        return self

    def show(self):
        '''Dump configuration file '''
        if self.exists():
            return yaml.round_trip_dump(self.config)
        return "No se ha encontrado configuracion."

    def exists(self):
        if self.config:
            return True
        return False
        #return self.config# is True

    def from_dict(self, json, save=False):
        self.config = json
        if save:
            self.save()
        return self
