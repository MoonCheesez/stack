from Tkinter import *
import tkMessageBox
import os
import subprocess

def main():
	class Application(Frame):
		def __init__(self, master):
			Frame.__init__(self, master)
			self.grid()
			self.create_widgets()

		def create_widgets(self):
			print "Creating Widgets..."
			#Image Label
			self.imglbl = Label(self, text = "Enter disk image directory here:")
			self.imglbl.grid(row = 0, column = 0, columnspan = 2, sticky = W)
			print "imglbl created."
			#Image Entry
			self.imgent = Entry(self)
			self.imgent.grid(row = 1, column = 0, columnspan = 2, sticky = W)
			print "imgent created."
			#Disk Directory Label
			self.dirlbl = Label(self, text = "Enter partition path here:")
			self.dirlbl.grid(row = 2, column = 0, columnspan = 2, sticky = W)
			print "dirlbl created."
			#Disk Directory Entry
			self.dirent = Entry(self)
			self.dirent.grid(row = 3, column = 0, columnspan = 2, sticky = W)
			print "dirent created."
			#Submit Button
			self.submitbut = Button(self, text = "Let's Go!", command = lambda: self.execute())
			self.submitbut.grid(row = 4, column = 0, columnspan = 1, sticky = W)
			print "submitbut created."
			#Enable PV Button
			self.pvcheck = IntVar()
			Checkbutton(self, text = "Enable PV", variable = self.pvcheck).grid(row = 4, column = 1, columnspan = 1, sticky = W)
			print "pvcheck created."
			#Exit Button
			self.exit = Button(self, text = "Exit", command = lambda: exit())
			self.exit.grid(row = 5, column = 0, columnspan = 2, sticky = W)

			print "Widgets Successfully created."

		def execute(self):
			print "Executing..."
			diskdir = self.dirent.get()
			imgdir = self.imgent.get()
			pv = self.pvcheck.get()
			#Check if Disk Directory includes /dev/
			if diskdir[0:5] == "/dev/":
				print "Disk Directory is valid"
				#Check if input includes .img or .dmg or .iso or /dev/zero
				if imgdir[-4:] == ".img" or imgdir[-4:] == ".dmg" or imgdir[-4:] == ".iso" or imgdir == "/dev/zero":
					print "Image Directory is valid"
					if pv == 1:
						print "PV Enabled"
						if subprocess.check_output("sudo echo 'Hello!'", shell=True) == "Hello!\n":
							size = os.path.getsize(imgdir)
							size = str(size)[:-3]
							os.system("sudo dd if="+imgdir+" | pv -s "+size+"K | sudo dd of="+diskdir+" bs=1M")
							exit()
						else:
							tkMessageBox.showwarning("ALERT", "Sudo is OFF. Attempting Sudo again.")
							os.system("sudo echo ''")
							os.system("sudo dd if="+imgdir+" | pv -s "+size+"K | sudo dd of="+diskdir+" bs=1M")
							exit()
					else:
						print "PV Disabled"
						if subprocess.check_output("sudo echo 'Hello!'", shell=True) == "Hello!\n":
							os.system("sudo dd if="+imgdir+" of="+diskdir+" bs=1M")
							exit()
						else:
							tkMessageBox.showwarning("ALERT", "Sudo is OFF. Attempting Sudo again.")
							os.system("sudo echo ''")
							os.system("sudo dd if="+imgdir+" of="+diskdir+" bs=1M")
							exit()
				else:
					tkMessageBox.showwarning("ALERT", "Image directory is not valid")
			else:
				tkMessageBox.showwarning("ALERT", "Disk directory is not valid")

	root = Tk()
	root.title("Image Burner")
	root.geometry("200x200")
	app = Application(root)
	root.mainloop()

if __name__ == '__main__' and subprocess.check_output("sudo echo 'Hello!'", shell=True) == "Hello!\n":
	main()
else:
	pass

