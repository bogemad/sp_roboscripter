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
template = """#!/usr/bin/env python3

#To run this script using the Opentron simulator, use opentrons_simulate [file name].py

import sys
from opentrons import protocol_api

#Metadata section required for OpenTron scripts; won't work without it
metadata = {
    "apiLevel":"2.3",
    "protocolName":"Nanopore Native Barcoding 96 Library Prep",
    "description":"Script for end prep step",
    "author": "Joshua Bourke"
}
#Requirements section not strictly required, but encouraged as best practice
#requirements = {"robotType":"OT-2", "apiLevel":"2.0"}

#Pipettes are loaded after labware: you need to have already loaded tips in order to tell the pipette to use it. And now you won’t have to reference tips again in your code — it’s assigned to the left_pipette and the robot will know to use it when commanded to pick up tips.



#Function to load labware into script
def run(protocol: protocol_api.ProtocolContext):
    sample_d = False
    if sample_d == False:
        sys.exit("Error - Sample details have not been added to this script. Please rerun sp_roboscripter.py")
    dna_control_sample = False
    blue_cap_EDTA = False
    numberOfSamples = len(sample_d['tube_nos'])
    mix_proportion = 0.7
    # function to choose setup based on number of samples
    if numberOfSamples <= 24:
        tipsSmall = protocol.load_labware("opentrons_96_filtertiprack_20ul",10)
        tipsLarge = protocol.load_labware("opentrons_96_filtertiprack_200ul",11)
        tubeRack = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap",6)
        samplePlate = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", 2)
        barcodePlate = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt",3)
        temperatureModule = protocol.load_module("temperature module gen2",1)
        reactionPlate=temperatureModule.load_labware(name="opentrons_96_aluminumblock_nest_wellplate_100ul")
        left_pipette = protocol.load_instrument("p20_single_gen2", "left", tip_racks=[tipsSmall])
    elif numberOfSamples <= 48 and numberOfSamples > 24:
        tipsSmall = protocol.load_labware("opentrons_96_filtertiprack_20ul",10)
        tipsSmall2= protocol.load_labware("opentrons_96_filtertiprack_20ul",9)
        tipsLarge = protocol.load_labware("opentrons_96_filtertiprack_200ul",11)
        tubeRack = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap",6)
        samplePlate = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", 2)
        barcodePlate = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt",3)
        reactionPrepPlate = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt",4)
        temperatureModule = protocol.load_module("temperature module gen2",1)
        reactionPlate=temperatureModule.load_labware(name="opentrons_96_aluminumblock_nest_wellplate_100ul")
        left_pipette = protocol.load_instrument("p20_single_gen2", "left", tip_racks=[tipsSmall, tipsSmall2])
    elif numberOfSamples <= 96 and numberOfSamples > 48:
        tipsSmall = protocol.load_labware("opentrons_96_filtertiprack_20ul",10)
        tipsSmall2= protocol.load_labware("opentrons_96_filtertiprack_20ul",9)
        tipsSmall3= protocol.load_labware("opentrons_96_filtertiprack_20ul",8)
        tipsSmall4= protocol.load_labware("opentrons_96_filtertiprack_20ul",7)
        tipsLarge = protocol.load_labware("opentrons_96_filtertiprack_200ul",11)
        tubeRack = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap",6)
        samplePlate = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", 2)
        barcodePlate = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt",3)
        reactionPrepPlate = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt",4)
        reactionPlate2 = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt",5)
        temperatureModule = protocol.load_module("temperature module gen2",1)
        reactionPlate=temperatureModule.load_labware(name="opentrons_96_aluminumblock_nest_wellplate_100ul")
        left_pipette = protocol.load_instrument("p20_single_gen2", "left", tip_racks=[tipsSmall, tipsSmall2, tipsSmall3, tipsSmall4])
    else:
        sys.exit(f"Error - Unable to proceed due to invalid number of samples number of samples must be between 1 and 96 (Number of Samples = {numberOfSamples})")
    
    right_pipette = protocol.load_instrument("p300_single_gen2", "right", tip_racks=[tipsLarge])

    print("Pipettes loaded:", left_pipette,",", right_pipette)

    fixed_barcodes = [ int(x)-1 for x in sample_d['ont_barcodes'] ]

    # Calculate and make ctrl end prep master mix

    buffered_num_samples = numberOfSamples + 5
    DCS_vol = buffered_num_samples * 1.0
    EPRB_vol = buffered_num_samples * 1.75
    EPE_vol = buffered_num_samples * 0.75
    #End prep reaction buffer - 1.75uL   
    right_pipette.transfer(
        volume=EPRB_vol,
        source=tubeRack["A1"],
        dest=tubeRack["D1"],
    )
    #End prep enzyme - 0.75uL   
    right_pipette.transfer(
        volume=EPE_vol,
        source=tubeRack["A2"],
        dest=tubeRack["D1"],
        mix_after=(5, (EPRB_vol+EPE_vol)*mix_proportion)
    )
    #Diluted DNA control sample - 1uL (add if necessary)
    if dna_control_sample == True:
        right_pipette.transfer(
            volume=DCS_vol,
            source=tubeRack["C1"],
            dest=tubeRack["D1"],
            mix_after=(5, (DCS_vol+EPRB_vol+EPE_vol)*mix_proportion)
        )
        MM_sample_vol = 3.5
    else:
        MM_sample_vol = 2.5

    #consolidate water, MM and sample in tip, transfer to reaction plate and mix
    for i, barcode in enumerate(fixed_barcodes):
        if float(sample_d['water_volumes'][i]) == 0.0:
            sources = [tubeRack["D1"],samplePlate.wells()[i]]
            source_volumes = [MM_sample_vol, float(sample_d['pcr_volumes'][i])]
        else:
            sources = [tubeRack["D5"],tubeRack["D1"],samplePlate.wells()[i]]
            source_volumes = [float(sample_d['water_volumes'][i]), MM_sample_vol, float(sample_d['pcr_volumes'][i])]
        left_pipette.pick_up_tip()
        left_pipette.consolidate(
            volume=source_volumes,
            source=sources,
            dest=reactionPlate.wells()[i],
            mix_after=(5,8),
            new_tip="never",
        )
        left_pipette.drop_tip()

    #Heating paramters for temperature module
    temperatureModule.set_temperature(celsius=20)
    protocol.delay(minutes=5)
    temperatureModule.set_temperature(celsius=65)
    protocol.delay(minutes=5)
    temperatureModule.set_temperature(celsius=20)
    protocol.delay(minutes=1)
    temperatureModule.deactivate()
    
    #Use second reaction plate if more than 48 samples
    if numberOfSamples <= 48:
        rxndest2 = reactionPlate.wells()[48:numberOfSamples+48]
    else:
        rxndest2 = reactionPlate2.wells()[numberOfSamples]

    #Add 5uL of BLMM to second reaction wells
    # left_pipette.transfer(
    #     volume=5,
    #     source=tubeRack["A4"],
    #     dest=rxndest2, #24-48-96
    #     new_tip="always",
    # )
    #consolidate water, barcode and end-prepped sample in tip, transfer to reaction prep plate and mix
    for reactionPrepWell, barcode0base in enumerate(fixed_barcodes):
        if numberOfSamples <= 24:
            rxnprepdest = reactionPlate.wells()[reactionPrepWell+24]
            rxndest2_ind = reactionPlate.wells()[reactionPrepWell+48]
        elif numberOfSamples > 24 and numberOfSamples <= 48:
            rxnprepdest = reactionPrepPlate.wells()[reactionPrepWell]
            rxndest2_ind = reactionPlate.wells()[reactionPrepWell+48]
        else:
            rxnprepdest = reactionPrepPlate.wells()[reactionPrepWell]
            rxndest2_ind = reactionPlate2.wells()[reactionPrepWell]
        left_pipette.pick_up_tip()
        left_pipette.transfer(
            volume=5,
            source=tubeRack["A4"],
            dest=rxndest2_ind,
            new_tip="never",
        )
        left_pipette.drop_tip()
        left_pipette.pick_up_tip()
        left_pipette.consolidate(
            volume=[12.0, 5.0, 3.0],
            source=[tubeRack["D4"], barcodePlate.wells()[barcode0base], reactionPlate.wells()[reactionPrepWell]],
            dest=rxnprepdest,
            mix_after=(5,14),
            new_tip="never",
        )
    # transfer 5uL of barcode, sample mix to second reaction wells
        left_pipette.transfer(
        volume=5,
        source=rxnprepdest,
        dest=rxndest2_ind, 
        new_tip="never",
        mix_after=(5,7),
        )
        left_pipette.drop_tip()

    #Incubate at room temperautre for 20 minutes (probably not needed as it should take more than 20 mins for above step to complete)
    #protocol.delay(minutes=5)
    protocol.pause("Up to EDTA addition")
    #Distribute 1uL of EDTA to each well (write blue cap EDTA option into procedure), mix and pool into D6
    if blue_cap_EDTA == True:
        edta_vol = 2
        consolidate_vol = 12
        beadsVolume = numberOfSamples*4.8
    else:
        edta_vol = 1
        consolidate_vol = 11
        beadsVolume = numberOfSamples*4.4

    for reactionPrepWell, barcode0base in enumerate(fixed_barcodes):
        if numberOfSamples <= 24:
            rxndest2_ind = reactionPlate.wells()[reactionPrepWell+48]
        elif numberOfSamples > 24 and numberOfSamples <= 48:
            rxndest2_ind = reactionPlate.wells()[reactionPrepWell+48]
        else:
            rxndest2_ind = reactionPlate2.wells()[reactionPrepWell]
        left_pipette.pick_up_tip()
        left_pipette.transfer(
            volume=edta_vol,
            source=tubeRack["A5"],
            dest=rxndest2_ind,
            new_tip="never",
            mix_after=(5,7)
        )
        left_pipette.transfer(
            volume=consolidate_vol,
            source=rxndest2_ind,
            dest=tubeRack["D6"],
            new_tip="never",
        )
        left_pipette.drop_tip()
        
    #Add AXP beads to pool. Volume to add varies depending on number of samples in pool (4uL beads per sample)
    right_pipette.transfer(
        volume=beadsVolume,
        source=tubeRack["A6"],
        dest=tubeRack["D6"],
        mix_before=(5, beadsVolume*mix_proportion),
    )

    #Slowly pipette mix for ~10 minutes at room temperature (this is to replace the Hula mixer to allow continuous automation)

    
    # approxPoolVol = (numberOfSamples*11)+beadsVolume
    # mixVolume=approxPoolVol*mix_proportion
    # if mixVolume >200:
    #     mixVolume=200 
    
    #calculate number of repetitions to make 10 minutes mixing = 600 secs / (2 * mixing volume uL (2 * as one rep = volume up + volume down))/(pipetting speed uL/sec)), round up by converting value to integer and + 1
    # repetitions = int((10*60)/((mixVolume*2)/0.2))+1

    # right_pipette.pick_up_tip()
    # right_pipette.mix(
    #     repetitions=repetitions,
    #     volume=mixVolume,
    #     location=tubeRack["D6"],
    #     rate=0.2,
    # )
    # right_pipette.drop_tip()

    #Pause protocol for user intervention
    protocol.pause("USER INTERVENTION: Sequencing pool and beads are ready for 10 minute Hula mixing and separation on a magnetic rack.")


"""

if __name__ == "__main__":
    main()
