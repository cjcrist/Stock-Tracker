# core.py

# standard library imports
import logging

# 3rd party imports
import requests
from requests import HTTPError

# local imports
from stock_tracker.utils.dot import Dot

LOGGER = logging.getLogger('stocktracker.core')


class Stock:
    def __init__(self, config) -> None:
        self._config = Dot(config['tracker'])
        self._response = None
        self._params = {}
        self.validated = False
        self._headers = {"Content-Type": "application/json"}

    @property
    def response(self) -> dict:
        return self._response

    def build_params(self, obj: dict, clean=False) -> None:
        """
        Build params object and sets params
        :param obj: params obj
        :param clean: Bool value
        """
        if clean:
            self._params = {}
        for k, v in obj.items():
            self._params[k] = v
        self._params['apikey'] = self._config.auth
        self._params['datatype'] = 'json'
        LOGGER.debug(f"params: {self._params}")

    def fetch(self, query: dict) -> None:
        """
        Query the API and retrieve the configured request
        """
        # Validate config file for minimum fields
        if not self.validated:
            if not self.validate_fields(query):
                raise KeyError(f"Missing required fields from query: {query}")
        elif not self._params:
            self.build_params(query)
        # Make request to API
        try:
            if not self._params:
                raise KeyError(f"Missing required params")
            response = requests.get(self._config.endpoint, params=self._params, headers=self._headers)
            response.raise_for_status()
            self._response = response.json()
        except HTTPError as e:
            LOGGER.error(str(e))
            raise HTTPError(f"There was an issue with the request: {str(e)}")

    def validate_fields(self, obj: dict, required=None) -> bool:
        """
        Validates an object with set required fields
        :param obj: a dictionary object to be validated
        :param required: Optional list of required fields
        :return: bool
        """
        fields = required if required else ["function", "symbol", "interval"]

        for k, v in obj.items():
            if isinstance(v, dict):
                self.validate_fields(v)
            if k not in fields:
                return False
        return True
