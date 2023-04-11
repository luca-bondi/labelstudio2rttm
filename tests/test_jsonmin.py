"""
Test conversion from LabelStudio JSON-MIN to RTTM

Author: Luca Bondi (bondi.luca@gmail.com)
"""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import labelstudio2rttm


class JsonMinToRttmTestCase(unittest.TestCase):
    """Test conversion from LabelStudio JSON-MIN to RTTM"""

    def test_convert(self):
        """Test conversion"""

        with TemporaryDirectory() as tmpdir:
            src = Path(__file__).parent.joinpath('data', 'src.json')
            dst = Path(tmpdir).joinpath('dst.rttm')
            labelstudio2rttm.convert(src=src, dst=dst)

            with dst.open('r') as file_pointer:
                output = file_pointer.readlines()

            with Path(__file__).parent.joinpath('data', 'dst.rttm').open('r') as file_pointer:
                self.assertSequenceEqual(file_pointer.readlines(), output)


if __name__ == '__main__':
    unittest.main()
