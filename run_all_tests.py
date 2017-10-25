import unittest
import transcribe_file

class TestRecognizer(unittest.TestCase):
    def test_functionality(self):
        transcribe_file('/home/kruszynka/Pobrane/Source/mastercoder/fakap-team/plikiaudio/rozmowa1_ENG/scen1tel2.flac')

    def test_new_something(self):
        newVar = 'ok'
        print(newVar)
        assert(True)


if __name__ == '__main__':
    unittest.main()
