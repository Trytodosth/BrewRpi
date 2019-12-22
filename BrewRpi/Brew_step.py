from enum import Enum


class Brew_step(object):
    """Class of a brewing step, including heating or not, and tracking temperature"""

    def __init__(self, name, temp, dur, param=0):
        self.name = name
        if dur > 0:
            if temp > 90:
                self.type = Step_types.Boiling
            elif temp > 0:
                self.type = Step_types.Mashing
            else:
                self.type = Step_types.Aromating
        else:
            if temp > 40:
                self.type = Step_types.Preheating
            else:
                self.type = Step_types.Cooling
                
        self.target_temp = temp
        self.duration = dur

    def must_heat(self):
        return self.type == Step_types.Mashing or self.type == Step_types.Boiling

    def must_wait(self):
        return self.type == Step_types.Aromating

    
    def __str__(self):
        if self.must_heat():
            return '%s: %0.1f°C during %imin' % (self.name, self.target_temp, self.duration)
        elif self.must_wait():
            return '%s: Waiting to reach %0.1f°C' % (self.name, self.target_temp)
        else:
            return '%s: Waiting to reach %0.1f°C' % (self.name, self.target_temp)

        
class Step_types(Enum):
    Preheating = 0
    Mashing = 1
    Boiling = 2
    Aromating = 3
    Cooling = 4
