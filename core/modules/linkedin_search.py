#!/usr/bin/env	python
#description:Linkedin employee search module#

from colorama import Fore,Back,Style
from core import load

import os,sys
import urllib
import requests
import re,string

class module_element(object):

	def __init__(self):
		self.title = "Linkedin gathering : \n"
		self.require = {"enterprise":[{"value":"","required":"yes"}],"limit_search":[{"value":"","required":"yes"}]}
		self.export = []
		self.export_file = ""
		self.export_status = False

	def show_options(self):
                load.show_options(self.require)

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

	def set_agv(self, argv):
		self.argv = argv

	def run_module(self):
		ret = self.check_require()
		if ret == False:
			print Back.YELLOW + Fore.BLACK + "Please set the required parameters" + Style.RESET_ALL
		else:
			self.main()

	def main(self):
		userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
		quantity = "100"
		server = "www.google.com"
		word = self.get_options("enterprise")
		limit = int(self.get_options("limit_search"))
		counter = 0
		result = ""
		totalresults = ""
		print Fore.GREEN + "Search Linkedin research" + Style.RESET_ALL
		url="http://"+ server + "/search?num=" + str(limit) + "&start=0&hl=en&meta=&q=site%3Alinkedin.com/in%20" + word
		r=requests.get(url)
		result = r.content
		if result != "":
			regex = re.compile('">[a-zA-Z0-9._ -]* \| LinkedIn')
			output = regex.findall(result)
			if len(output) > 0:
				for line in output:
					if line.strip() != "":
						if " | LinkedIn" in line and '">' in line:
							people = line.strip().replace(' | LinkedIn','').replace('">','')
							print Fore.BLUE + "* "+ Style.RESET_ALL + people
							self.export.append(people)
			else:
				print Fore.RED + "Nothing on linkedin." + Style.RESET_ALL
		else:
			print Fore.RED + "Can't get response" + Style.RESET_ALL


