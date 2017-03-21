from unittest import TestCase
from .. import dispatch as nav

class NavigationTest(TestCase):
    # -----------------------------------------------------------------------
    # ---- Acceptance Tests
    # 100 dispatch
    #    Analysis
    #        inputs:
    #           values ->    dictionary, must contain an 'op' key with values 'adjust',
    #                       'predict', 'correct' or 'locate', mandatory, unvalidated
    #        outputs:    dictionary of input in addition to a new altitude element
    #    Happy path analysis:
    #       dispatch({
    #           'observation': '30d1.5',
    #           'height': '19.0',
    #           'pressure': '1000',
    #           'horizon': 'artificial',
    #           'op': 'adjust',
    #           'temperature': '85'
    #       }) -> {
    #           'altitude': '29d59.9',
    #           'observation': '30d1.5',
    #           'height': '19.0',
    #           'pressure': '1000',
    #           'horizon': 'artificial',
    #           'op': 'adjust',
    #           'temperature': '85'
    #       }
    #    Sad path analysis:
    #       dispatch({'op': 'locate'}) -> {'error': 'no op is specified'}
    #       dispatch({
    #           'observation': '15d04.9',
    #           'height': '6.0',
    #           'pressure': '1010',
    #           'horizon': 'artificial',
    #           'temperature': '72'
    #       }) -> {
    #           'observation': '15d04.9',
    #           'height': '6.0',
    #           'pressure': '1010',
    #           'horizon': 'artificial',
    #           'temperature': '72',
    #           'error':'no op is specified'
    #       }
    #       dispatch(42) -> {'error':'parameter is not a dictionary'}
    #       dispatch({'op': 'unknown'}) -> {'error':'op is not a legal operation'}
    #       dispatch() -> {'error':'dictionary is missing'}
    # Happy path
    def test100_010_ShouldCalculateAltitude(self):
        input = {
            'observation': '30d1.5',
            'height': '19.0',
            'pressure': '1000',
            'horizon': 'artificial',
            'op': 'adjust',
            'temperature': '85'
        }
        output = {
            'altitude': '29d59.9',
            'observation': '30d1.5',
            'height': '19.0',
            'pressure': '1000',
            'horizon': 'artificial',
            'op': 'adjust',
            'temperature': '85'
        }
        self.assertDictEqual(nav.dispatch(input), output)
    # Sad path
    def test100_910_ShouldReturnNoOpError(self):
        input = {}
        output = {'error': 'no op is specified'}
        self.assertDictEqual(nav.dispatch(input), output)

    def test100_920_ShouldReturnNoOpError(self):
        input = {
              'observation': '15d04.9',
              'height': '6.0',
              'pressure': '1010',
              'horizon': 'artificial',
              'temperature': '72'
          }
        output = {
              'error': 'no op is specified',
              'observation': '15d04.9',
              'height': '6.0',
              'pressure': '1010',
              'horizon': 'artificial',
              'temperature': '72'
          }
        self.assertDictEqual(nav.dispatch(input), output)

    #       dispatch(42) -> {'error':'parameter is not a dictionary'}
    def test100_930_ShouldReturnErrorIfInputIsNotDict(self):
        input = 42
        output = {'error':'parameter is not a dictionary'}
        self.assertDictEqual(nav.dispatch(input), output)

    #       dispatch({'op': 'unknown'}) -> {'error':'op is not a legal operation'}
    # NOTE: Going with umphress's implementation that combines previous key-values Not excel
    def test100_940_ShouldReturnIllegalOpError(self):
        input = {'op': 'unknown'}
        output = {
            'op': 'unknown',
            'error':'op is not a legal operation'
        }
        self.assertDictEqual(nav.dispatch(input), output)

    #       dispatch() -> {'error':'dictionary is missing'}
    # again, inconsistent with umphress's implementation and excel's. going with umphress again
    def test100_950_ShouldReturnDictMissingError(self):
        output = {'error':'parameter is missing'}
        self.assertDictEqual(nav.dispatch(), output)

#---- Unit tests
#
# 200 adjust
#     Analysis
#        inputs:
#            values ->  dict mandatory validated (private functions are usually validated)
#     Happy path:
#            adjust(validDict) -> dictionary with a new altitude element calculated
#     Sad path:
#            adjust(invalidDict) -> dictionary with an error corresponding to the invalid element
#
    # Happy path
    def test200_010_ShouldReturnCalcuatedAltitude(self):
        input = {'observation': '30d1.5', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        expected = {'altitude':'29d59.9', 'observation': '30d1.5', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        self.assertDictEqual(nav.adjust(input), expected)

    def shouldReturnErrorIfAltitudeExists(self):
        input = {
            'altitude': 'something'
        }
        expected = {
            'altitude': 'something',
            'error': 'altitude already exists in the input'
        }
        actual = nav.adjust(input)
        self.assertDictEqual(expected, actual)

    def shouldReturnErrorIfObservationDoesNotExist(self):
        input = {
            ''
        }


