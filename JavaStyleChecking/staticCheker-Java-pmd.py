#! /usr/bin/python 
# -*- coding: utf-8 -*-

########################################################################
"""staticChecker-Java-pmd.py: 
This script is used to grade the submitted java files to the introductory 
and OOP Java courses running on Coursera for 2013/2014."""
__author__ = " Marwan Abdellah, Maxime Augier, \
			   Jean-Cedric Chapplier, \
			   Lepitete Vinecnt, \
			   Jamila Sam"
__copyright__ = "Copyright 2013, EPFL"
__credits__ = ["Marwan Abdellah, \
				Maxime Augier, \
				Jean-Cedric Chapplier, \
				Lepitete Vinecnt, \
				Jamila Sam"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Marwan Abdellah"
__email__ = "marwan.abdellah@epfl.ch"
__status__ = "Testing"
####################################################################

import os
import subprocess
import shutil
import glob
import sys
import re
from random import Random
from decimal import Decimal
import random

# PMD source on the sever 
# This variable has to be changed after deploying the PMD package on the server
# Like /opt/PMD
PMD_SOURCE = "/home/abdellah/Desktop/Coursera/CourseraPreparation/JavaStyleChecking/pmd/"

"""
NOTES: 
* The static checker shoud be running on the .java files after being compiled.
* The script doesn't work if the compilation stage is failed. 
* The static checker should be running in a separte directory to avoid 
  un wanted warnings from the testc cases.  
* The grade must be scaled later on according to the assignment 
* The script runs in the following way 
	/bin/run.sh pmd 	# Run the script 
	-d <file.java> 		# Supply a file to be checked 
	-f text			 	# Text format for the output file 
	-R <rule.xml> 		# Specify a certain rule 
	-version 1.7 		# PMD version 
	-language java 		# Specificy the langauge 
* We have the following checks to choose from "later"
		android.xml
		basic.xml
		braces.xml
		clone.xml
		codesize.xml
		comments.xml
		controversial.xml
		coupling.xml
		design.xml
		empty.xml
		finalizers.xml
		imports.xml
		j2ee.xml
		javabeans.xml
		junit.xml
		logging-jakarta-commons.xml
		logging-java.xml
		migrating_to_13.xml
		migrating_to_14.xml
		migrating_to_15.xml
		migrating_to_junit4.xml
		migrating.xml
		naming.xml
		optimizations.xml
		rulesets.properties
		strictexception.xml
		strings.xml
		sunsecure.xml
		typeresolution.xml
		unnecessary.xml
		unusedcode.xml
"""

"""
! Parses the report file and return the total number of lost points 
  and the messages  
"""
def parse_report_file(report_file_path):
	
	# Report data in details 
	report_data = ""
		
	# Open the report file 
	report_file = open(report_file_path, 'r')
	
	# Initial number of warning 
	num_warnings = 0

	# Read every single line in the file and parse it. 
	for i_line in report_file:
		
		# Check for the logged warning messages.  
		if (":" in i_line):
			record = i_line.split(":")
			
			# The record always has 3 parts, else, there is some problem.
			if (len(record) == 3):
				
				# If the record contains always 2 parts, then that's a warning 
				# report it and increment the number of warnings.
				num_warnings = num_warnings + 1
				report_data += "@Line:" + str(record[1]) + ": " + record[2] + "\n"
	return (report_data, num_warnings)
		
"""
! Returns the total number of lost points from the static checker 
"""
def get_lost_points(num_warnings):
	
	# Penalty for a single warning 
	warning_penalty = -1
	
	# Total lost points 
	lost_points = num_warnings * warning_penalty 
	return lost_points 

"""
# TODOs 
# Define the source directory and the files to be ckeched. 
# Define the path to the PMD "run.sh" script (normal under the bin directory).
# Define the path to the checking rules that the grader will be consider. 
"""
def run_java_static_checker(src_file):
	# Java source file to be checked "will be passed to the main function. 
	# If more than one file needs to be checked, then you just pass the parent directory
	# that contains all the files.  
	src_file = "/home/abdellah/Desktop/Coursera/CourseraPreparation/JavaStyleChecking/code/src/sample.java" 

	# The report file that contains all the warning messages. 
	# For the moment, I just put it in the curent directory, ans I append to it 
	# the new messages every time I just run a new rule check. 
	# We need to clean the file at the first run sp that we can append the 
	# different messages from the different rules. 
	report_file_path = os.getcwd() + "/styleChecker.report"
	subprocess.call("rm " + report_file_path, shell=True)
	
	"""
	PMD stuff, should be passed to the @main function.  
	"""
	# PMD script, and rule path   
	pmd_Script = PMD_SOURCE + "/pmd-src-5.0.4/bin/run.sh"
	pmd_rule_path = PMD_SOURCE + "/pmd-bin-5.0.4/rulesets/java/"
	
	# PMD rule 
	pmd_rule_list =  ["android.xml", 
					"basic.xml",
					"braces.xml",
					"clone.xml",
					"codesize.xml",
					"comments.xml",
					"controversial.xml",
					"design.xml",
					"empty.xml",
					"finalizers.xml",
					"imports.xml",
					"j2ee.xml",
					"javabeans.xml",
					"junit.xml",
					"logging-jakarta-commons.xml",
					"logging-java.xml",
					"migrating_to_13.xml",
					"migrating_to_14.xml",
					"migrating_to_15.xml",
					"migrating_to_junit4.xml",
					"migrating.xml",
					"naming.xml",
					"optimizations.xml",
					"rulesets.properties",
					"strictexception.xml",
					"strings.xml",
					"sunsecure.xml",
					"typeresolution.xml",
					"unnecessary.xml",
					"unusedcode.xml"]
	
	# Check the selected rules in the list "CUSTOMIZABLE"  
	for rule in pmd_rule_list:
		pmd_rule = pmd_rule_path + rule 
		
		# Command for running the static checker 
		shell_command = pmd_Script 
	
		# Indicate the checker 
		shell_command += " pmd -d "
	
		# File to be checked 
		shell_command += src_file
		 
		# For command line user interface 
		shell_command += " -f text" 
	
		# Rule set 
		shell_command += " -R " + pmd_rule
	
		# Version 
		shell_command += " -version 1.7"
	
		# Language 
		shell_command += " -language java"
	
		# Output report file that contains all the warnings messages 
		shell_command += ">>" + report_file_path 
	
		print "Bash Command : \t " + shell_command + "\n"
		subprocess.call(shell_command, shell=True)
	
	# Parse the generated report file.  
	warning_data, num_warnings = parse_report_file(report_file_path)
	
	# Display the lost points and the final message that will be sent 
	# back to the student indicating the total number of lost marks. 
	# This message is just for testing purpose, but it can be printed to the 
	# log file  
	print("Total number of lost points is " + str(get_lost_points(num_warnings)))
	print("The final messges will be : " )
	print (warning_data)
	
run_java_static_checker("")
	
	
	
	
	




