'''
Created on Nov 2, 2011

@author: aradi
'''
import numpy as np

def miller_to_normal(latvecs, miller_indices):
    '''Calculates the normal form of a plane defined by Miller indices'''
    reclatvecs = np.array([ np.cross(latvecs[(ii+1)%3], latvecs[(ii+2)%3]) 
        for ii in range(3) ])
    normals = np.dot(miller_indices, reclatvecs)
    return normals
