import subprocess


def calculate_rmsd(reference_file, model_path, results_path):
    subprocess.check_call(['bash', 'rmsd.sh', reference_file, model_path, results_path])



