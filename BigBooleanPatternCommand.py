import adsk.core
import adsk.fusion
import traceback

from .Fusion360Utilities.Fusion360Utilities import get_app_objects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase
from .Fusion360Utilities import Fusion360Utilities as futil


def copy_in_direction(translation_vector, seed_body, target_component, source_body, move_feats):

    new_collection = adsk.core.ObjectCollection.create()

    new_body = seed_body.copyToComponent(target_component)
    new_collection.add(new_body)

    transform_matrix = adsk.core.Matrix3D.create()

    transform_matrix.translation = translation_vector

    move_input = move_feats.createInput(new_collection, transform_matrix)
    move_feats.add(move_input)

    tool_bodies = [new_body]
    futil.combine_feature(source_body, tool_bodies, adsk.fusion.FeatureOperations.JoinFeatureOperation)


# Creates rectangle pattern of bodies based on vectors
def rect_body_pattern(source_body,
                      x_qty, x_distance, y_qty, y_distance, z_qty, z_distance,
                      x_axis=adsk.core.Vector3D.create(1, 0, 0),
                      y_axis=adsk.core.Vector3D.create(0, 1, 0),
                      z_axis=adsk.core.Vector3D.create(0, 0, 1)):

    app_objects = futil.get_app_objects()

    # target_occurrence = target_body.assemblyContext

    target_component = app_objects['design'].activeComponent

    move_feats = target_component.features.moveFeatures

    seed_body = source_body.copyToComponent(target_component)

    for i in range(0, x_qty):

        translation_vector = adsk.core.Vector3D.create(x_distance * i, 0, 0)

        if translation_vector.length > 0:
            # Create a collection of entities for move
            copy_in_direction(translation_vector, seed_body, target_component, source_body, move_feats)

    seed_body = source_body

    for j in range(0, y_qty):

        translation_vector = adsk.core.Vector3D.create(0, y_distance * j, 0)

        if translation_vector.length > 0:
            # Create a collection of entities for move
            copy_in_direction(translation_vector, seed_body, target_component, source_body, move_feats)

    seed_body = source_body

    for k in range(0, z_qty):
        translation_vector = adsk.core.Vector3D.create(0, 0, z_distance * k)

        if translation_vector.length > 0:
            # Create a collection of entities for move
            copy_in_direction(translation_vector, seed_body, target_component, source_body, move_feats)


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
        source_body = all_selections[0]

        # all_selections = input_values['target_input']
        # target_body = all_selections[0]

        start_index = futil.start_group()

        rect_body_pattern(source_body,
                          input_values['x_qty'], input_values['x_distance'],
                          input_values['y_qty'], input_values['y_distance'],
                          input_values['z_qty'], input_values['z_distance'])

        futil.end_group(start_index)

    # Run when the user selects your command icon from the Fusion 360 UI
    # Typically used to create and display a command dialog box
    # The following is a basic sample of a dialog UI
    def on_create(self, command, command_inputs):

        # Select the bodies
        body_select = command_inputs.addSelectionInput('selection_input', 'Select Source Body', 'Select Body')
        body_select.addSelectionFilter('SolidBodies')
        body_select.setSelectionLimits(1,1)

        # # Select the bodies
        # body_select = command_inputs.addSelectionInput('target_input', 'Select Target Body', 'Select Body')
        # body_select.addSelectionFilter('SolidBodies')
        # body_select.setSelectionLimits(1, 1)

        # Create a default value using a string
        default_value = adsk.core.ValueInput.createByString('1.0 in')

        # Create a few inputs in the UI
        command_inputs.addValueInput('x_distance', 'X Spacing Distance', 'in', default_value)
        command_inputs.addIntegerSpinnerCommandInput('x_qty', 'X Quantity', 0, 1000, 1, 1)

        command_inputs.addValueInput('y_distance', 'Y Spacing Distance', 'in', default_value)
        command_inputs.addIntegerSpinnerCommandInput('y_qty', 'Y Quantity', 0, 1000, 1, 1)

        command_inputs.addValueInput('z_distance', 'Z Spacing Distance', 'in', default_value)
        command_inputs.addIntegerSpinnerCommandInput('z_qty', 'Z Quantity', 0, 1000, 1, 1)



