from pylab import *
from prody import *

MODELS_PATH = 'C:\\Users\\Ryan\\Documents\\Bacherlorscriptie2.0\\case10_DisVis_water'
RESULTS_PATH = 'C:\\Users\\Ryan\\Documents\\Bacherlorscriptie2.0\\case10_DisVis_water\\all_fnat.txt'
INTERFACE_REFCOMP = [79, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 121, 122, 123, 124, 125, 126,
                     127, 128, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163,
                     164, 165, 166, 167, 168, 169, 170, 176, 177, 179, 183, 190, 200, 201, 202, 203, 204, 205, 206, 207,
                     208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 683, 684, 686, 687, 688,
                     767, 768, 792, 793, 794, 795, 796, 797, 798, 813, 814, 835, 837, 840, 841, 842, 843, 844, 845, 846,
                     847, 848, 861, 862, 863, 864, 865, 866, 867, 868, 880, 881, 882, 883, 884, 885, 886, 887, 888, 900,
                     901, 902, 903, 904, 905, 906, 908, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 960,
                     969, 970, 971, 972, 973, 974, 986, 987, 988, 1008, 1009, 1010, 1011, 1012, 1023, 1024, 1025, 1026,
                     1027, 1048, 1049, 1050, 1051, 1052, 1053, 1066, 1091, 1092, 1093, 1107]

def interface_res(pdb_path):
    pdb = parsePDB(pdb_path)
    interface1 = pdb.select('chain A and calpha and (same residue as within 10 of chain B)').getResindices()
    interface2 = pdb.select('chain B and calpha and (same residue as within 10 of chain A)').getResindices()
    interface = interface1.tolist() + interface2.tolist()
    return interface


def fnat(interface_refcomp, interface_model):
    amount = 0
    for res in interface_refcomp:
        if res in interface_model:
            amount += 1
    fnat = float(amount) / float(len(interface_refcomp))
    return fnat

def all_fnat(model_path,results_path):
    with open(results_path, 'w') as results:
        for i in range(1, 201):
            pdb_path = model_path + '\\complex_' + str(i) + 'w.pdb'
            interface_model = interface_res(pdb_path)
            results.write(str(fnat(INTERFACE_REFCOMP, interface_model)) + '\n')