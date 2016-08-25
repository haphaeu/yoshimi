# -*- coding: utf-8 -*-
"""

Module to tweak a simulation file that failed in dynamics - 'Simulation was unstable...'

Using yml files, reduces the time-step by a factor. First using contant time-steps, and then
switching to variable time-steps.

*** The tricky part to integrate this into the automate_batch, is that there is not way to know
if the simulation is not ready yet because of unstable dynamics or any other reason.

==> 25-Aug-2016: This has been incorporated into automate_batch repository and will be further 
    developed there, together with the dof_status script. Keeping a copy here.

Created on Thu Aug 11 14:44:22 2016

@author: rarossi
"""

import yaml


def tweak(yml, ts_start=0.01, ts_div=2.0, ts_min=0.001):
    """Tweak an OrcaFlex yml file by reducing the timestep. First constant time-step is tried,
    then variable.

    If the yml files doesn't have a General section, create one with initial
    parameters. Otherwise, assume that the General section constains the necessary keys, i.e.,
    that is has been created by this module.

    Note a potential bug here: if the input yml has a General section created by the user and
    doesn't have all the required keys used here, this function will crash.
    """

    # If no 'General' key, this is the first tweak attemp.
    # Set-up constant time-step, starting at ts_start
    if 'General' not in yml.keys():
        yml['General'] = dict()
        yml['General']['ImplicitUseVariableTimeStep'] = 'No'
        yml['General']['ImplicitConstantTimeStep'] = ts_start
        yml['General']['TargetLogSampleInterval'] = ts_start
        return True

    ts_key = ('ImplicitConstantTimeStep' if yml['General']['ImplicitUseVariableTimeStep'] == 'No'
              else 'ImplicitVariableMaxTimeStep')

    # Divide the current time-step and logging interval by 2.
    yml['General'][ts_key] /= ts_div
    yml['General']['TargetLogSampleInterval'] = yml['General'][ts_key]

    # Check if time-step is still above ts_min, if so, return yml
    if yml['General'][ts_key] > ts_min:
        return True
    # If not, and if still using cte time-step, switch to variable, set ts_start and return yml
    elif yml['General']['ImplicitUseVariableTimeStep'] == 'No':
        yml['General']['ImplicitUseVariableTimeStep'] = 'Yes'
        yml['General']['ImplicitVariableMaxTimeStep'] = ts_start
        yml['General']['TargetLogSampleInterval'] = ts_start
        del yml['General']['ImplicitConstantTimeStep']
        return True
    # End of the tweak loop. Nothing more to do
    else:
        return False  # nothing more to do


def init_yml(yml_name, yml):
    """Adds to the yml file the time-step parameters according to the model.
    (*) It is assumed that initially the yml file doesn't have a General section, so that
    it will be created in the first tweak and updated later on.
    """

    try:
        import OrcFxAPI as of
        m = of.Model(yml_name)
        variable = m['General'].ImplicitUseVariableTimeStep
        ts = (m['General'].ImplicitVariableMaxTimeStep if variable == 'Yes'
              else m['General'].ImplicitConstantTimeStep)
    except:
        # Oh, no! What to do?!
        # If orcaflex is not available, assume some things:
        variable = 'No'
        ts = 0.01

    if 'General' in yml.keys():
        # yml file already initialised - or maybe assumption (*) is wrong??
        return False
    else:
        yml['General'] = dict()

    yml['General']['ImplicitUseVariableTimeStep'] = variable
    if variable == 'Yes':
        yml['General']['ImplicitVariableMaxTimeStep'] = ts
    else:
        yml['General']['ImplicitConstantTimeStep'] = ts

    return ts


if __name__ == '__main__':

    yml_name = 'copia.yml'

    # read yml file into dictionary
    with open(yml_name, 'r') as fd:
        yml = yaml.load(fd)

    # tries to initialise the yml dictionary
    ts_start = init_yml(yml_name, yml)
    if not ts_start: ts_start = 0.01

    # tweak it!
    if tweak(yml, ts_start=ts_start/2, ts_div=2, ts_min=0.001):
        # if successfull, save back to yml file
        with open('copia.yml', 'w') as fd:
            yaml.dump(yml, fd,  default_flow_style=False)
