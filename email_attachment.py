import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import Encoders
from time import sleep
from random import choice
import re
import io
import os
import sys
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Designed and implemented for the Pomona College CS51 Course
# Author: Juan Zamudio
# Date: February 1, 2017
#
# To be used only by the Pomona College Computer Science Department
# and with permission from Juan Zamudio
#
# Copyright 2017 Juan Zamudio
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# You must turn ON less secure apps for Gmail
# (https://www.google.com/settings/security/lesssecureapps)#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
try:
	s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	# identify ourselves to gmail client
	# use port 587 for TLS with the basic smtplib.SMTP('domain.com', 587) method.
	# re-identify ourselves as an encrypted connection
	s.ehlo()
	# If using TLS, uncomment the line below.
	# s.starttls()
	# login with user input if you are not comfortable storing
	# your password in plaintext
	#
	# Fill in the parameters of method below with (email address, password)
	s.login('','')
	s.set_debuglevel(1)
except IOError:
	print IOError

##########################################################################
# TODO;								       	 #
# 	-filter bad emails (failed send attempts are bad mmkay)	    [1/2]#
#		+ connect to telnet and send bogus email, 	         #
#		+ and take error message to determine if real or not   	 #
#	-implement send rate-limiting loop			      [X]#
#	-body template with variable or probabalistics modifications  [X]#
#	-attachments			                              [0]#
##########################################################################
#
# Build a body template here, {}'s are filled randomly later on,
# in respective order of what is passed in.
#

labNames = ["Lab 01", #[0]
			"Lab 02",
			"Lab 03",
			"Lab 04",
			"Lab 05",
			"Lab 06", #[5]
			"Lab 07",
			"Lab 08",
			"Lab 09",
			"Lab 10",
			"Lab 11", #[10]
			"Lab 12",
			"Test Program 1",
			"Test Program 2"] #[13]

# {0} - Different message subjects"
variation0 = ["CS51: " + labNames[0] + " Grade",
			  "CS51: Missing " + labNames[0] + " Submission",
			  "CS51: Improper " + labNames[0] + " Submission."]

# {1} Different salutations.
variation1 = ["Hello", "Good evening", "Good morning"]

# {2} Something to change it up, you decide.
variation2 = ["", "", ""]

# {3} - The last "blank space" of the message.
variation3 = ["Sincerely,", "Thank you,", "Best,"]

# Where the {}'s are, is where a variation(0-3) will be substituted in.
# In their respective orders.
template1 = """{} {},

Attached is a file containing a rubric with your grade for {}.

If you have any questions please let us know!

{}

Your CS51 TAs"""

# initialize your sending address and create empty lists
# add email address in sender assignment
sender = ''
recipients = []
names = []

# As it stands, the script takes a plaintext file of the format
# "examplemail@example.com:John Doe" per line
# Add the name of the text file in the first parameter of open method
mailTxt = open("", 'r')

# load recipients from text file into a list (recipients), strip the \n
# from the strings
for line in mailTxt:
	line = line.replace('\n',"")
	recipients.append(re.split(':', line)[0])
	names.append(re.split(':',line)[1])

# create a pseudo-random message
# write the message to a log file for later analysis/debugging
# send an email every 75 seconds to avoid getting flagged as spam
# print out "sending..." and the message for debugging purposes
cwd = os.getcwd()

show = []

for visible in os.listdir(sys.argv[1]):
	if visible != "log.txt" and not visible.startswith('.'):
		show.append(visible)

for k, items in zip (range(len(recipients)), show):

	os.chdir(cwd)

	msg = MIMEMultipart()
	msg['Subject'] = variation0[0]
	msg['From'] = sender
	msg['To'] = recipients[k]

	part1 = MIMEText(template1.format(variation1[0], names[k], labNames[0], variation3[0]))
	msg.attach(part1)

	os.chdir(sys.argv[1])

	part2 = MIMEBase('application', "octet-stream")
	part2.set_payload(open(items,"rb").read())
	Encoders.encode_base64(part2)
	part2.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(items))
	msg.attach(part2)

	print "Sending..."
	print msg

	try:
		s.sendmail(sender, recipients[k], msg.as_string())
	# Basic error handling: sometimes the SSL/TLS connection is interrupted
	# which will stop the script. When this happens, it will try to reconnect,
	# send the message, and continue the loop.
	except Exception, e:
		print str(e) + "error: logging in and continuing loop with next address..."
		s = smtplib.SMTP_SSL('smtp.gmail.com',465)
		s.ehlo()
		s.login(#email address as before, password as before)
		s.set_debuglevel(1)
		continue

	# with io.open('log.txt', 'a', encoding='utf-8') as f:
	#   try:
	#   	f.write(unicode(msg))
	#   # As the code stands, it has trouble with accented characters.
	#   # You might want to figure out a way to remove them or change
	#   # the encoding of the script.
	#   except:
	# 	f.write("Error handling ASCII encoded names: "+ unicode(recipients[k]))

	print "Sleeping for 20 seconds..."
	sleep(20)

print "Messages have been sent."
f.close()
s.quit()
