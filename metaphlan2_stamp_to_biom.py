#!/usr/bin/env python

from __future__ import division, print_function

__author__ = "Gavin Douglas"
__credits__ = ["Gavin Douglas"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Gavin Douglas"
__email__ = "gavin.douglas@dal.ca"
__status__ = "Development"

import argparse

parser = argparse.ArgumentParser(description="Convert Metaphlan2 taxonomic relative abundances in STAMP format to legacy (tsv) BIOM format", 
                                 epilog='''Usage example:

metaphlan2_stamp_to_biom.py -i metaphlan2_taxonomy.spf -o metaphlan2_taxonomy_tsv.biom

'''
                                 ,formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-i","--input",help="Input STAMP file", required=True)

parser.add_argument("-o","--output",help="Output legacy TSV BIOM file", required=True)

def main():

    # Each metaphlan2 taxa will be given an unique number as an id 
    taxa_num = 1

    header_marker = 0

    args = parser.parse_args()

    outfile = open( args.output , "w" )

    with open( args.input , "r" ) as infile:

        for line in infile:

            # remove newline character
            line = line.rstrip()

            # split by tab
            line_split = line.split("\t") 

            # if this integer == 0 then that means it's the first line, i.e. the header
            if ( header_marker == 0 ):
                header_marker += 1

                header = ["#taxa"] + line_split[8:] + ["taxonomy"]

                # convert each element of header to a string
                headerline = [str(e) for e in header]
                col = "\t".join( headerline )
                print( col , file=outfile )

                # go to next iteration of for loop once finished with header
                continue

            tax = ";".join( line_split[0:8] )

            row_list = [ taxa_num ] + line_split[8:] + [tax]

            # convert each element of row_list to string
            row = [str(e) for e in row_list]

            line_out = "\t".join( row )

            print( line_out , file=outfile)

            # add 1 to the taxa id
            taxa_num += 1 

    outfile.close()

if __name__ == "__main__":
    main()
