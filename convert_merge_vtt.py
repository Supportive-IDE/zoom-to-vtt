import os, re

SOURCE_FOLDER = 'REPLACE WITH PATH TO FOLDER CONTAINING RAW TRANSCRIPT'

class Row:
    speaker = 'UNKNOWN'
    words = ''

    def __init__(self, time_entry: str):
        times = time_entry.split(' --> ')
        self.start_time = times[0][:times[0].find('.')]
        self.end_time = times[1][:times[1].find('.')]

    def process_speech(self, speaker_entry: str):
        first_colon = speaker_entry.find(':')
        if first_colon == -1:
            raise IndexError("Doesn't seem to have a speaker")
        self.speaker = speaker_entry[:first_colon]
        self.words = speaker_entry[first_colon+1:]

    def __str__(self):
        return f'{self.start_time}    {self.speaker}: {self.words}'


def get_vtt() -> list:
    vtts = []
    for file in os.listdir(SOURCE_FOLDER):
        if file.endswith('.vtt'):
            vtts.append(file)
    return vtts


def get_vtt_contents(file: str) -> list:
    lines = []
    with open(file, 'r') as file:
        lines = [line.strip() for line in file if line != '\n']
    return lines


def is_time_row(line: str) -> bool:
    return re.match("\d\d:\d\d:\d\d.\d\d\d", line) is not None


def convert_lines_to_rows(lines: list) -> list:
    rows = []
    for i in range(len(lines)):
        if is_time_row(lines[i]):
            new_row = Row(lines[i])
            new_row.process_speech(lines[i+1])
            rows.append(new_row)
            i += 1
    return rows


def merge_speakers(rows: list) -> list:
    merged = []
    for row in rows:
        if len(merged) == 0 or row.speaker != merged[-1].speaker:
            merged.append(row)
        else:
            merged[-1].end_time = row.end_time
            merged[-1].words = f'{merged[-1].words} {row.words}'
    return merged


if __name__ == '__main__':
    vtts = get_vtt()
    for transcript in vtts:
        lines = get_vtt_contents(SOURCE_FOLDER + transcript)
        rows = merge_speakers(convert_lines_to_rows(lines))
        rows_to_write = [str(row) for row in rows]
        with open(SOURCE_FOLDER + 'merged_transcript.txt', 'w') as file:
            file.write('\n'.join(rows_to_write))
