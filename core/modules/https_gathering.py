#!/usr/bin/env	python
#description:SSL/TLS information gathering (sslyze)#

from colorama import Fore,Back,Style

import os,sys
import urllib
import subprocess

class module_element(object):

	def __init__(self):
		self.title = "SSL/TLS gathering : \n"
		self.require = {"domain":[{"value":"","required":"yes"}]}
		self.export = []
		self.export_file = ""
		self.export_status = False

	def set_agv(self, argv):
		self.argv = argv

	def show_options(self):
		#print Back.WHITE + Fore.WHITE + "Module parameters" + Style.RESET_ALL
		for line in self.require:
			if self.require[line][0]["value"] == "":
				value = "No value"
			else:
				value = self.require[line][0]["value"]
			if self.require[line][0]["required"] == "yes":
				if self.require[line][0]["value"] != "":
					print Fore.GREEN+Style.BRIGHT+ "+ " +Style.RESET_ALL+line+ ": " +value
				else:
					print Fore.RED+Style.BRIGHT+ "- " +Style.RESET_ALL+line+ "(" +Fore.RED+ "is_required" +Style.RESET_ALL+ "):" +value
			else:
				if self.require[line][0]["value"] != "":
					print Fore.GREEN+Style.BRIGHT+ "+ " +Style.RESET_ALL+line + ": " +value
				else:
					print Fore.WHITE+Style.BRIGHT+ "* " +Style.RESET_ALL+line + "(" +Fore.GREEN+ "optional" +Style.RESET_ALL+ "):" +value
		#print Back.WHITE + Fore.WHITE + "End parameters" + Style.RESET_ALL

	def export_data(self, argv=False):
		if len(self.export) > 0:
			if self.export_file == "":
				if argv == False:
					user_input = raw_input("operative (export file name ?) > ")
				else:
					user_input = argv
				if os.path.exists("export/"+user_input):
					self.export_file = "export/"+user_input
				elif os.path.exists(user_input):
					self.export_file = user_input
				else:
					print Fore.GREEN + "Writing " + user_input + " file" + Style.RESET_ALL
					self.export_file = "export/"+user_input
				self.export_data()
			elif self.export_status == False:
				file_open = open(self.export_file,"a+")
				file_open.write(self.title)
				for line in self.export:
					file_open.write("- " + line +"\n")
				print Fore.GREEN + "File writed : " + self.export_file + Style.RESET_ALL
				file_open.close()
				self.export_status = True
		else:
			print Back.YELLOW + Fore.BLACK + "Module empty result" + Style.RESET_ALL
	
	def set_options(self,name,value):
		if name in self.require:
			self.require[name][0]["value"] = value
		else:
			print Fore.RED + "Option not found" + Style.RESET_ALL
	
	def check_require(self):
		for line in self.require:
			for option in self.require[line]:
				if option["required"] == "yes":
					if option["value"] == "":
						return False
		return True

	def get_options(self,name):
		if name in self.require:
			return self.require[name][0]["value"]
		else:
			return False

	def run_module(self):
		ret = self.check_require()
		if ret == False:
			print Back.YELLOW + Fore.BLACK + "Please set the required parameters" + Style.RESET_ALL
		else:
			self.main()

	def main(self):
		domain = self.get_options('domain')
		if "://" in domain:
			domain = domain.split("://")[1]
		if domain[:-1] == "/":
			domain = domain[-1]
		try:
		    response = subprocess.check_output(["sslyze", "--regular", domain])
		    if response != "":
		    	explode = response.split('\n')
		    	for line in explode:
		    		self.export.append(line)
		    		print Fore.BLUE + "* " + Style.RESET_ALL + line
		    else:
		    	print Fore.RED + "* "  + Style.RESET_ALL + "Can't get SSL/TLS with sslyze"
		except OSError as e:
		    if e.errno == os.errno.ENOENT:
		        print e
		    else:
		        # Something else went wrong while trying to run `sslyze`
		        raise


