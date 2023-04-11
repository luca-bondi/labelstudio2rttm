"""
LabelStudio to RTTM labels converter

Author: Luca Bondi (bondi.luca@gmail.com)
"""
import datetime
import json
from pathlib import Path
from typing import Optional

import dateutil.parser
import defopt
from dateutil.tz import tz


def convert(src: Path, dst: Optional[Path] = None, *, speaker_label_prefix: str = 'speaker', overwrite: bool = False):
    """Convert JSON-MIN annotations format to RTTM

    Args:
        src: LabelStudio JSON-MIN file path
        dst: path to destination RTTM file. If not provided, the same as `src` is used, with `.rttm` extension
        speaker_label_prefix: prefix for speaker labels
        overwrite: set to overwrite output file if it already exists

    RTTM format:
    https://github.com/pyannote/pyannote-audio/blob/3147e2bfe9a7af388d0c01f3bba3d0578ba60c67/tutorials/prodigy.md#rttm-file-format
    """

    if dst is None:
        dst = src.with_suffix('.rttm')

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination file {dst} already exists.")

    with src.open('r') as file_pointer:
        labelstudio_annotations = json.load(file_pointer)

        annotation_idx = 0
        if len(labelstudio_annotations) > 1:
            # Multiple annotations, preserve only the most recently updated one
            print(f'Found multiple annotations in {src}, selecting the most recent only')
            most_recent_update = datetime.datetime(year=1970, month=1, day=1, tzinfo=tz.tzutc())

            for idx, annotation in enumerate(labelstudio_annotations):
                update = dateutil.parser.isoparse(annotation['updated_at'])
                if update > most_recent_update:
                    annotation_idx = idx

        annotation = labelstudio_annotations[annotation_idx]

    with dst.open('w') as file_pointer:
        uri = Path(annotation["audio"]).name
        for segment in annotation["label"]:
            for label in segment['labels']:
                if label.startswith(speaker_label_prefix):
                    start_time = segment['start']
                    duration = segment['end'] - segment['start']
                    speaker_id = "speaker_" + label.replace(speaker_label_prefix, '')
                    file_pointer.write(f"SPEAKER {uri} 1 {start_time} {duration} <NA> <NA> {speaker_id} <NA> <NA>\n")

    print(f'RTTM file saved in {dst}')


if __name__ == "__main__":
    defopt.run(convert)
