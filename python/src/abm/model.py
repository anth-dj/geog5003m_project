#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model module

Provides classes used to represent agent-based models.

@author: Anthony Jarrett
"""

import os

from . import agentframework, logger

DEFAULT_NUM_OF_PARTICLES = 5000
DEFAULT_BOMB_LOCATION_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + \
    os.sep + '../wind.raster'

class Model():

    def __init__(self, parameters=None):

        # If parameters are not provided, use default values
        if parameters is None:
            parameters = self._get_default_parameters()

        # Set the model parameters
        self._parameters = parameters

    def __str__(self):
        return \
"""=======================================
                Model
---------------------------------------

{}
=======================================""".format(self._parameters)

    def _get_default_parameters(self):

        # Create default wind settings
        wind_settings = agentframework.WindSettings()

        # Load environment
        environment = agentframework.Environment.read_from_file(DEFAULT_BOMB_LOCATION_FILE_PATH)

        # Set default number of particles
        num_of_particles = DEFAULT_NUM_OF_PARTICLES

        # Return parameters
        return Parameters(wind_settings, environment, num_of_particles)


class Parameters():

    def __init__(self, wind_settings, environment,
        num_of_particles=DEFAULT_NUM_OF_PARTICLES):
        self._wind_settings = wind_settings
        self._environment = environment
        self._num_of_particles = num_of_particles

    def __str__(self):
        return \
"""Wind Settings
{}

Environment
{}

Number of particles
{}
""".format(
    self._wind_settings,
    self._environment,
    self.num_of_particles
)

    @property
    def wind_settings(self):
        """
        Get the wind settings.
        """
        return self._wind_settings

    @wind_settings.setter
    def wind_settings(self, value):
        """
        Set the wind settings.
        """
        self._wind_settings = value

    @wind_settings.deleter
    def wind_settings(self):
        """
        Delete the wind settings property.
        """
        del self._wind_settings

    @property
    def bomb_location(self):
        """
        Get the bomb location.
        """
        return self._bomb_location

    @bomb_location.setter
    def bomb_location(self, value):
        """
        Set the bomb location.
        """
        self._bomb_location = value

    @bomb_location.deleter
    def bomb_location(self):
        """
        Delete the bomb location property.
        """
        del self._bomb_location

    @property
    def num_of_particles(self):
        """
        Get the number of particles.
        """
        return self._num_of_particles
    
    @num_of_particles.setter
    def num_of_particles(self, value):
        """
        Set the number of particles.
        """
        self._num_of_particles = value
    
    @num_of_particles.deleter
    def num_of_particles(self):
        """
        Delete the number of particles property.
        """
        del self._num_of_particles


