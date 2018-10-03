from python.roco import read_vtp, write_dgf
from sys import argv


def vtp_to_dgf(name_vtp, name_dgf):
    """ Converts an vtp file to a Dunde Grid File (.dgf)
    """
    pd = read_vtp(name_vtp)
    write_dgf(name_dgf, pd)


if __name__ == "__main__":
    if len(argv) == 1:
        print("Please state file for conversion")
        exit()
    n1 = argv[2]
    if len(argv) == 2:
        n2 = n1[:-4] + ".dgf"
    if len(argv) == 3:
        n2 = argv[3]
    print("Converting", n1, "to", n2)
    vtp_to_dgf(n1, n2)
    print("done.")
