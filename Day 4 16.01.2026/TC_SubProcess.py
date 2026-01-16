import subprocess

result = subprocess.run("echo Hello World", capture_output=True, text=True, shell=True)
print("Output:", result.stdout)

subprocess.run("python TC_Multiple_Abstract.py", shell=True)
