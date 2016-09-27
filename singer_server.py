
import time
import serial
import socketserver
import threading


class SignerServer:

    class SignerServerHandler(socketserver.BaseRequestHandler):
        def handle(self):
            self.start_blinking_led()
            while True:
                data = self.request.recv(2)

                if not data:
                    time.sleep(0.01)
                    continue

                if data == bytearray([0xff, 0xff]):
                    break

                note = (int.from_bytes(data, byteorder='big') & 0xFF00) >> 8
                start_or_stop = int.from_bytes(data, byteorder='big') & 0x00FF

                if start_or_stop == 1:
                    if self.note_is_playing():
                        self.stop_playing_note()
                    self.start_playing_note(note)
                elif start_or_stop == 0:
                    self.stop_playing_note()

            self.stop_blinking_led()

        def start_playing_note(self, note):
            self.server.keep_playing = True
            self.server.note_thread = threading.Thread(target=self.play_note_continuously, args=(note,))
            self.server.note_thread.start()

        def stop_playing_note(self):
            self.server.keep_playing = False
            self.server.note_thread.join()

        def play_note_continuously(self, note):
            while self.server.keep_playing:
                self.server.kobuki.play_note(note)

        def note_is_playing(self):
            return self.server.note_thread != None and self.server.keep_playing

        def start_blinking_led(self):
            self.server.keep_blinking = True
            blinking_thread = threading.Thread(target=self.blink_led_continuously)
            blinking_thread.start()

        def stop_blinking_led(self):
            self.server.keep_blinking = False

        def blink_led_continuously(self):
            while self.server.keep_blinking:
                self.server.kobuki.toggle_led(1)
                time.sleep(1)

            self.server.kobuki.leds_off()

    def __init__(self):
        pass

    def __enter__(self):
        self.server = socketserver.TCPServer(('0.0.0.0', 1986), self.SignerServerHandler)
        self.server.keep_playing = False
        self.server.kobuki = Kobuki()
        self.server.kobuki.connect()
        self.server.kobuki.play_note(50)
        self.server.note_thread = None
        self.server.keep_blinking = False
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.server.server_close()
        self.server.kobuki.close()

    def serve(self):
        self.server.serve_forever()


class Kobuki:
    TUNING_CONSTANT = 0.00000275

    def __init__(self):
        self.led_flags = 0x00

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def frequency_of_note(self, note):
        return 2**((note-69)/12) * 440

    def connect(self):
        self.comm  = serial.Serial(
            port='/dev/kobuki',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)

    def close(self):
        self.comm.close()

    def bytes_of_note(self, note):
        kobuki_encoded_note = int(round(1 / (self.frequency_of_note(note) *
                                             self.TUNING_CONSTANT)))

        return kobuki_encoded_note.to_bytes(2, byteorder='little')

    def checksum(self, bytearray):
        checksum = 0x00
        for byte in bytearray:
            checksum = checksum ^ byte

        return checksum

    def wrap_payload(self, payload):
        wrapped_payload = payload.copy()
        wrapped_payload.insert(0, len(payload))
        wrapped_payload.append(self.checksum(payload))

        wrapped_payload.insert(0, 0x55)
        wrapped_payload.insert(0, 0xAA)

        return wrapped_payload

    def payload_of_note(self, note, duration):
        payload = bytearray([0x03, 0x03])

        code_of_note = self.bytes_of_note(note)
        payload.append(code_of_note[0])
        payload.append(code_of_note[1])
        payload.append(duration)

        return payload

    def play_note(self, note):
        payload = self.wrap_payload(self.payload_of_note(note, 20))
        self.comm.write(payload)
        time.sleep(0.012)

    def payload_of_led(self):
        return bytearray([0x0C, 0x02, 0x00, self.led_flags])

    def payload_of_leds_off(self):
        return bytearray([0x0C, 0x02, 0x00, 0x00])

    def toggle_led(self, led):
        mask = 0x00
        if led == 1:
            mask = 0x02
        elif led == 2:
            mask = 0x08

        self.led_flags = self.led_flags ^ mask
        self.update_leds()

    def update_leds(self):
        payload = self.wrap_payload(self.payload_of_led())
        self.comm.write(payload)

    def leds_off(self):
        payload = self.wrap_payload(self.payload_of_leds_off())
        self.comm.write(payload)

if __name__ == '__main__':

    with SignerServer() as server:
        server.serve()
