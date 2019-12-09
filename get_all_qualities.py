# add CAPRI assesment to all_results.txt

input = open('/Users/ryan/Documents/case10_XL/results/all_results.txt', 'r')
output = open('/Users/ryan/Documents/case10_XL/results/all_qualities.txt', 'w')

for line in input:
	columns = line.split(',')
	l_rmsd = columns[1]
	i_rmsd = columns[2]
	if l_rmsd <= 1.0 or i_rmsd <= 1.0:
		quality = 'high\n'
	if l_rmsd <= 5.0 or i_rmsd <= 2.0:
		quality = 'medium\n'
	if l_rmsd <= 10.0 or i_rmsd <= 4.0:
		quality = 'acceptable\n'
	else:
		quality = 'incorrect\n'
	output.write(quality)
input.close()
output.close()