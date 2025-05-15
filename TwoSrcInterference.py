import png
from math import pi, cos, sqrt
e0 = 8.854 * 10**-12
c = 3.00 * 10**8

""" class Src:
    amplitude_const = 1/sqrt(2*pi*e0*c)
    def __init__(self, x,y,z, frequency, phase, luminosity):
        self.x, self.y, self.z, = x,y,z
        self.frequency = frequency
        self.phase = phase
        self.luminosity = luminosity

    def distance_to(self,x,y,z):
        return sqrt( (self.x-x)**2 + (self.y-y)**2 + (self.z-z)**2 )
    
    def amplitude_at(self, x,y,z):
        return sqrt(self.luminosity) / self.distance_to(x,y,z) """

class InterferenceSetup:
    srcs = {}
    def __init__(self, wavelength):
        self.wave = {'length':wavelength, 'frequency':c/wavelength, 'period':wavelength/c}

    def add_src(self, name, x,y,z, phase, luminosity):
        self.srcs[name] = {'x':x,'y':y,'z':z, 'phase':phase, 'luminosity':luminosity}