import xml.etree.ElementTree
import itertools

class SongParser:

    def __init__(self, filename):
        root = xml.etree.ElementTree.parse(filename).getroot()
        self.parsed_song = {}
        for track in root:
            events = self._parse_events(track)

        self.note_list = []
        for c in self.parsed_song:
            for note in self.parsed_song[c]:
                self.note_list.append(note)
        self.note_list.sort(key=lambda x: x['time'], reverse=False)


    def _parse_events(self, events):
        for e in events:
            e_parsed = {}
            channel_number = None
            for child in e:
                if child.tag == 'Absolute':
                    e_parsed['time'] = child.text
                elif child.tag == 'NoteOn':
                    e_parsed['type'] = 'on'
                    e_parsed['note'] = child.attrib['Note']
                    channel_number = child.attrib['Channel']
                elif child.tag == 'NoteOff':
                    e_parsed['type'] = 'off'
                    e_parsed['note'] = child.attrib['Note']
                    channel_number = child.attrib['Channel']
            if channel_number and 'type' in e_parsed:
                if channel_number not in self.parsed_song:
                    self.parsed_song[channel_number] = []
                self.parsed_song[channel_number].append(e_parsed)


if __name__ == '__main__':
    pass
