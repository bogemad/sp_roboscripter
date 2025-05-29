#!/usr/bin/env python3

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
    sample_d = {'tube_nos': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], 'sample_ids': ['24/856-13B', '24/856-16B', '24/856-19A', '24/856-22C', '25/81-18', '25/81-46A', '25/81-15', '25/81-20', '24/761-1', '24/761-2', '24/761-9', '24/851-11', '24/851-15', '24/851-18', '24/761-1', '24/761-2', '24/761-9', '24/851-11', '24/851-15', '24/851-18', 'dummy_sample_1', 'dummy_sample_2', 'dummy_sample_3', 'dummy_sample_4'], 'pcr_volumes': ['0.7', '0.9', '0.8', '0.9', '1.1', '1.3', '1.5', '1.2', '12.5', '12.5', '12.5', '12.5', '12.5', '12.5', '12.5', '12.5', '12.5', '12.5', '12.5', '12.5', '6.2', '3.1', '0.3', '10.3'], 'water_volumes': ['11.8', '11.6', '11.7', '11.6', '11.4', '11.2', '11.0', '11.3', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '6.3', '9.4', '12.2', '2.2'], 'ont_barcodes': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]}
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
    temperatureModule.set_temperature(celsius=25)
    protocol.delay(minutes=5)
    temperatureModule.set_temperature(celsius=65)
    protocol.delay(minutes=5)
    temperatureModule.set_temperature(celsius=25)
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
            volume=consolidate_vol+1,
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
    #At the default aspiration/dispensing speed of 3.78uL/sec, to mix for 10 minutes would require ~79 mixes
    #Mix volume calculated based off number of samples. If calculated mix volume is greater than 300uL, set mix volume to 300uL (largest available tip size)
    #Aspirate speed is calculated as "rate" multiplied by default aspiration/dispense speed (default speed can be changed with separate command, or by editing back-end labware files)
    #To properly use mix command, tip must be picked up and dropped manually with pick_up_tip and drop_tip commands
    
    approxPoolVol = (numberOfSamples*11)+beadsVolume
    mixVolume=approxPoolVol*mix_proportion
    if mixVolume >200:
        mixVolume=200 

    right_pipette.pick_up_tip()
    right_pipette.mix(
        repetitions=40,
        volume=mixVolume,
        location=tubeRack["D6"],
        rate=0.081,
    )
    right_pipette.drop_tip()

    #Pause protocol for user intervention
    protocol.pause("USER INTERVENTION: Rest of barcode ligation procedure must be completed by hand")