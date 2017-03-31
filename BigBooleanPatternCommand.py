import adsk.core
import adsk.fusion
import traceback

from .Fusion360Utilities.Fusion360Utilities import get_app_objects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase
from .Fusion360Utilities import Fusion360Utilities as futil


# Creates rectangle pattern of bodies based on vectors
def rect_body_pattern(target_component, source_body,
                      x_qty, x_distance, y_qty, y_distance, z_qty, z_distance,
                      x_axis=adsk.core.Vector3D.create(1, 0, 0),
                      y_axis=adsk.core.Vector3D.create(0, 1, 0),
                      z_axis=adsk.core.Vector3D.create(0, 0, 1)):

    move_feats = target_component.features.moveFeatures

    seed_body = source_body.copyToComponent(target_component)

    for k in range(0, z_qty):
        for j in range(0, y_qty):
            for i in range(0, x_qty):

                translation_vector = adsk.core.Vector3D.create(x_distance * i, y_distance * j, z_distance * k)

                if translation_vector.length > 0:
                    # Create a collection of entities for move
                    new_collection = adsk.core.ObjectCollection.create()

                    new_body = seed_body.copyToComponent(target_component)
                    new_collection.add(new_body)

                    transform_matrix = adsk.core.Matrix3D.create()

                    # x_axis.normalize()
                    # x_axis.scaleBy(x_distance * i)
                    # y_axis.normalize()
                    # y_axis.scaleBy(y_distance * j)
                    # z_axis.normalize()
                    # z_axis.scaleBy(z_distance * k)


                    # translation_vector.add(x_axis)
                    # translation_vector.add(y_axis)
                    # translation_vector.add(z_axis)


                    transform_matrix.translation = translation_vector

                    move_input = move_feats.createInput(new_collection, transform_matrix)
                    move_feats.add(move_input)

                    tool_bodies = [new_body]
                    futil.combine_feature(source_body, tool_bodies, adsk.fusion.FeatureOperations.JoinFeatureOperation)



# Class for a Fusion 360 Command
# Place your program logic here
# Delete the line that says "pass" for any method you want to use
class BigBooleanPatternCommand(Fusion360CommandBase):

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

        start_index = futil.start_group()
        target_body = all_selections[0]

        rect_body_pattern(target_body.parentComponent, target_body, 1, 2.54, 1, 2.54, 4, 2.54)

        futil.end_group(start_index)

    # Run when the user selects your command icon from the Fusion 360 UI
    # Typically used to create and display a command dialog box
    # The following is a basic sample of a dialog UI
    def on_create(self, command, command_inputs):

        # Select the bodies
        body_select = command_inputs.addSelectionInput('selection_input', 'Select Bodies', 'Select Bodies')
        body_select.addSelectionFilter('SolidBodies')
        body_select.setSelectionLimits(1,1)
