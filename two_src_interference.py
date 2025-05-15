from math import cos, pi, sqrt
import png

# interference of light from two point sources

#ptsrc1 = {'coords': (0,0,10**-3), 'wavelength': 400*10**-9, 'luminosity': 1, 'phase': 0}
#ptsrc2 = {'coords': (0,0,-10**-3), 'wavelength': 400*10**-9, 'luminosity': 1, 'phase': 0}

#field_dueto_ptsrc1 = lambda x,y,z: 0

'''
# defaults
wavelength = 587*10**-9 # 587 nm
phase_diff = 0 # in radians
luminosity_ratio = 1 # gives src2 relative to src1

coords1 = (-0.1,0,0)
coords2 = (0.1,0,0)
# 20 cm separation along x axis
# λ = ax/D  -->  λD/a = x
# fringe separation = 294 * 10**-8
frame_specs = {'xleft':-0.5, 'xright':0.5, 'y':1, 'ztop':0.5, 'zbottom':-0.5, 'spacing':0.001}
'''

def capture_pattern(coords1, coords2, wavelength, phase_diff, luminosity_ratio, frame_specs, bitdepth, img_name):
    
    def amplitude_at(x,y,z):
        dist1 = sqrt( (x-coords1[0])**2 + (y-coords1[1])**2 + (z-coords1[2])**2 )
        ampl1 = 1/dist1

        dist2 = sqrt( (x-coords2[0])**2 + (y-coords2[1])**2 + (z-coords2[2])**2 )
        ampl2 = luminosity_ratio/dist2

        path_diff = (dist1 - dist2)/wavelength
        resultant_ampl = sqrt( ampl1**2 + ampl2**2 + 2*ampl1*ampl2*cos(2*pi*(path_diff+phase_diff)) )
        return resultant_ampl

    """
    displacement over time, for any particular point:
    ~ due to 1 = ampl1 * sin(t * wavelength/pi*c)
    ~ due to 2 = ampl2 * sin( (t * wavelength/pi*c) - (2*pi*path_diff) )
            = ampl2*sin(t * wavelength/pi*c)*cos(2*pi*path_diff) - ampl2*cos(t * wavelength/pi*c)*sin(2*pi*path_diff)

    resultant ~ = (ampl1 + ampl2*cos(2*pi*path_diff)) * sin(t * wavelength/pi*c) - ampl2*sin(2*pi*path_diff) * cos(t * wavelength/pi*c)
    this is in the form  a sin θ + b cos θ
    resultant amplitude = sqrt[ (ampl1 + ampl2*cos(2*pi*path_diff))**2 + (ampl2*sin(2*pi*path_diff))**2 ]
                        = sqrt[ ampl1**2 + ampl2**2 + 2*ampl1*ampl2*cos(2*pi*path_diff) ]
    """

    xleft, xright, y, ztop, zbottom, spacing = frame_specs.values()
    widthpix, heightpix = int((xright-xleft)/spacing), int((ztop-zbottom)/spacing)
    if input(f'Confirm generate {widthpix}x{heightpix} image? Enter "x" to stop') == 'x':
        print('Stopped. Exiting function.')
        return

    frame = {
        'x':[xleft+(n*spacing) for n in range(widthpix)], 
        'y':y, 
        'z':[ztop-(n*spacing) for n in range(heightpix)]
        }

    ampl_array = []
    for z in frame['z']:
        row = []
        for x in frame['x']:
            row.append( amplitude_at(x, y, z) )
        ampl_array.append(row)
    max_ampl = max(max(row) for row in ampl_array)

    max_pixel = 2**(abs(int(bitdepth))) - 1
    pixel_array = [ [round(max_pixel*ampl/max_ampl) for ampl in row] for row in ampl_array ]

    img = png.from_array(pixel_array, f'L;{bitdepth}')
    img.save(f'2src_intfrnc-{img_name}.png')
    print('saved an image. Exiting function')


frame_specs = {'xleft':-0.2, 'xright':0.2, 'y':1, 'ztop':0.2, 'zbottom':-0.2, 'spacing':0.0002}

frame_specs['y'] = 0.1
capture_pattern((-0.1,0,0), (0.1,0,0), 587*10**-9, 0, 1, frame_specs, 8, 'sf01')

frame_specs['y'] = 0.05
capture_pattern((-0.1,0,0), (0.1,0,0), 587*10**-9, 0, 1, frame_specs, 8, 'sf005')

frame_specs['y'] = 0.01
capture_pattern((-0.1,0,0), (0.1,0,0), 587*10**-9, 0, 1, frame_specs, 8, 'sf001')
