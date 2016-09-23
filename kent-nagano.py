import time

class KobukiToto():

    def __init__(self, number):
        self.number = number

    def play(self, note):
        print("K%d: play" % self.number, note)

    def stop(self, note):
        print("K%d: stop" % self.number, note)

class KentNagano:

    def __init__(self, notes_sorted_by_time, kobukis):
        self.notes = list(notes_sorted_by_time)
        self.free_kobukis = list(kobukis)
        self.tasks = {}


    def play(self):
        while self.notes:
            note = self.notes.pop(0)

            if note['type'] == 'on':
                if self.free_kobukis:
                    k = self.free_kobukis.pop(0)
                    k.play(note)
                    self.tasks[(note['channel'], note['note'])] = k

            elif note['type'] == 'off':
                k = self.tasks[(note['channel'], note['note'])] 
                k.stop(note)
                self.free_kobukis.append(k)

            if self.notes:
                next_note_time = self.notes[0]['time']
                sleep_time = max(0, (next_note_time - note['time']) / 1000.0)
                time.sleep(sleep_time)


if __name__ == '__main__':
    notes = [{'type': 'on', 'note': 48, 'channel': 1, 'time': 1000},
             {'type': 'on', 'note': 48, 'channel': 2, 'time': 2000},
             {'type': 'off', 'note': 48, 'channel': 1,'time': 2500},
             {'type': 'off', 'note': 48, 'channel': 2, 'time': 2550}]

    kobukis = [KobukiToto(i) for i in range(5)]

    kent = KentNagano(notes, kobukis)
    kent.play()
