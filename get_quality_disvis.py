import sys

if len(sys.argv) != 3:
    print 'Usage: ' + sys.argv[0] + ' <case> <length prot1>'


CASE = sys.argv[1]
LENGTH_PROT1 = int(sys.argv[2])
MAIN_DIR = '/Users/ryan/'+CASE
INTERFACE_HYPOTHETICAL_10A_PATH = MAIN_DIR+'/'+CASE+'_blind/assessment/interface_hypothetical_5A.txt'
PREDICTED_RES_PATH = MAIN_DIR+'/'+CASE+'_predicted_residues_correct.txt'
QUALITY_DISVIS_PATH = MAIN_DIR+'/quality_DisVis_prediction_correct.txt'

with open(PREDICTED_RES_PATH, 'r') as predicted:
	act_prot1 = predicted.readline().split(', ')
	act_prot2 = predicted.readline().split(', ')
	pas_prot1 = predicted.readline().split(', ')
	pas_prot2 = predicted.readline().split(', ')
	act_prot2_conv = []
	pas_prot2_conv = []
	for res in act_prot2:
		converted_res = int(res)+LENGTH_PROT1
		act_prot2_conv.append(str(converted_res))
	for res in pas_prot2:
		converted_res = int(res)+LENGTH_PROT1
		pas_prot2_conv.append(str(converted_res))


with open(INTERFACE_HYPOTHETICAL_10A_PATH,'r') as int_hypo:
	interface_hypothetical = int_hypo.readline().split(', ')


def count_predicted(predicted):
    amount = 0
    for res in predicted:
        if res in interface_hypothetical:
            amount += 1
    return amount


text = 	'# correctly predicted act res prot1: '+str(count_predicted(act_prot1))+'\n' \
		'# correctly predicted act res prot2: '+str(count_predicted(act_prot2_conv))+'\n' \
		'# correctly predicted pas res prot1: '+str(count_predicted(pas_prot1))+'\n' \
		'# correctly predicted pas res prot2: '+str(count_predicted(pas_prot2_conv))+'\n' \
		'# act res prot1: '+str(len(act_prot1))+'\n' \
		'# act res prot2: '+str(len(act_prot2_conv))+'\n' \
		'# pas res prot1: '+str(len(pas_prot1))+'\n' \
		'# pas res prot2: '+str(len(pas_prot2_conv))+'\n' \
		'# hypothetical interface residues: '+str(len(interface_hypothetical))+'\n'
with open(QUALITY_DISVIS_PATH, 'wb+') as qual_disvis:
	qual_disvis.write(text)


