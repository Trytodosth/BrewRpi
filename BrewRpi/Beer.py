from BrewRpi.Brew_step import *
import datetime

class Beer(object):
    """Beer class containing the different steps information"""

    def __init__(self):
        self.brewing_steps = self.read_steps()
        
        # Sensors information
        self.current_temperature = -1
        self.relay_status = False

        # The running step variables (nothing running at initiation)
        self.is_brewing = False
        self.current_step = -1
        self.step_start = datetime.datetime.now()
            
        
    def get_info_step(self, typ):
        print(len(self.brewing_steps))
        print([s.type for s in self.brewing_steps])
        relevant = [s for s in self.brewing_steps if s.type == Step_types(typ)]
        print(relevant)
        
        for step in self.brewing_steps:
            print(step.type)
            print(step)
            
        if not relevant:
            return 'Not necessary for this beer!'
        
        if len(relevant) == 1:
            return str(relevant[0])
        else:
            return '%i steps for %s, starting with %s' % (len(relevant), Step_types(typ).name, str(relevant[0]))
        
    def read_steps(self):
        steps = list()
        
        steps.append(Brew_step('Preheating', 50, 0, 20))
        steps.append(Brew_step('Saccharification', 66, 60))
        steps.append(Brew_step('Enzyme', 75, 15))
        steps.append(Brew_step('Boiling', 95, 40))
        steps.append(Brew_step('Aromation', 0, 20))
        
        return steps
            
    def list_substeps(self, typ):
        for step in self.brewing_steps:
            print(step)
        return [s for s in self.brewing_steps if s.type == Step_types(typ)]

    def start_step(self, ind, force=False):
        if self.is_brewing and not force:
            return 'Some beer is already being brewed'

        if ind < 0 or ind >= len(self.brewing_steps):
            return 'Invalid step identifaction. Asked %i but %i steps only!' %  (ind, len(self.brewing_steps))

        # New step!
        self.is_brewing = True
        self.current_step = ind
        self.step_start = datetime.datetime.now()

    def get_running_info(self):
        if self.is_brewing:
            return str(self.current_brew_step())
        else:
            return 'Well, ready to brew when you are!'
        
    def current_brew_step(self):    
        if ind < 0 or ind >= len(self.brewing_steps):
            return self.brewing_steps[self.current_step]
        else:
            return None

    def get_progress(self):
        if not self.is_brewing:
            return 'Either we finished, or we never started!'
        
        relevant = [s for s in self.brewing_steps if s.type == Step_types(typ)]

        end_time = self.step_start+self.current_step()
        remaining = end_time - datetime.datetime.now()

        if remaining < 0:
            return 'The step should have been finished %0.1f minutes ago!' % (-remaining.second/60.0)

        if len(relevant) == 1:
            return '%s will be finished at %s' % (Step_types(typ).name, end_time.strftime("%H:%M"))

        next = [s for (i, s) in enumerate(self.brewing_steps) if s.type == Step_types(typ) and i > self.current_step]

        if len(next) > 0:
            return 'This step will be finished at %s. %i more to go to finish %s' % (end_time.strftime("%H:%M"), len(next), Step_types(typ).name)

        return '%s will be finished at %s' % (Step_types(typ).name, end_time.strftime("%H:%M"))



