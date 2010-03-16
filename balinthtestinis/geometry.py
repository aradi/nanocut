# -*- coding: iso-8859-2 -*-
############################################################################
#
# NEBMANIA, General minimum energy path and saddle point searching tool.
# Copyright (C) 2005, Bálint Aradi (inidos@prophy.net)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110, USA
#
############################################################################
#
# Geometry related routines
#
############################################################################
import re
import Numeric as num


# Starting line of a gen formatted structure
PAT_GENS_BEGIN = re.compile(r"^[ \t]*\d+[ \t]+(?:s|S|c|C)", re.MULTILINE)
PAT_XYZS_BEGIN = re.compile(r"^[ \t]*\d+[ \t]*$", re.MULTILINE)



# Simple minded class for containing geometry information. It's variables
# are not protected by seters/geters, so consistency of the data inside
# is not guaranteed
class Geometry(object):
  """Only a data container with constructor for storing a geometry"""


  def __init__(self, species, indexes, coords, latVecs=None):
    """Constructs a geometry object.
  species -- Name of the species present in the structure.
  indexes -- For each atom the sequence number of its specie.
  coords  -- Coordinates (nAtom, 3).
  latVecs -- Translation vectors, if structure is periodic.
"""

    self.species = species[:]
    self.nSpecie = len(self.species)
    self.indexes = num.array(indexes)
    self.nAtom = len(indexes)
    self.coords = num.array(coords, num.Float)
    if (self.coords.shape != (self.nAtom, 3)):
      raise "Bad coordinate array"
    if not latVecs:
      self.periodic = False
      self.latVecs = None
    else:
      self.latVecs = num.array(latVecs, num.Float)
      if self.latVecs.shape != (3, 3):
        raise "Bad cell vectors"
      self.periodic = True


  def collapse(self):
    """If types with similar names are specified, it collapes them together"""

    double = [ False, ] * len(self.species)
    newSpecies = []
    for iSp1 in range(len(self.species)):
      if double[iSp1]:
        continue
      sp1 = self.species[iSp1]
      newSpecies.append(sp1)
      for iSp2 in range(iSp1, len(self.species)):
        if self.species[iSp2] == sp1:
          double[iSp2] = True
          self.indexes = num.where(num.equal(self.indexes, iSp2),
                                   len(newSpecies)-1, self.indexes)
    self.species = newSpecies
    self.nSpecie = len(self.species)
    

#
# Converting routines
#

def gen2geo(input):
  """Converts the content of a gen file into a geometry object
  input  -- Content of a gen file as a string.
  return -- Initialized Geometry object.
"""

  lines = input.split("\n")
  words = lines[0].split()
  nAtom = int(words[0])
  periodic = (words[1] == "S") or (words[1] == "F")
  if periodic:
    fractional = words[1] == "F"
  species = lines[1].split()
  indexes = []
  coords = []
  for line in lines[2:2+nAtom]:
    words = line.split()
    indexes.append(int(words[1])-1)
    coords.append([ float(ww) for ww in words[2:5]])
  
  if periodic:
    latVecs = []
    for line in lines[2+nAtom+1:2+nAtom+4]:
      words = line.split()
      latVecs.append([ float(ww) for ww in words[0:3]])
    if fractional:
      coords = num.dot(coords, latVecs)

  if periodic:
    return Geometry(species, indexes, coords, latVecs)
  else:
    return Geometry(species, indexes, coords)



def xyz2geo(input, latVecs=None):
  """Converts the content of an xyz file into a geometry object
  input -- Content of the xyz file as string
  latVecs -- Text representation of the lattice vectors (optional)
  return -- Initialised Geometry object
  """

  lines = input.strip().split("\n")
  words = lines[0].split()
  nAtom = int(words[0])
  coords = num.zeros((nAtom, 3), num.Float)
  indexes = num.zeros((nAtom,), num.Int)
  species = []
  for ii in range(nAtom):
    words = lines[2+ii].split()
    specie = words[0].lower()
    specie = specie[0].upper() + specie[1:]
    try:
      ind = species.index(specie)
    except ValueError:
      species.append(specie)
      ind = len(species) - 1
    indexes[ii] = ind
    coords[ii][0] = float(words[1])
    coords[ii][1] = float(words[2])
    coords[ii][2] = float(words[3])
  if latVecs == None:
    ii += 2 + 1
  else:
    lines = latVecs.strip().split("\n")
    ii = 0
  if ii + 3 <= len(lines):
    periodic = True
    latVecs = num.zeros((3, 3), num.Float)
    for jj in range(3):
      words = lines[ii+jj].split()
      latVecs[jj] = [ float(s) for s in words ]
  else:
    periodic = False
  if periodic:
    return Geometry(species, indexes, coords, latVecs)
  else:
    return Geometry(species, indexes, coords)
    


