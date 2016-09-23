
import time
import serial


class Kobuki:
    TUNING_CONSTANT = 0.00000275

    frequencies_of_notes = {
        48: 261.63, # C4
        49: 277.18,
        50: 293.66, # D4
        51: 311.13,
        52: 329.63, # E4
        53: 349.23, # F4
        54: 369.99,
        55: 392.0,  # G4
        56: 415.30,
        57: 440.0, # A4
        58: 466.16,
        59: 493.88, # B4
        60: 523.25, # C5
    }

    def __init__(self):
        pass

    def __enter__(self):
        self.comm  = serial.Serial(
            port='/dev/kobuki',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.comm.close()

    def bytes_of_note(self, note):
        kobuki_encoded_note = int(round(1 / (self.frequencies_of_notes[note] *
                                             self.TUNING_CONSTANT)))
        print(kobuki_encoded_note)

        return kobuki_encoded_note.to_bytes(2, byteorder='little')

    def checksum(self, bytearray):
        checksum = 0x00
        for byte in bytearray:
            checksum = checksum ^ byte

        print(checksum)
        return checksum

    def wrap_payload(self, payload):
        wrapped_payload = payload.copy()
        wrapped_payload.insert(0, len(payload))
        wrapped_payload.append(self.checksum(payload))

        print(wrapped_payload)

        wrapped_payload.insert(0, 0x55)
        wrapped_payload.insert(0, 0xAA)

        return wrapped_payload

    def payload_of_note(self, note, duration):
        payload = bytearray([0x03, 0x03])

        code_of_note = self.bytes_of_note(note)
        print(code_of_note)
        payload.append(code_of_note[0])
        payload.append(code_of_note[1])
        payload.append(duration)

        return payload

    def play_note(self, note):
        payload = self.wrap_payload(self.payload_of_note(note, 20))
        self.comm.write(payload)
        time.sleep(0.012)


with Kobuki() as kobuki:
    while True:
        kobuki.play_note(49)