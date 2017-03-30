import adsk.core
import adsk.fusion
import traceback

from .Fusion360Utilities.Fusion360Utilities import get_app_objects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase
from .Fusion360Utilities import Fusion360Utilities as futil

# Class for a Fusion 360 Command
# Place your program logic here
# Delete the line that says "pass" for any method you want to use
class BigBooleanCommand(Fusion360CommandBase):

    # Run whenever a user makes any change to a value or selection in the addin UI
    # Commands in here will be run through the Fusion processor and changes will be reflected in  Fusion graphics area
    def on_preview(self, command, inputs, args, input_values):
        pass

    # Run after the command is finished.
    # Can be used to launch another command automatically or do other clean up.
    def on_destroy(self, command, inputs, reason, input_values):
        pass

    # Run when any input is changed.
    # Can be used to check a value and then update the add-in UI accordingly
    def on_input_changed(self, command_, command_inputs, changed_input, input_values):
        pass

    # Run when the user presses OK
    # This is typically where your main program logic would go
    def on_execute(self, command, inputs, args, input_values):

        # Get a reference to all relevant application objects in a dictionary
        app_objects = get_app_objects()
        ui = app_objects['ui']

        # Get the values from the user input
        all_selections = input_values['selection_input']

        if len(all_selections) < 2:
            ui.messageBox('Not enough Bodies')

        else:

            start_index = futil.start_group()
            target_body = all_selections[0]

            # Selections are returned as a list so lets get the first one and its name
            for selection in all_selections[1:]:
                tool_bodies = [selection]
                futil.combine_feature(target_body, tool_bodies, adsk.fusion.FeatureOperations.JoinFeatureOperation)

            futil.end_group(start_index)

    # Run when the user selects your command icon from the Fusion 360 UI
    # Typically used to create and display a command dialog box
    # The following is a basic sample of a dialog UI
    def on_create(self, command, command_inputs):

        # Select the bodies
        body_select = command_inputs.addSelectionInput('selection_input', 'Select Bodies', 'Select Bodies')
        body_select.addSelectionFilter('SolidBodies')
        body_select.setSelectionLimits(2, 0)