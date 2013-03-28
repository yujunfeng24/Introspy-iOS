#!/usr/bin/env python

""" Command-line parser for an introspy generated db. """

from sys import argv
from argparse import ArgumentParser
from Analysis import Analyzer
from Signatures import signature_list
from HTMLReport import HTMLReport
from APIGroups import APIGroups

__author__	= "Tom Daniels & Alban Diquet"
__license__	= "?"
__copyright__	= "Copyright 2013, iSEC Partners, Inc."

def main(argv):
	parser = ArgumentParser(description="introspy analysis tool")
	parser.add_argument("db",
			help="Tthe introspy-generated database to analyze.\
			specifying 'remote' initiates the analyzer to fetch a\
			remote database from an iOS device.")
	parser.add_argument("-o", "--outdir",
			help="Generate an HTML report and write it to the specified directory")
	parser.add_argument("-g", "--group",
			choices=APIGroups.API_GROUPS_LIST,
			help="Filter by signature group")
	parser.add_argument("-s", "--sub-group",
			choices=APIGroups.API_SUBGROUPS_LIST,
			help="Filter by signature sub-group")
#	parser.add_argument("-n", "--no-info",
#			action="store_false",
#			help="Don't run signatures that are purely informational")
	args = parser.parse_args()
	analyzer = Analyzer(args.db, signature_list, args.group, args.sub_group)

	if args.outdir:
		report = HTMLReport(args.db, signature_list)
		report.write_to_directory(args.outdir)
	else:
		for (signature, matching_calls) in analyzer.get_findings():
			# Hide empty results
			# TODO: Print other stuff ? signature name or group ?
			if matching_calls:
				print "# %s" % signature.description
				for traced_call in matching_calls:
					print "  %s" % traced_call

if __name__ == "__main__":
	main(argv[1:])

