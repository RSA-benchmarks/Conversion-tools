from vtk_tools import read_polydata, write_dgf

def vtp_to_msh(name_vtp,name_dgf):
    """ Converts an vtp file to a Dunde Grid File (.dgf)
    """
    pd = read_polydata(name_vtp)
    write_dgf(name_dgf,pd)

if __name__ == "__main__":    
    vtp_to_msh("test.vtp","test.msh")
    print("done.")
