import subprocess

def run(*cmd):
    print('exec', ' '.join(cmd))
    return subprocess.run(cmd, stdout=subprocess.PIPE, check=False)
