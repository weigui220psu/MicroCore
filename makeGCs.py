from opentrons import protocol_api
import csv
import numpy

# tweakable settings


Culture_Volume = 0.8 # volume to load of each strain

# metadata
metadata = {
	'protocolName': 'Growth Curve Setup', 
	'author': 'S Tian, sbt5355@psu.edu',
	'description': 'Transfer strains from 96 well growth plate to 2x 384 plates with test compound pre-loaded. Tips returned to box to be discarded!',
	'apiLevel': '2.7'
}

def run(protocol: protocol_api.ProtocolContext):

	# define labware and locations
	tips1 = protocol.load_labware('opentrons_96_filtertiprack_20ul', '6') # 20ul filter tips on deck position 1
	assayplate1 = protocol.load_labware('corning_384_wellplate_112ul_flat', '1') # empty corning 384 well plate to hold co-culture reactions
	assayplate2 = protocol.load_labware('corning_384_wellplate_112ul_flat', '2') # empty corning 384 well plate to hold co-culture reactions
	cultureplate = protocol.load_labware('corning_96_wellplate_360ul_flat', '3') # plate contains liquid cultures of each strain

	# define pipettes
	#p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tips1])
	multi20 = protocol.load_instrument('p20_multi_gen2', 'right', tip_racks=[tips1])
	
	
	for i in range(1, 13):
		multi20.pick_up_tip()
		multi20.mix(5, 20) # mix culture before taking out
		multi20.aspirate(Culture_Volume*9, cultureplate['A'+str(i)]) # pull one extra load dead volume
		multi20.dispense(Culture_Volume, assayplate1['A'+str(i*2-1)])
		multi20.dispense(Culture_Volume, assayplate1['A'+str(i*2)])
		multi20.dispense(Culture_Volume, assayplate2['A'+str(i*2-1)])
		multi20.dispense(Culture_Volume, assayplate2['A'+str(i*2)])
		
		multi20.dispense(Culture_Volume, assayplate2['B'+str(i*2)])
		multi20.dispense(Culture_Volume, assayplate2['B'+str(i*2-1)])
		multi20.dispense(Culture_Volume, assayplate1['B'+str(i*2)])
		multi20.dispense(Culture_Volume, assayplate1['B'+str(i*2-1)])
		multi20.return_tip()