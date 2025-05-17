import png
# from Geometry3D import *
from math import sqrt, sin, cos, asin, acos, pi
e0 = 8.854 * 10**-12 # permittivity of free space
c = 3.00 * 10**8 # speed of light in a vacuum


""" def arctrig(cosv, sinv):
    "returns the angle with the sin and cos values passed, or None if no such angle"
    snip = lambda theta: round(theta, 8) 
    # we want sets of solutions in [0, 2*pi]
    # range of math.asin is [-pi/2, pi/2]
    # range of math.acos is [0, pi]
    asinset = { snip((asin(sinv)+2*pi)%(2*pi)), snip(pi-asin(sinv)) }
    acosset = { snip(acos(cosv)), snip(2*pi - acos(cosv)) }
    
    commons = asinset.intersection(acosset)
    if len(commons) == 1:
        return commons.pop()
    return None """


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
        return amplitude_const * sqrt(self.luminosity) / self.distance_to(x,y,z) """

class InterferenceSetup:
    amplitude_const = 1/sqrt(2*pi*e0*c)
    def __init__(self, wavelength):
        "wavelength in metres - all sources added will share this"
        self.wavelength = wavelength
        self.srcs = {}

    def add_src(self, name, position, phase, luminosity):
        "phase as an angle in radians, between 0 and 2π \n\n luminosity in Watts"
        self.srcs[name] = {'x':position[0],'y':position[1],'z':position[2]}
        self.srcs[name]['phase'] = phase%(2*pi)
        self.srcs[name]['luminosity'] = luminosity
    
    def src_influence_at(self, src_name, point):
        src = self.srcs[src_name]
        x,y,z = point
        distance = sqrt( (src['x']-x)**2 + (src['y']-y)**2 + (src['z']-z)**2 )
        amplitude = self.amplitude_const * sqrt(src['luminosity'])/distance
        phase = 2*pi*((distance/self.wavelength)%1) + src['phase']
        return {'amplitude':amplitude, 'phase':phase%(2*pi)}

    def amplitude_at(self, point):
        oscillations = [
            self.src_influence_at(src_name, point) for src_name in self.srcs
        ]
        # add up sinusoids
        resultant_amplitude = sqrt(
            sum([ osc['amplitude']*sin(osc['phase']) for osc in oscillations ])**2 +
            sum([ osc['amplitude']*cos(osc['phase']) for osc in oscillations ])**2
        )
        return resultant_amplitude
        """ resultant_phase = arctrig(
            sum([ osc['amplitude']*cos(osc['phase']) for osc in oscillations ])/resultant_amplitude,
            sum([ osc['amplitude']*sin(osc['phase']) for osc in oscillations ])/resultant_amplitude
        ) """
    
    def capture_frame(self, topleftcorner, bottomrightcorner, horizontal_vector, spacing, img_name, bitdepth):
        """topleftcorner: The point that should appear at the top-left of the frame \n
        bottomrightcorner: The point that should appear at the bottom-right of the frame \n
        horizontal_vector: A vector giving the direction of the rows of the frame \n
        spacing: Distance between sampling points \n
        All coordinates and distances will be interepreted in metres
        """
        #args: top_left_corner, horizont_vector, widthpix, vertic_vector, heightpix
        # input invalid if horizont and vertic vectors are not orthogonal
        #args: topleftcorner, normal and horizontal vectors, widthpix and heightpix
        # too much manipulation
        #args: topleftcorner, bottomrightcorner, horizontal vector, (widthpix, heightpix | spacing)

        absolute = lambda nums: sqrt(sum(num**2 for num in nums))
        scale = lambda seq, factor: tuple(_*factor for _ in seq)
        add = lambda seq1, seq2: tuple( seq1[i]+seq2[i] for i in range(len(seq1)) )
        sub = lambda seq1, seq2: tuple( seq1[i]-seq2[i] for i in range(len(seq1)) )
        mul = lambda seq1, seq2: tuple( seq1[i]*seq2[i] for i in range(len(seq1)) )

        diagonal = sub(bottomrightcorner, topleftcorner)
        h_dot_d = mul(diagonal, horizontal_vector)
        horizontal = scale(horizontal_vector, sum(h_dot_d)/(absolute(horizontal_vector))**2)
        vertical = sub(bottomrightcorner,add(topleftcorner, horizontal))

        width, height = absolute(horizontal), absolute(vertical)
        ncols, nrows = int(width/spacing), int(height/spacing)
        col_spacing, row_spacing = scale(horizontal, 1/ncols), scale(vertical, 1/nrows)

        if input(f'Confirm generate {ncols}x{nrows} image? Enter "x" to stop: ') == 'x':
            print('Stopped. Exiting function.')
            return

        frame_point = lambda rown, coln: add(topleftcorner, add(scale(row_spacing,rown), scale(col_spacing,coln)))
        amplitudes_array = [
            [self.amplitude_at(frame_point(rown, coln)) for coln in range(ncols)] for rown in range(nrows)
        ]
        max_ampl = max(max(row) for row in amplitudes_array)
        print(max_ampl)
        max_pixel = 2**(abs(int(bitdepth))) - 1
        pixel_array = [
            [round(max_pixel*ampl/max_ampl) for ampl in row] for row in amplitudes_array
        ]
        png.from_array(pixel_array, f'L;{bitdepth}').save(f'Interference-{img_name}.png')
        print(f'Saved image Interference-{img_name}.png')    


if __name__ == '__main__':
    doubleslitgreen = InterferenceSetup(587*10**-9)
    doubleslitgreen.add_src('A', (-0.01,0,0), 0, 1)
    doubleslitgreen.add_src('B', (0.01,0,0), pi, 1)
    doubleslitgreen.capture_frame((-0.5,1,0.5),(0.5,1,-0.5), (1,0,0), 0.001, 'eqn_verif', 8)