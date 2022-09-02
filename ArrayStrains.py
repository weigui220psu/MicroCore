from opentrons import protocol_api
import csv
import numpy

# metadata
metadata = {
    'protocolName': 'Array Strains',
    'author': 'J Bisanz, jordan.bisanz@gmail.com',
    'description': 'Load samples from a 12mL snap top culture tubes (90) to a deep well plate which already has 500ul glycerol in it.',
    'apiLevel': '2.7'
}


#fix disposing first tip, and protocol comment instead of print, add tip touch on both sides?

# The data below is taken from a CSV wherein the first column defines the plate number, the second is the well from an indexing plate (biorad 96 well) and the third column is the volume (in µL) to transfer.
# Note: Ensure that total volumes to be transferred do not exceed 1.4mL!!!!! If so, program will pause and ask you to replace the tube when it is full. After run merge all tubes.
# Lines 17-114 are to be replaced with the users data taken from the loadings.csv of the tracking sheet.
loadings = '''
StrainID,Rack_Deck,Rack_Well,DeepPlate_Well
JEBNNNNN,Rack1,A1,B1
JEBNNNNN,Rack1,A2,C1
JEBNNNNN,Rack1,A3,D1
JEBNNNNN,Rack1,A4,E1
JEBNNNNN,Rack1,A5,F1
JEBNNNNN,Rack1,B1,G1
JEBNNNNN,Rack1,B2,H1
JEBNNNNN,Rack1,B3,A2
JEBNNNNN,Rack1,B4,C2
JEBNNNNN,Rack1,B5,D2
JEBNNNNN,Rack1,C1,E2
JEBNNNNN,Rack1,C2,F2
JEBNNNNN,Rack1,C3,G2
JEBNNNNN,Rack1,C4,H2
JEBNNNNN,Rack1,C5,A3
JEBNNNNN,Rack2,A1,B3
JEBNNNNN,Rack2,A2,D3
JEBNNNNN,Rack2,A3,E3
JEBNNNNN,Rack2,A4,F3
JEBNNNNN,Rack2,A5,G3
JEBNNNNN,Rack2,B1,H3
JEBNNNNN,Rack2,B2,A4
JEBNNNNN,Rack2,B3,B4
JEBNNNNN,Rack2,B4,C4
JEBNNNNN,Rack2,B5,E4
JEBNNNNN,Rack2,C1,F4
JEBNNNNN,Rack2,C2,G4
JEBNNNNN,Rack2,C3,H4
JEBNNNNN,Rack2,C4,A5
JEBNNNNN,Rack2,C5,B5
JEBNNNNN,Rack3,A1,C5
JEBNNNNN,Rack3,A2,D5
JEBNNNNN,Rack3,A3,F5
JEBNNNNN,Rack3,A4,G5
JEBNNNNN,Rack3,A5,H5
JEBNNNNN,Rack3,B1,A6
JEBNNNNN,Rack3,B2,B6
JEBNNNNN,Rack3,B3,C6
JEBNNNNN,Rack3,B4,D6
JEBNNNNN,Rack3,B5,E6
JEBNNNNN,Rack3,C1,G6
JEBNNNNN,Rack3,C2,H6
JEBNNNNN,Rack3,C3,A7
JEBNNNNN,Rack3,C4,B7
JEBNNNNN,Rack3,C5,C7
JEBNNNNN,Rack4,A1,D7
JEBNNNNN,Rack4,A2,E7
JEBNNNNN,Rack4,A3,F7
JEBNNNNN,Rack4,A4,G7
JEBNNNNN,Rack4,A5,H7
JEBNNNNN,Rack4,B1,A8
JEBNNNNN,Rack4,B2,B8
JEBNNNNN,Rack4,B3,C8
JEBNNNNN,Rack4,B4,D8
JEBNNNNN,Rack4,B5,E8
JEBNNNNN,Rack4,C1,F8
JEBNNNNN,Rack4,C2,G8
JEBNNNNN,Rack4,C3,H8
JEBNNNNN,Rack4,C4,A9
JEBNNNNN,Rack4,C5,B9
JEBNNNNN,Rack5,A1,C9
JEBNNNNN,Rack5,A2,D9
JEBNNNNN,Rack5,A3,E9
JEBNNNNN,Rack5,A4,F9
JEBNNNNN,Rack5,A5,G9
JEBNNNNN,Rack5,B1,H9
JEBNNNNN,Rack5,B2,A10
JEBNNNNN,Rack5,B3,B10
JEBNNNNN,Rack5,B4,C10
JEBNNNNN,Rack5,B5,D10
JEBNNNNN,Rack5,C1,E10
JEBNNNNN,Rack5,C2,F10
JEBNNNNN,Rack5,C3,G10
JEBNNNNN,Rack5,C4,H10
JEBNNNNN,Rack5,C5,A11
JEBNNNNN,Rack6,A1,B11
JEBNNNNN,Rack6,A2,C11
JEBNNNNN,Rack6,A3,D11
JEBNNNNN,Rack6,A4,E11
JEBNNNNN,Rack6,A5,F11
JEBNNNNN,Rack6,B1,G11
JEBNNNNN,Rack6,B2,H11
JEBNNNNN,Rack6,B3,A12
JEBNNNNN,Rack6,B4,B12
JEBNNNNN,Rack6,B5,C12
JEBNNNNN,Rack6,C1,D12
JEBNNNNN,Rack6,C2,E12
JEBNNNNN,Rack6,C3,F12
JEBNNNNN,Rack6,C4,G12
JEBNNNNN,Rack6,C5,H12

'''
loadings_parsed = loadings.splitlines()[1:] # Discard the blank first line.

def run(protocol: protocol_api.ProtocolContext):

    # define labware
	DeepPlate = protocol.load_labware('nest_96_wellplate_2ml_deep', '7')
	tips1 = protocol.load_labware('opentrons_96_filtertiprack_1000ul', '8') # 20ul filter tips on deck position 1
	p1000 = protocol.load_instrument('p1000_single_gen2', 'right', tip_racks=[tips1])

	#Racks
	Rack1 = protocol.load_labware('opentrons_15_tuberack_14000ul', '1')
	Rack2 = protocol.load_labware('opentrons_15_tuberack_14000ul', '2')
	Rack3 = protocol.load_labware('opentrons_15_tuberack_14000ul', '3')
	Rack4 = protocol.load_labware('opentrons_15_tuberack_14000ul', '4')
	Rack5 = protocol.load_labware('opentrons_15_tuberack_14000ul', '5')
	Rack6 = protocol.load_labware('opentrons_15_tuberack_14000ul', '6')

    #Loop through the transfer
	for transfer in csv.DictReader(loadings_parsed):
		p1000.pick_up_tip()
		p1000.aspirate(1000, eval(transfer['Rack_Deck'])[transfer['Rack_Well']].bottom(10))
		p1000.dispense(1000, DeepPlate[transfer['DeepPlate_Well']].bottom(10))
		p1000.mix(2, 700, DeepPlate[transfer['DeepPlate_Well']].bottom(10))
		#p1000.touch_tip()
		p1000.drop_tip()

