
import time
import serial

codes_of_notes = {'C': (0x01, 0x05),
                'D': (0x01, 0x25),
                'E': (0x01, 0x49),
                'F': (0x01, 0x5D),
                'G': (0x01, 0x88),
                'A': (0x01, 0xB8),
                'B': (0x01, 0xED)}

def checksum(bytearray):
    checksum = 0x00
    for byte in bytearray:
        checksum = checksum ^ byte

    print(checksum)
    return checksum

def wrap_payload(payload):
    wrapped_payload = payload.copy()
    wrapped_payload.insert(0, len(payload))
    wrapped_payload.append(checksum(payload))

    print(wrapped_payload)

    wrapped_payload.insert(0, 0x55)
    wrapped_payload.insert(0, 0xAA)

    return wrapped_payload

def payload_of_note(note, duration):
    payload = bytearray([0x03, 0x03])

    code_of_note = codes_of_notes[note]
    payload.append(code_of_note[1]) # less significant byte first
    payload.append(code_of_note[0])
    payload.append(duration)

    return payload

kobuki = serial.Serial(
    port='/dev/kobuki',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)

print(kobuki.is_open)

# First byte: play a sound
# Second byte: the size of the payload (1)
# third byte: play the happy robot sound
#payload = bytearray([0x04, 0x01, 0x01])
#kobuki.write(wrap_payload(payload))

# First byte: play an arbitrary sound
# Second byte: the size of the payload (3)
# third and fourth bytes: the note to play
# fifth byte: the duration in milis
payload = payload_of_note('B', 255)
kobuki.write(wrap_payload(payload))
kobuki.close()
