import xml.etree.ElementTree
import itertools

class SongParser:

    def __init__(self, filename):
        root = xml.etree.ElementTree.parse(filename).getroot()
        self.parsed_song = {}
        for track in root:
            if track.tag == 'Track':
                track_number = int(track.attrib['Number'])
                if track_number not in [0, 1, 2, 5, 7, 11, 13, 14, 15]:
                    self._parse_events(track, track_number)

        self.note_list = []
        for c in self.parsed_song:
            for note in self.parsed_song[c]:
                self.note_list.append(note)
        self.note_list.sort(key=lambda x: (x['time'], x['type'] == 'on'), reverse=False)


    def _parse_events(self, events, track_number):
        for e in events:
            e_parsed = {}
            e_parsed['track'] = track_number
            channel_number = None
            for child in e:
                if child.tag == 'Absolute':
                    e_parsed['time'] = int(child.text)
                elif child.tag == 'NoteOn':
                    e_parsed['type'] = 'on'
                    e_parsed['note'] = int(child.attrib['Note']) + 12
                    channel_number = int(child.attrib['Channel'])
                    e_parsed['channel'] = channel_number
                elif child.tag == 'NoteOff':
                    e_parsed['type'] = 'off'
                    e_parsed['note'] = int(child.attrib['Note']) + 12
                    channel_number = int(child.attrib['Channel'])
                    e_parsed['channel'] = channel_number
            if channel_number and 'type' in e_parsed:
                if channel_number not in self.parsed_song:
                    self.parsed_song[channel_number] = []
                self.parsed_song[channel_number].append(e_parsed)


if __name__ == '__main__':
    pass
