from xml_player import SongParser
import time
import socket

class KobukiToto():

    def __init__(self, number, ip , port):
        print(ip, port)
        self.number = number
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    def play(self, note):
        self.socket.send(bytes([note['note'], 1]))
        # print("K%d:" % self.number, note)

    def stop(self, note):
        self.socket.send(bytes([note['note'], 0]))
        # print("K%d:" % self.number, note)

class KentNagano:

    def __init__(self, notes_sorted_by_time, kobukis):
        self.notes = list(notes_sorted_by_time)
        self.free_kobukis = list(kobukis)
        self.tasks = {}


    def play(self):
        while self.notes:
            note = self.notes.pop(0)

            if note['type'] == 'on':
                if self.free_kobukis and (note['channel'], note['note'], note['track']) not in self.tasks.keys():
                    k = self.free_kobukis.pop(0)
                    k.play(note)
                    self.tasks[(note['channel'], note['note'], note['track'])] = k

            elif note['type'] == 'off':
                try:
                    k = self.tasks.pop((note['channel'], note['note'], note['track']))
                    k.stop(note)
                    self.free_kobukis.append(k)
                except KeyError:
                    pass

            if self.notes:
                next_note_time = self.notes[0]['time']
                sleep_time = max(0, (next_note_time - note['time']) / 1000.0)
                time.sleep(sleep_time)


if __name__ == '__main__':
    notes = SongParser('./song.xml').note_list
    print('playing %d notes' % len(notes))

    kobukis = [KobukiToto(i, '192.168.0.1%02d' % i, 1986) for i in [1, 2, 4, 5, 6, 9, 11, 14]]

    kent = KentNagano(notes, kobukis)
    kent.play()
