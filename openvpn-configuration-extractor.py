#!/usr/bin/python
import sys
import os.path

'''
Author: Kraen Hansen <kh@bitblueprint.com>
See: http://howto.praqma.net/ubuntu/vpn/openvpn-access-server-client-on-ubuntu
'''

def print_usage():
	print "Usage: %s client.ovpn [output-directory]" % __file__

def extract_openvpn_config(configuration_filepath, output_directory):
	print "Parsing %s and extracting into %s" % (configuration_filepath, output_directory)
	cf = open(configuration_filepath, 'r')
	fixed_cf = open(output_directory + os.sep + 'client-fixed.ovpn', 'w')
	ca_crt = open(output_directory + os.sep + 'ca.crt', 'w')
	client_crt = open(output_directory + os.sep + 'client.crt', 'w')
	client_key = open(output_directory + os.sep + 'client.key', 'w')
	ta_key = open(output_directory + os.sep + 'ta.key', 'w')

	output = fixed_cf
	for line in cf:
		if '<ca>' in line:
			output = ca_crt
			continue
		elif '<cert>' in line:
			output = client_crt
			continue
		elif '<key>' in line:
			output = client_key
			continue
		elif '<tls-auth>' in line:
			output = ta_key
			continue
		elif '</ca>' in line or '</cert>' in line or '</key>' in line or '</tls-auth>' in line:
			output = fixed_cf
			continue

		 # Skip this line
		if 'key-direction 1' in line:
			continue

		# Prepend references to the output files, into the fixed configuration
		if '## -----BEGIN RSA SIGNATURE-----' in line:
			line = 'ca ca.crt\ncert client.crt\nkey client.key\ntls-auth ta.key 1\n' + line

		output.write(line)
	cf.close()
	fixed_cf.close()
	ca_crt.close()
	client_crt.close()
	client_key.close()
	ta_key.close()
	print "Done ..."

if __name__ == '__main__':
	configuration_filepath = None
	output_directory = None

	# We need the configuration file's path.
	if len(sys.argv) >= 2:
		configuration_filepath = sys.argv[1]
	# Make this the absolute path.
	configuration_filepath = os.path.abspath(configuration_filepath)

	# If the third argument is given, use this as the output directory.
	if len(sys.argv) >= 3:
		output_directory = sys.argv[2]
	else: # The directory of the configuration.
		output_directory = os.path.dirname(sys.argv[1])

	# Make this the absolute path.
	output_directory = os.path.abspath(output_directory)

	if configuration_filepath != None and output_directory != None:
		extract_openvpn_config(configuration_filepath, output_directory)
	else:
		print_usage()
