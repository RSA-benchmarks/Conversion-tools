from python.roco.vtk_tools import *
import os
from io import StringIO  # StringIO behaves like a file object
import math


def read_rootsys(fname):

    with open(fname) as f:

        content = f.readlines()

        # read relevant data
        simtime = float(content[1])

        table1 = ""  # holds: segID#    x          y          z      prev or  br#  length   surface  mass
        table2 = ""  # holds: origination time

        i = 26  # start row
        while i < len(content):
            line = content[i]
            if len(line) < 40:  # lousy stopping criteria
                break
            table1 += (line + "\n")
            table2 += (content[i + 1] + "\n")
            i += 2

        id2, x, y, z, prev, order, bn, length, surface , mass = np.loadtxt(StringIO(table1), unpack = True)
        ctime, unused = np.loadtxt(StringIO(table2), unpack = True)

        for i, id_ in enumerate(id2):
            if i != int(id_ - 1):
                print("ERROR: ids are not sequential, this is not implemented (yet)", i, id_ - 1)
                return

        # create polydata object
        nodes = np.zeros((len(x), 3))
        nodes[:, 0] = x
        nodes[:, 1] = y
        nodes[:, 2] = z
        points = vtkPoints(nodes)

        bn_ = vtk.vtkIntArray()
        order_ = vtk.vtkIntArray()
        length_ = vtk.vtkFloatArray()
        surface_ = vtk.vtkFloatArray()
        radius_ = vtk.vtkFloatArray()
        mass_ = vtk.vtkFloatArray()
        time_ = vtk.vtkFloatArray()
        age_ = vtk.vtkFloatArray()

        bn_.SetName("Branch number")
        order_.SetName("Order")
        length_.SetName("Length")
        radius_.SetName("Radius")
        mass_.SetName("Mass")
        time_.SetName("Creation Time")
        age_.SetName("Age")
        surface_.SetName("Surface")

        segs = []
        for i in range(0, len(id2)):
            i_ = int(id2[i] - 1)  # lets start at 0
            time_.InsertNextValue(ctime[i_])
            age_.InsertNextValue(simtime - ctime[i_])
            if prev[i] != 0:  # Cellata
                segs.append((int(prev[i] - 1), i_))
                order_.InsertNextValue(int(order[i_]))
                bn_.InsertNextValue(int(bn[i_]))
                length_.InsertNextValue(length[i_])
                surface_.InsertNextValue(surface[i_])
                radius_.InsertNextValue(surface[i_] / length[i_] / (2 * math.pi))
                mass_.InsertNextValue(mass[i_])

        segs = np.array(segs, dtype = int)  # copy list into numpy array
        cells = vtkCells(segs)

        pd = vtk.vtkPolyData()
        pd.SetPoints(points)
        pd.SetLines(cells)
        pd.GetPointData().AddArray(time_)
        pd.GetPointData().AddArray(age_)
        pd.GetCellData().AddArray(bn_)
        pd.GetCellData().AddArray(order_)
        pd.GetCellData().AddArray(surface_)
        pd.GetCellData().AddArray(mass_)
        pd.GetCellData().AddArray(radius_)
        pd.GetCellData().AddArray(length_)

    return pd

