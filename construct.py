import subprocess
import os
import re
import tokenize



def main():
	while True:
		cmnd = input(">>> ")
		#cmnd1 = list(cmnd)
		#cmnd2 = tokenize.tokenize(cmnd1)
		#print("command is", cmnd2)
		if cmnd == "exit":
			break
		elif cmnd == "cd":
			newpath = input("What path?")
			new_cd(newpath)
		elif cmnd == "help":
			print("Insert command descriptions here")
		elif cmnd == "jobs":
			execute_commands("ps")

		else:
			execute_commands(cmnd)

def new_cd(path):
	try:
		os.chdir(path)
	except Exception:
		print("no such file or directory")


def execute_commands(command):
	try:	
		if "|" in command:
			fpart, lpart = (0, 0)
			fpart = os.dup(0)
			lpart = os.dup(1)

			fcom = os.dup(fpart)

			for cmnd in command.split("|"):
				os.dup2(fcom, 0)
				os.close(fcom)

				if cmnd == command.split("|")[-1]:
					ncom = os.dup(lpart)
				else:
					fcom, ncom = os.pipe()

				os.dup2(ncom, 1)
				os.close(ncom)

				try:
					subprocess.run(cmnd.strip().split())
				except Exception:
					print("Error: Command Not Found")

			os.dup2(fpart, 0)
			os.dup2(lpart, 1)
			os.close(fpart)
			os.close(lpart)
		else:
			#subprocess.run(command.split())
			subprocess.run(command, shell=True)
	except Exception:
		print("Error: Command not found: {}".format(command))




if '__main__' == __name__:
	main()

