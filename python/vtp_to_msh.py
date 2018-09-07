from vtk_tools import read_polydata, write_msh

def vtp_to_msh(name_vtp,name_msh):
    """ Converts an vtp file to a Gmsh (.msh) file
    """
    pd = read_polydata(name_vtp)
    write_msh(name_msh,pd)

if __name__ == "__main__":    
    vtp_to_msh("test.vtp","test.dgf")
    print("done.")
