import subprocess


def align_profit(profit_script,reference_file, mobile_file, profit_output_file, algn_short_file):
    subprocess.check_call(['bash', 'profit', '-f', profit_script, '-h', reference_file, mobile_file])
    with open(profit_output_file, 'r') as profit_output:
        with open(algn_short_file, 'w') as align_short:
            for line in profit_output:
                if 'with' in line:
                    columns = line.split()
                    short = columns[0]+'-'+columns[2]+':'+columns[4]+'-'+columns[6]+'\n'
                    align_short.write(short)

def convert_numbering(list,align_file,converted_file):
    new_list = []
    with open(align_file, 'r') as align:
        with open(converted_file, 'w') as converted:
            for line in align:
                a,b = line.split(':')
                start_a,end_a = a.split('-')
                start_b,end_b = b.split('-')
                for i in list:
                    if int(end_a)>=int(i)>=int(start_a):
                        print start_a,end_a,start_b,i
                        new = int(i)+int(start_b)-int(start_a))
                        new_list.append(new)
                        converted.write(new)
                        converted.write('\n')
    return new_list
