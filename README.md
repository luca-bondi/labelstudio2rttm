# LabelStudio to RTTM labels converter
Converter from LabelStudio JSON-MIN format to RTTM

RTTM reference: https://github.com/pyannote/pyannote-database#speaker-diarization

## Usage
```
positional arguments:
  src                   LabelStudio JSON-MIN file path
  dst                   path to destination RTTM file. If not provided, the same as src is used, with .rttm extension
                        (default: None)

optional arguments:
  -h, --help            show this help message and exit
  -s SPEAKER_LABEL_PREFIX, --speaker-label-prefix SPEAKER_LABEL_PREFIX
                        prefix for speaker labels
                        (default: speaker)
  -o, --overwrite, --no-overwrite
                        set to overwrite output file if it already exists
                        (default: False)

```