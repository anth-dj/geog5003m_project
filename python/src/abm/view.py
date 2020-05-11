#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
View module

Provides classes used to display agent-based models.

@author: Anthony Jarrett
"""

import tkinter
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

from . import logger


# Set the plot color map
COLOR_MAP = cm.get_cmap('magma', 255)
COLOR_MAP.set_under(color='white')  

class View():

    def __init__(self, controller):

        logger.log("Instantiating a View.")
        
        # Set the controller back-reference
        self.controller = controller

        # Prepare the visualization figure
        matplotlib.pyplot.ioff()
        self.fig = matplotlib.pyplot.figure(figsize=(7, 7))
        ax = self.fig.add_axes([0, 0, 1, 1])
        ax.set_autoscale_on(False)

        # Create GUI window
        root = tkinter.Tk()
        root.wm_title("Bacterial Bomb Agent-Based Model")
        root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Create menu
        menubar = tkinter.Menu(root)
        root.config(menu=menubar)
        model_menu = tkinter.Menu(menubar)
        menubar.add_cascade(label="Model", menu=model_menu)
        model_menu.add_command(label="Run model", command=self._on_run_model)
        model_menu.add_command(label="Exit", command=self._on_exit)
        
        
        # Add parameter inputs
        parameters_frame = tkinter.Frame(root)
    
        self.north_percentage_entry = self._insert_labelled_entry(
            parameters_frame, "North wind direction %:", "")

        self.east_percentage_entry = self._insert_labelled_entry(
            parameters_frame, "East wind direction %:", "",
            1, 0, 1, 1)

        self.south_percentage_entry = self._insert_labelled_entry(
            parameters_frame, "South wind direction %:", "",
            2, 0, 2, 1)

        self.west_percentage_entry = self._insert_labelled_entry(
            parameters_frame, "West wind direction %:", "",
            3, 0, 3, 1)

        self.up_percentage_entry = self._insert_labelled_entry(
            parameters_frame, "Upward wind direction %",
            "",
            0, 2, 0, 3)

        self.down_percentage_entry = self._insert_labelled_entry(
            parameters_frame, "Downward wind direction %:",
            "",
            1, 2, 1, 3)

        self.no_change_percentage_entry = self._insert_labelled_entry(
            parameters_frame, "No height change %:",
            "",
            2, 2, 2, 3)

        self.num_of_particles_entry = self._insert_labelled_entry(
            parameters_frame, "Number of particles:",
            "",
            3, 2, 3, 3)
        
        # Add a button to update parameters
        load_button = tkinter.Button(parameters_frame, text="Update Model",
                                     command=self._on_load_parameters)
        load_button.grid(row=0, column=4, padx=12, rowspan=2)

        
        # Add the parameters frame to the GUI
        parameters_frame.pack(side=tkinter.TOP, fill=tkinter.X, padx=8, pady=8)

        # Store a reference to the root view
        self.root = root
        
        # Add canvas for rendering
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.fig, 
                                                                     master=root)
        canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.canvas = canvas


    def show_error(self, message):
        """
        Display error message

        Parameters
        ----------
        message : str
            Error message to be displayed.

        Returns
        -------
        None.

        """
        
        tkinter.messagebox.showinfo("Error", message)


    def _on_close(self):
        
        logger.log("Shutting down program.")
        
        # Close all open figures
        matplotlib.pyplot.close('all')
        
        # Quit the GUI program and free up memory
        self.root.quit()
        self.root.destroy()


    def _on_run_model(self):
        self.controller.run_model()

    def _on_exit(self):
        self._on_close()

    def _on_load_parameters(self):
        self.controller.load_parameters()

    def display(self, environment, bomb_position):
        """
        Display the current state of the given model

        Parameters
        ----------
        model : Model
            The model to be rendered in the GUI.

        Returns
        -------
        None.

        """
                
        # Reset the current view data
        self.fig.clear()
        matplotlib.pyplot.xlim(0, environment.width)
        matplotlib.pyplot.ylim(0, environment.height)
        
        # Render the environment
        matplotlib.pyplot.imshow(environment.plane, cmap=COLOR_MAP, vmin=0.0000001)

        # Render the bomb location
        matplotlib.pyplot.scatter(bomb_position.x, bomb_position.y, color='red')


    def _insert_labelled_entry(self, row, label, default_value="", label_row=0, 
                               label_column=0, entry_row=0, entry_column=1):
        """
        Return an entry field widget with the given label and default value.

        Parameters
        ----------
        row : tkinter.Frame
            Frame widget to attach to.
        label : str
            Entry field text label.
        default_value : str
            Default value for the entry field.
        label_row : int, optional
            Row to insert the label. The default is 0.
        label_column : int, optional
            Column to insert the label. The default is 0.
        entry_row : int, optional
            Row to insert the entry field. The default is 0.
        entry_column : int, optional
            Column to insert the entry field. The default is 1.

        Returns
        -------
        entry : tkinter.Entry
            A GUI entry component.

        """

        # Create the label element
        label = tkinter.Label(row, text=label)
        label.grid(row=label_row, column=label_column)
        
        # Create the entry element
        entry = tkinter.Entry(row)
        entry.grid(row=entry_row, column=entry_column)
        
        # Set the default value
        entry.insert(0, str(default_value))
        
        return entry

    def _set_entry_field_value(self, entry_field, value):
        """
        Set the entry field text to the given value

        Parameters
        ----------
        entry_field : tkinter.Entry
            The entry field to modify.
        value : str
            The value to set in the entry field.

        Returns
        -------
        None.

        """
        
        entry_field.delete(0, tkinter.END)
        entry_field.insert(0, value)
