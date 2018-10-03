from python.roco import read_rootsys, write_rsml, write_vtp, Metadata
from sys import argv


def rootsys_to_rsml(name_rs, name_rsml):
    """ Converts an RSWMS RootSys file to a Root System Markup Language (RSML) File
    """
    pd = read_rootsys(name_rs)

    # RSML meta tag
    meta = Metadata()
    meta.set_fun_names(["Time", "Age" ])
    meta.image_label = "Converted from " + name_rs

    write_rsml(name_rsml, pd, meta)
    write_vtp(name_rs + ".vtp", pd)


if __name__ == "__main__":

    if len(argv) == 1:
        print("Please state file for conversion")
        exit()
    n1 = argv[2]
    if len(argv) == 2:
        n2 = n1 + ".rsml"
    if len(argv) == 3:
        n2 = argv[3]
#     n1 = "RootSys1"
#     n2 = n1 + ".xml"
#     print("Converting", n1, "to", n2)
    rootsys_to_rsml(n1, n2)
    print("done.")
