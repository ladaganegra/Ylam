# -*- coding: utf-8 -*-
''' Manager for Ylam instances '''

import os
from pathlib import Path
from .ylam import Ylam
from .exceptions import *


class YlamManager(object):
	''' Gestor de configuraciones múltiples basadas en YAML con Ylam'''

	def __init__(self, verbose=False):
		self._verbose = verbose
		self._config_list_ = {}
		return

	def create(self, path):
		if path is None:
			raise FCNoFileProvidedException(path, self._verbose)
		# TODO: Allow to create a custom config file.
		pass

	def load(self, path, key=None):
		if path is None:
			raise FCNoFileProvidedException(path, self._verbose)
		if key is None:
			key = os.path.split(path)[1].split('.')[0].lower()
		if path.startswith('.') or path.startswith('..'):
			path = self.relative_dir(path)
		try:
			self._config_list_[key] = Ylam(path, self._verbose)
		except FCNoFileProvidedException as no_file:
			raise no_file  # TODO: tratar ésta excepción capturada
		except FCNoFileAccessException as no_access:
			raise no_access  # TODO: tratar ésta excepción capturada
		return self._config_list_[key]

	def save(self, key=None, make_backup=False):
		if key is not None:
			if key.lower() in self._config_list_:
				try:
					self._config_list_[key.lower()].save(make_backup)
				except FCInvalidConfException as inv_config:
					raise inv_config  # TODO: tratar ésta excepción capturada
				except FCSavingErrorException as save_config:
					raise save_config  # TODO: tratar ésta excepción capturada
		else:
			try:
				for cfg in self._config_list_.keys():
					self._config_list_[cfg].save(make_backup)
			except FCInvalidConfException as inv_config:
				raise inv_config  # TODO: tratar ésta excepción capturada
			except FCSavingErrorException as save_config:
				raise save_config  # TODO: tratar ésta excepción capturada
		return

	def get(self, key=None):
		if key is None:
			raise FCMNullKey()
		if key.lower() not in self._config_list_.keys():
			raise FCMInvalidKey(key)
		return self._config_list_[key.lower()]

	def relative_dir(self, dirstr):
		cwd = Path.cwd()
		return (cwd / dirstr).resolve()
