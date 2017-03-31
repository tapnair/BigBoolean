#Author-Patrick Rainsberry
#Description-Different Approach to a many body boolean operation

# Importing sample Fusion Command
# Could import multiple Command definitions here
from .BigBooleanCommand import BigBooleanCommand
from .BigBooleanPatternCommand import BigBooleanPatternCommand

commands = []
command_definitions = []

# Define parameters for 1st command
cmd = {
    'cmd_name': 'Big Boolean',
    'cmd_description': 'Different Approach to creating Booleans of many bodies',
    'cmd_id': 'cmdID_BigBooleanCommand',
    'cmd_resources': './resources',
    'workspace': 'FusionSolidEnvironment',
    'toolbar_panel_id': 'SolidScriptsAddinsPanel',
    'class': BigBooleanCommand
}
command_definitions.append(cmd)


# Define parameters for 1st command
cmd = {
    'cmd_name': 'Big Boolean Pattern',
    'cmd_description': 'Different Approach to creating Booleans of many bodies',
    'cmd_id': 'cmdID_BigBooleanPatternCommand',
    'cmd_resources': './resources',
    'workspace': 'FusionSolidEnvironment',
    'toolbar_panel_id': 'SolidScriptsAddinsPanel',
    'class': BigBooleanPatternCommand
}
command_definitions.append(cmd)

# Set to True to display various useful messages when debugging your app
debug = False


# Don't change anything below here:
for cmd_def in command_definitions:
    command = cmd_def['class'](cmd_def, debug)
    commands.append(command)


def run(context):
    for run_command in commands:
        run_command.on_run()


def stop(context):
    for stop_command in commands:
        stop_command.on_stop()
