#!/usr/bin/env python3

import sys, csv
from gooey import Gooey, GooeyParser

@Gooey(default_size=(1000, 530))
def main():
    parser = GooeyParser(description="Sangopore RoboScriptor. Generate scripts to run the Sangopore protocol on the OpenTrons OT-2.")
    parser.add_argument('CSVfile', help="Location of the CSV formatted submission sheet", widget="FileChooser")
    parser.add_argument('Script', help="Name of output Sangopore Roboscript", widget="FileSaver")
    parser.add_argument('--DNAControlSample', help="Tick you want DNA Control Sample added to library", action="store_true")
    parser.add_argument('--EDTATubeColour', help="Colour of the EDTA tube cap in the Native barcoding kit 96", choices=['Blue', 'Clear'], default='Clear')
    args = parser.parse_args()
    incsv = args.CSVfile
    outfile = args.Script

    with open(incsv) as inhandle:
        csvr = csv.reader(inhandle)

        outd= {'tube_nos':[], 'sample_ids':[], 'pcr_volumes':[], 'water_volumes':[], 'ont_barcodes':[]}

        for row in csvr:
            try:
                tube_no = int(row[0])
            except ValueError:
                continue
            if tube_no > 96 or tube_no < 1:
                sys.exit("Error - CSV contains tube number outside acceptable limits (must be integer 1-96)")
            sample_id = row[1]
            if sample_id == "":
                continue
            pcr_volume = row[5]
            if pcr_volume == "NA":
                continue
            water_volume = row[6]
            if water_volume == "#VALUE!":
                continue
            try:
                ont_barcode = int(row[9])
            except ValueError:
                continue
            if ont_barcode > 96 or ont_barcode < 1:
                sys.exit("Error - CSV contains ONT Barcode outside acceptable limits (must be integer 1-96)")
            outd['tube_nos'].append(tube_no)
            outd['sample_ids'].append(sample_id)
            outd['pcr_volumes'].append(pcr_volume)
            outd['water_volumes'].append(water_volume)
            outd['ont_barcodes'].append(ont_barcode)
    
    for k,v in outd.items():
        if len(v) != len(outd['tube_nos']):
            sys.exit("Error - Mismatch in critical values. Ensure that all rows in CSV are completely filled with correct values.")

    outscript = template.replace("sample_d = False", f"sample_d = {str(outd)}")
    if args.DNAControlSample == True:
        outscript = outscript.replace("dna_control_sample = False", "dna_control_sample = True")

    if args.EDTATubeColour == 'Blue':
        outscript = outscript.replace("blue_cap_EDTA = False", "blue_cap_EDTA = True")

    with open(outfile, 'w') as outhandle:
        outhandle.write(outscript)

#with open("/home/bogemad/scripts/sangopore_robotics/sp_robotics_template_24-48-96.py") as tmp_handle:
#    template = tmp_handle.read()
template = """REPLACE_ME_1
"""

if __name__ == "__main__":
    main()