def geo2gen(geo):
  """Converts a geometry object to a gen string
  geo    -- Geometry object.
  return -- String containing the geometry in gen format.
"""

  result = []
  if geo.periodic:
    mode = "S"
  else:
    mode = "C"
  result.append("%5d %2s" % (geo.nAtom, mode))
  result.append(("%2s "*geo.nSpecie) % tuple(geo.species))

  for ii in range(geo.nAtom):
    result.append("%5d %3d %16.8f %16.8f %16.8f"
                  % (ii+1, geo.indexes[ii]+1, geo.coords[ii][0],
                     geo.coords[ii][1], geo.coords[ii][2]))
  if geo.periodic:
    result.append("%16.8f %16.8f %16.8f" % (0.0, 0.0, 0.0))
    for latv in geo.latVecs:
      result.append("%16.8f %16.8f %16.8f" % tuple(latv))

  return "\n".join(result)



def geo2xyz(geo, printLatVec=False):
  """Converts a geometry object to xyz format
  geo    -- Geometry object
  printLatVec -- If lattice vectors should be appended (default: False)
  return -- String containing the geometry in xyz format
"""

  result = []
  result.append("%5d" % geo.nAtom)
  result.append(("%2s "*geo.nSpecie) % tuple(geo.species))
  for ii in range(geo.nAtom):
    result.append(" %-3s %16.8f %16.8f %16.8f" % (geo.species[geo.indexes[ii]],
                                                  geo.coords[ii][0],
                                                  geo.coords[ii][1],
                                                  geo.coords[ii][2]))
  if geo.periodic and printLatVec:
    #result.append("%16.8f %16.8f %16.8f" % (0.0, 0.0, 0.0))
    for latv in geo.latVecs:
      result.append("%16.8f %16.8f %16.8f" % tuple(latv))

  return "\n".join(result)




def geos2gens(geos):
  """Converts a list of Geometry objects to string containing the geometries
in gen format.
  geos   -- List of Geometry objects.
  return -- String containing the geometries in gen format, separated by
    blank lines.
"""

  result = []
  for geo in geos:
    result.append(geo2gen(geo))
  return "\n\n".join(result)



def geos2xyzs(xyzs):
  """Converts a list of Geometry objects to string containing the geometries
in xyz format.
  geos   -- List of Geometry objects.
  return -- String containing the geometries in xyz format separated by newline
"""

  result = [ geo2xyz(geo) for geo in geos ]
  return "\n".join(result)




def gens2geos(gens):
  """Converts a string containing gen-formatted structures to a list of
Geometry objects.
  gens   -- String containing the gen-formatted structures. The structures
    may or may not be separated by empty lines.
  return -- List of Geometry objects.
"""

  # Split string by searching for the characteristic 1st line of the gen format.
  result = []
  start = 0
  match = PAT_GENS_BEGIN.search(gens)
  while match:
    prevStart = match.start()
    match = PAT_GENS_BEGIN.search(gens, pos=match.end())
    if match:
      gen = gens[prevStart:match.start()]
    else:
      gen = gens[prevStart:]
    result.append(gen2geo(gen))

  return result



def xyzs2geos(xyzs):
  """Converts a string containing xyz-formatted structures to a list of
Geometry objects.
  xyzs   -- String containing the xyz-formatted structures. The structures
    may or may not be separated by empty lines.
  return -- List of Geometry objects.
"""

  # Split string by searching for the characteristic 1st line of the gen format.
  result = []
  start = 0
  match = PAT_XYZS_BEGIN.search(xyzs)
  while match:
    prevStart = match.start()
    match = PAT_XYZS_BEGIN.search(xyzs, pos=match.end())
    if match:
      xyz = xyzs[prevStart:match.start()]
    else:
      xyz = xyzs[prevStart:]
    result.append(xyz2geo(xyz))

  return result

