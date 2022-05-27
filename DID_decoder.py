# PCR84 DID decoder
import xlsxwriter
# Create structures
events = [
    'Dropped AVB packets',
    'AAM AVB buffer underrun',
    'AAM AVB buffer overrun',
    'Missing AVB stream at point of Rendering',
    'Missing AVB stream while Rendering, cyclic check',
    'AudioSession creation',
    'AudioSession KeepAlive',
    'Dropped PTP packets',
    'PTP historic SequenceID',
    'PTP duplicated packet',
    'Non AS-capable FICM',
    'BroadR-Reach disconnected / CAN NManagement present'
]

counters = [
    'Current power cycle',
    'Last 16 power cycles',
    'Number of power cycles since last detected',
    'Lifetime counter'
]

stream_monitors = [
    '0x00 00 00 00 00 00 00 02 ---> FG_FICM_01',
    '0x00 00 00 00 00 00 00 03 ---> FG_FICM_02',
    '0x00 00 00 00 00 00 00 04 ---> FG_FICM_03',
    '0x00 00 00 00 00 00 00 05 ---> FG_FICM_04',
    '0x00 00 00 00 00 00 00 06 ---> FG_FICM_05',
    '0x00 00 00 00 00 00 00 07 ---> FG_FICM_06',
    '0x00 00 00 00 00 00 00 08 ---> TeDL_FICM_01',
    '0x00 00 00 00 00 00 00 0B ---> BG_FICM_00',
    '0x00 00 00 00 00 00 00 0E ---> BG_RICM_00',
    '0x00 00 00 00 00 00 00 11 ---> BG_RICM_03',
    '0x00 00 00 00 00 00 00 12 ---> BG_RICM_04',
    '0x00 00 00 00 00 00 00 13 ---> BG_RICM_05',
    '0x00 00 00 00 00 00 00 18 ---> BG_HSPM_00',
    '0x00 00 00 00 00 00 00 19 ---> BG_HSPM_03',
    '0x00 00 00 00 00 00 00 1A ---> BG_HSPM_04',
    '0x00 00 00 00 00 00 00 1B ---> BG_HSPM_05',
    'Other stream IDs'
]

session_monitors = [
    '0x00 ---> Entertainment',
    '0x01 ---> EntertainmentSpeech',
    '0x02 ---> BroadcastAnnoucment',
    '0x03 ---> NavigationPrompt',
    '0x04 ---> NavigationChime',
    '0x05 ---> TelephoneCall_BTWideband',
    '0x06 ---> TelephoneCall_BTNarrowband',
    '0x07 ---> TelephoneCall_BTSuperWideband',
    '0x08 ---> TelephoneCall_CarPlayWideband',
    '0x09 ---> TelephoneCall_CarPlayNarrowband',
    '0x0A ---> TelephoneCall_CarPlaySuperWideband',
    '0x0B ---> TelephoneCall_CarPlaySiri',
    '0x0C ---> TelephoneCall_CarPlayFacetime',
    '0x0D ---> TelephoneRingNearEndInBand',
    '0x0E ---> TelephoneRingNearEndInWav',
    '0x0F ---> TelematicseCall',
    '0x10 ---> TelematicsbCall',
    '0x11 ---> TelematicsConciergeCall',
    '0x12 ---> SpeechPlayback',
    '0x13 ---> SpeechListening',
    '0x14 ---> UISoundsDucking',
    '0x15 ---> UISounds1',
    '0x16 ---> AlertChimeHi',
    '0x17 ---> AlertChimeMid',
    '0x18 ---> AlertChimeLo',
    '0x19 ---> InfoChimeHi',
    '0x1A ---> InfoChimeMid',
    '0x1B ---> InfoChimeLo',
    '0x1C ---> Alert PromptHi',
    '0x1D ---> AlertPromptMid',
    '0x1E ---> AlertPromptLo',
    '0x1F ---> Tick-Tock',
    '0x20 ---> Seatbelt',
    '0x21 ---> Seatbelt Escalation',
    '0x22 ---> Park Aid',
    '0x23 ---> Wade Aid',
    '0x24 ---> CarPlayAlternateAudio_NonDucking',
    '0x25 ---> CarPlayAlternateAudio_Ducking',
    '0x26 ---> CarPlayAlternateAudio_Muting',
    '0x27 ---> TelephoneCall_AndroidAutoASR',
    '0x28 ---> TelephoneCall_BaiduCarLifeASR',
    '0x29 ---> UISoundsMuting',
    'Other SessionType IDs (0x2A-0xFF)',
]

raw_did = "62 80 D1 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 01 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 00 00 00 02 00 00 01 00 07 00 03 6F 00 00 00 02 00 00 "

did_values = []
raw_did_no_spaces = raw_did.replace(" ","")
if raw_did_no_spaces.find("6280D1") == 0: # returns the position a string was found
    did_string = raw_did_no_spaces[6:]
else:
    did_string = raw_did_no_spaces
if len(did_string) != 2112:
    print("Incorrect DID size, check raw_did")

i = 0
while i != 2112:
    i = i + 2
    did_values.append(did_string[i - 2:i])
    i = i + 4
    did_values.append(did_string[i - 4:i])
print(did_values)

# for i in range(2, len(did_string), 2):
#     did_values.append(did_string[i-2:i])
# print(did_values)


did_names = []
for i, e in enumerate(events):
    if i < 5:
        for sm in stream_monitors:
            for c in counters:
                did_names.append(c + ' ' + e + ' ' + sm)
    elif i < 7:
        for sm in session_monitors:
            for c in counters:
                did_names.append(c + ' ' + e + ' ' + sm)
    else:
        for c in counters:
            did_names.append(c + ' ' + e)

with open('output.txt', 'w') as output_file:
    for r in did_names:
        # print(r)
        output_file.write(r + '\n')

workbook = xlsxwriter.Workbook('DID_decoder.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', "DID description")
for i, n in enumerate(did_names):
    worksheet.write('A' + str(i+2), n)
worksheet.write('B1', "DID value (HEX)")
for i, v in enumerate(did_values):
    worksheet.write('B' + str(i + 2), v)

workbook.close()