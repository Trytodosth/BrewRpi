#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import datetime
from enum import Enum

class OldBeer:
    #Beer class
    
    StepsNames = {
    -1: 'Not initialized',
    0: 'Preheating',
    1: 'Mashing',
    2: 'Boiling',
    3: 'Aromation',
    4: 'Brewing finished'}
    
    def __init__(self):
        self.brewing_steps = self.read_steps()
        
        self.current_temperature = -1
        self.relay_status = False
        
        self.current_step = -1
        self.start_time = 0
        self.is_brewing = False
        self.status = 'Ready'
        
    def getStepName(self):
        return self.StepsNames[self.current_step]
        
        
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
            return '%i steps for %s, starting with %s' % (len(relevant), Step_types(typ), str(relevant[0]))
                
    def restart(self):
        self.stop()
        self.current_step = -1
        self.start()
        self.status = 'Restarted'

    def start(self):
        if not self.is_brewing:
            self.current_step = self.current_step + 1
            self.start_time = datetime.datetime.now()
            self.is_brewing = True
            self.status = 'Started'
        
    def stop(self):
        self.is_brewing = False
        self.status = 'Stopped by YOU (or someone else)'
        
    def set_step(self, target_step):
        self.current_step = target_step
        self.start_time = datetime.datetime.now()
        self.is_brewing = True
        self.status = 'Started at a certain step'
        
        
    def get_step(self):
        if not self.is_brewing:
            return 0, 0
            
        currSteps = [s for s in self.steps if s[0] == self.current_step]
        
        # Pre heating is special
        if self.current_step == 0:
            self.status = 'Preheating to %s°C' % (currSteps[0][2])
            return currSteps[0][2], 0
            
        # Other steps
        elapsed = datetime.datetime.now() - self.start_time
        maxTime = max([s[1] for s in currSteps])
        endStepTime = self.start_time + datetime.timedelta(seconds=maxTime)
        self.status = 'Brewing: %s,\nEnd at %s' % (self.getStepName(), endStepTime.strftime("%H:%M:%S"))
        
        # Checking if next step
        if elapsed.seconds > maxTime:
            self.finish_step()
            return 0, 0
        
        # Getting the current subStep
        currSubStep = [i for i,s in enumerate(currSteps) if s[1] > elapsed.seconds]
        if currSubStep:
            currSubStep = currSubStep[0]
        else:
            currSubStep = 0
        currTemp = currSteps[currSubStep][2]
        
        print(currSteps)
        print('Elapsed: %s ' % elapsed.seconds)
        print('currTemp: %s ' % currTemp)
        
        if currSubStep >= (len(currSteps)-1): # This is the last step
            self.status = self.status + '\nNext step will be %s' % self.StepsNames[self.current_step+1]
        else:
            endSubStepTime = self.start_time + datetime.timedelta(seconds=currSteps[currSubStep][1])
            if self.current_step == 1: # Mashing
                self.status = self.status + '\nNext temperature change at %s, to %0.1f°C' % (endSubStepTime.strftime("%H:%M:%S"), currSteps[currSubStep+1][2])
            else: # Boiling or aromating
                self.status = self.status + '\nNext hop addition at %s' % (endSubStepTime.strftime("%H:%M:%S"))
        
        
        # Returning the info
        return currTemp, min(0, maxTime - elapsed.seconds)
        
        
    def finish_step(self):
        self.start_time = datetime.datetime.now()
        self.is_brewing = False
        self.status = 'Step finished'
        
        
    def init_steps(self):
        self.steps = list()
        self.preheat = list()
        self.mashing = list()
        self.boiling = list()
        self.aromation = list()
        
        # Preparing infusion
        if self.mash_steps[0].type == 'Infusion':
            self.preheat.append((0, -10, self.mash_steps[0].infuse_temp))
            self.preheat.append((0, 0, self.mash_steps[0].infuse_temp))
        
        # Mashing
        self.mashing.append((1, 0, self.mash_steps[0].step_temp))
        for mash in self.mash_steps:
            self.mashing.append((1, self.mashing[-1][1], mash.step_temp))
            self.mashing.append((1, self.mashing[-1][1] + mash.step_time, mash.step_temp))
        
        # Getting total times for hops
        #boilTime = self.mashing[-1][1]
        boilTime = 0
        hopMaxBoilTime = max([h.time for h in self.hops if h.use == 'Boil'])
        hopMaxAromaTime = max([h.time for h in self.hops if h.use == 'Aroma'])
        print('hopMaxBoilTime = %s' % hopMaxBoilTime)
        print('hopMaxAromaTime = %s' % hopMaxAromaTime)
        # Boiling step
        for hop in self.hops:
            if hop.use == 'Boil':
                self.boiling.append((2, boilTime + hopMaxBoilTime - hop.time, 95))
        self.boiling.append((2, boilTime + hopMaxBoilTime, 95))
        # Aromas step
        for hop in self.hops:
            if hop.use == 'Aroma':
                self.aromation.append((3, boilTime + hopMaxBoilTime + hopMaxAromaTime - hop.time, 20))
        self.aromation.append((3, boilTime + hopMaxBoilTime + hopMaxAromaTime, 20))
        
        self.steps = self.preheat + self.mashing + self.boiling + self.aromation
            
    def read_steps(self):
        steps = list()
        
        steps.append(Brewing_step('Preheating', 50, 0, 20))
        steps.append(Brewing_step('Saccharification', 66, 60))
        steps.append(Brewing_step('Enzyme', 75, 15))
        steps.append(Brewing_step('Boiling', 95, 40))
        steps.append(Brewing_step('Aromation', 0, 20))
        
        return steps
            
    def list_substeps(self, typ):
        for step in self.brewing_steps:
            print(step)
        return [s for s in self.brewing_steps if s.type == Step_types(typ)]
    
class Hop:
    def __init__(self, name, amount, alpha, use, time, form):
        self.name = name
        self.amout = amount
        self.alpha = alpha
        self.use = use
        self.time = time
        self.form = form

class Brewing_step:
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
            return 'Step %s: %0.1f°C during %imin' % (self.name, self.target_temp, self.duration)
        elif self.must_wait():
            return 'Step %s: Waiting to reach %0.1f°C' % (self.name, self.target_temp)
        else:
            return 'Step %s: Waiting to reach %0.1f°C' % (self.name, self.target_temp)

class Step_types(Enum):
    Preheating = 0
    Mashing = 1
    Boiling = 2
    Aromating = 3
    Cooling = 4
