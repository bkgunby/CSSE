from unittest import TestCase
from .. import dispatch as nav

class DispatchTest(TestCase):
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
    #         dispatch({
    #             'op': 'predict',
    #             'body': 'Betelgeuse',
    #             'date': '2016-01-17',
    #             'time': '03:15:42'
    #         }) -> {
    #             'op':'predict',
    #             'body': 'Betelgeuse',
    #             'date': '2016-01-17',
    #             'time': '03:15:42',
    #             'long': '75d53.6',
    #             'lat': '7d24.3'
    #         }
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

    def test100_020_ShouldPredict(self):
        input = {
            'op': 'predict',
            'body': 'Betelgeuse',
            'date': '2016-01-17',
            'time': '03:15:42'
        }
        output = {
            'op':'predict',
            'body': 'Betelgeuse',
            'date': '2016-01-17',
            'time': '03:15:42',
            'long': '75d53.6',
            'lat': '7d24.3'
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
        self.assertDictEqual(nav.dispatch(input), expected)
    def test200_020_ShouldReturnCalcuatedAltitude(self):
        input = {'observation': '42d0.0',  'op': 'adjust'}
        expected = {'altitude':'41d59.0', 'observation': '42d0.0',  'op': 'adjust'}
        self.assertDictEqual(nav.dispatch(input), expected)
    def test200_030_ShouldReturnCalcuatedAltitude(self):
        input = {'observation': '42d0.0',  'op': 'adjust', 'extraKey':'ignore'}
        expected = {'altitude':'41d59.0', 'observation': '42d0.0',  'op': 'adjust', 'extraKey':'ignore'}
        self.assertDictEqual(nav.dispatch(input), expected)

    # Sad path
    def test200_910_ShouldReturnMandatoryElemMissingError(self):
        input = {'op': 'adjust'}
        expected = {'op': 'adjust', 'error':'mandatory information is missing'}
        self.assertDictEqual(nav.dispatch(input), expected)

    def test200_920_ShouldReturnInvalidObservationError(self):
        input = {'observation': '101d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
        expected = {'observation': '101d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71', 'error':'observation is invalid'}
        self.assertDictEqual(nav.dispatch(input), expected)

    def test200_910_ShouldReturnInvalidHeightError(self):
        input = {'observation': '45d15.2', 'height': 'a', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
        expected = {'observation': '45d15.2', 'height': 'a', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71', 'error':'height is invalid'}
        self.assertDictEqual(nav.dispatch(input), expected)

    def test200_920_ShouldReturnInvalidHorizonError(self):
        input = {'observation': '45d15.2', 'height': '6', 'horizon': '   ', 'pressure': '1010', 'op': 'adjust', 'temperature': '71'}
        expected = {'observation': '45d15.2', 'height': '6', 'horizon': '   ', 'pressure': '1010', 'op': 'adjust', 'temperature': '71', 'error':'horizon is invalid'}
        self.assertDictEqual(nav.dispatch(input), expected)

    def test200_930_ShouldReturnInvalidHorizonError(self):
        input = {'observation': '45d15.2', 'height': '6', 'horizon': 2, 'pressure': '1010', 'op': 'adjust', 'temperature': '71'}
        expected = {'observation': '45d15.2', 'height': '6', 'horizon': 2, 'pressure': '1010', 'op': 'adjust', 'temperature': '71', 'error':'horizon is invalid'}
        self.assertDictEqual(nav.dispatch(input), expected)


#---- Unit tests
#
# 300 predict
#     Analysis
#        inputs:
#            values ->  dict mandatory validated (private functions are usually validated)
#     Happy path:
#            predict(validDict) -> dictionary with a new long/lat element calculated
#     Sad path:
#            predict(invalidDict) -> dictionary with an error corresponding to the invalid element
#
    def test300_010_ShouldReturnPredictedLocation(self):
        input = {
            'op': 'predict',
            'body': 'Betelgeuse',
            'date': '2016-01-17',
            'time': '03:15:42'
        }
        output = {
            'op':'predict',
            'body': 'Betelgeuse',
            'date': '2016-01-17',
            'time': '03:15:42',
            'long': '75d53.6',
            'lat': '7d24.3'
        }
        print(nav.dispatch(input))
        self.assertDictEqual(nav.dispatch(input), output)
