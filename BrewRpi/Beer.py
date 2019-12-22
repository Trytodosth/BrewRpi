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
        relevant = [s for s in self.brewing_steps if s.type == Step_types(typ)]

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
        return [s for s in self.brewing_steps if s.type == Step_types(typ)]


    ########## STARTING BREWING

    def start_substep(self, ind_step, ind_substep, force=False):
        """Implementation to match the need for step=<step>&ind=<ind>"""
        this_step = [(i, s) for (i, s) in enumerate(self.brewing_steps) if s.type == Step_types(ind_step)]
        if ind_substep >= 0 and ind_substep < len(this_step):
            return self.start_step(this_step[ind_substep])
        else:
            return self.start_step(-1)

    def start_step(self, ind, force=False):
        """Implementation to match the need for the global index"""
        if self.is_brewing and not force:
            return False, 'Some beer is already being brewed'

        if ind < 0 or ind >= len(self.brewing_steps):
            return False, 'Invalid step identifaction. Asked %i but %i steps only!' % (ind, len(self.brewing_steps))

        # New step!
        self.is_brewing = True
        self.current_step = ind
        self.step_start = datetime.datetime.now()
        return True, 'It\'s started!'

    def refresh(self, stop=False):
        """Refresh the actual state of the brewing (relay and time)"""

        if stop or not self.is_brewing or not self.current_brew_step():
            self.relay_status = False
        else:
            self.relay_status = self.current_temperature < self.current_brew_step().target_temp


    
    ########## INFO ON RUNNING BREW

    def get_running_info(self):
        if self.is_brewing:
            return str(self.current_brew_step())
        else:
            return 'Well, ready to brew when you are!'
        
    def current_brew_step(self) -> (Brew_step):    
        if self.current_step < 0 or self.current_step >= len(self.brewing_steps):
            return None
        else:
            return self.brewing_steps[self.current_step]

    def get_progress(self):
        if not self.is_brewing or not self.current_brew_step():
            return 'Either we finished, or we never started!'
        
        relevant = [s for s in self.brewing_steps if s.type == self.current_brew_step().type]

        end_time = self.step_start+datetime.timedelta(minutes=self.current_brew_step().duration)
        remaining = end_time - datetime.datetime.now()

        if remaining.total_seconds() < 0:
            self.refresh(stop=True)
            return 'The step should have been finished %0.1f minutes ago!' % (-remaining.second/60.0)

        if len(relevant) == 1:
            return '%s will be finished at %s' % (self.current_brew_step().type.name, end_time.strftime("%H:%M"))

        next = [s for (i, s) in enumerate(self.brewing_steps) if s.type == self.current_brew_step().type and i > self.current_step]

        if len(next) > 0:
            return 'This step will be finished at %s. %i more to go to finish %s' % (end_time.strftime("%H:%M"), len(next), self.current_brew_step().type.name)

        return '%s will be finished at %s' % (self.current_brew_step().type.name, end_time.strftime("%H:%M"))



