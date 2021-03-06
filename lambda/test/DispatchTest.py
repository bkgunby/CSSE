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
    # Happy path
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
        self.assertDictEqual(nav.dispatch(input), output)

    def test300_020_ShouldReturnPredictedLocation(self):
        input = {
            'op': 'predict',
            'body': 'Procyon',
            'date': '2018-05-22',
            'time': '12:43:33'
        }
        output = {
            'body': 'Procyon',
            'long': '315d55.5',
            'lat': '5d10.9',
            'time': '12:43:33',
            'date': '2018-05-22',
            'op': 'predict'
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test300_030_ShouldReturnPredictedLocation(self):
        input = {
            'op': 'predict',
            'body': 'Alnilam',
            'date': '2014-12-22',
            'time': '03:43:33'
        }
        output = {
            'body': 'Alnilam',
            'long': '62d13.6',
            'lat': '-1d11.8',
            'time': '03:43:33',
            'date': '2014-12-22',
            'op': 'predict'
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test300_040_ShouldReturnPredictedLocation(self):
        input = {
            'op': 'predict',
            'body': 'Nunki',
            'date': '2042-11-01',
            'time': '08:02:04'
        }
        output = {
            'body': 'Nunki',
            'long': '237d10.2',
            'lat': '-26d16.4',
            'time': '08:02:04',
            'date': '2042-11-01',
            'op': 'predict'
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test300_050_ShouldAssignDefaultDate(self):
        input = {
            'op': 'predict',
            'body': 'Nunki',
            'time': '08:02:04'
        }
        output = {
            'body': 'Nunki',
            'lat': '-26d16.4',
            'op': 'predict',
            'long': '297d30.0',
            'time': '08:02:04'
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test300_060_ShouldAssignDefaultTime(self):
        input = {
            'op': 'predict',
            'body': 'Nunki',
            'date': '2011-04-05'
        }
        output = {
            'body': 'Nunki',
            'date': '2011-04-05',
            'lat': '-26d16.4',
            'long': '268d52.8',
            'op': 'predict'
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test300_070_ShouldSupportCaseInsensitiveStar(self):
        input = {
            'op': 'predict',
            'body': 'betelgeuse',
            'date': '2016-01-17',
            'time': '03:15:42'
        }
        output = {
            'op':'predict',
            'body': 'betelgeuse',
            'date': '2016-01-17',
            'time': '03:15:42',
            'long': '75d53.6',
            'lat': '7d24.3'
        }
        self.assertDictEqual(nav.dispatch(input), output)

    # Sad path
    def test300_910_ShouldReturnLatLongExistsError(self):
        input = {
            'op': 'predict',
            'body': 'Betelgeuse',
            'date': '2016-01-17',
            'time': '03:15:42',
            'lat': '32d3.33'
        }
        output = {
            'op':'predict',
            'body': 'Betelgeuse',
            'date': '2016-01-17',
            'time': '03:15:42',
            'lat': '32d3.33',
            'error': 'lat or long already exists in the input'
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test300_920_ShouldReturnLatLongExistsError(self):
        input = {
            'op': 'predict',
            'body': 'Betelgeuse',
            'date': '2016-01-17',
            'time': '03:15:42',
            'long': '32d3.33'
        }
        output = {
            'op':'predict',
            'body': 'Betelgeuse',
            'date': '2016-01-17',
            'time': '03:15:42',
            'long': '32d3.33',
            'error': 'lat or long already exists in the input'
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test300_930_ShouldReturnMandatoryMissingError(self):
        input = {
            'op': 'predict',
        }
        output = {
            'op':'predict',
            'error': 'mandatory information is missing'
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test300_940_ShouldReturnInvalidStarError(self):
        input = {
            'op': 'predict',
            'body': 'unknown',
            'date': '2016-01-17',
            'time': '03:15:42'
        }
        output = {
            'op': 'predict',
            'body': 'unknown',
            'date': '2016-01-17',
            'time': '03:15:42',
            'error': 'star not in catalog'
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test300_950_ShouldReturnInvalidDateError(self):
        input = {
            'op': 'predict',
            'body': 'Betelgeuse',
            'date': '2016-13-17',
            'time': '03:15:42'
        }
        output = {
            'op': 'predict',
            'body': 'Betelgeuse',
            'date': '2016-13-17',
            'time': '03:15:42',
            'error': 'date is invalid'
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test300_960_ShouldReturnInvalidDateError(self):
        input = {
            'op': 'predict',
            'body': 'Betelgeuse',
            'date': '2016-013-17',
            'time': '03:15:42'
        }
        output = {
            'op': 'predict',
            'body': 'Betelgeuse',
            'date': '2016-013-17',
            'time': '03:15:42',
            'error': 'date is invalid'
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test300_970_ShouldReturnInvalidTimeError(self):
        input = {
            'op': 'predict',
            'body': 'Betelgeuse',
            'date': '2016-01-17',
            'time': '03:15:62'
        }
        output = {
            'op': 'predict',
            'body': 'Betelgeuse',
            'date': '2016-01-17',
            'time': '03:15:62',
            'error': 'time is invalid'
        }
        self.assertDictEqual(nav.dispatch(input), output)

#---- Unit tests
#
# 300 predict
#     Analysis
#        inputs:
#            values ->  dict mandatory validated (private functions are usually validated)
#     Happy path:
#            correct(validDict) -> dictionary with a new correctedDistance/correctedAzimuth element calculated
#     Sad path:
#            correct(invalidDict) -> dictionary with an error corresponding to the invalid element
#
    # Happy path
    def test400_010_ShouldReturnProperElements(self):
        input = {
            'op': 'correct',
            'lat' : '89d20.1',
            'long' :'154d5.4',
            'altitude' :'37d17.4',
            'assumedLat': '35d59.7',
            'assumedLong': '74d35.3',
        }
        output = {
            'op': 'correct',
            'lat' : '89d20.1',
            'long' :'154d5.4',
            'altitude' :'37d17.4',
            'assumedLat': '35d59.7',
            'assumedLong': '74d35.3',
            'correctedDistance': '104',
            'correctedAzimuth': '0d36.8',
        }
        self.assertDictEqual(nav.dispatch(input), output)

    # Sad path
    def test400_010_ShouldReturnMissingLatError(self):
        input = {
            'op': 'correct',
            # 'lat' : '89d20.1',
            'long' :'154d5.4',
            'altitude' :'37d17.4',
            'assumedLat': '35d59.7',
            'assumedLong': '74d35.3',
        }
        output = {
            'op': 'correct',
            # 'lat' : '89d20.1',
            'error': 'mandatory information is missing',
            'long' :'154d5.4',
            'altitude' :'37d17.4',
            'assumedLat': '35d59.7',
            'assumedLong': '74d35.3',
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test400_020_ShouldReturnMissingLongError(self):
        input = {
            'op': 'correct',
            'lat' : '89d20.1',
            # 'long' :'154d5.4',
            'altitude' :'37d17.4',
            'assumedLat': '35d59.7',
            'assumedLong': '74d35.3',
        }
        output = {
            'op': 'correct',
            'lat' : '89d20.1',
            'error': 'mandatory information is missing',
            # 'long' :'154d5.4',
            'altitude' :'37d17.4',
            'assumedLat': '35d59.7',
            'assumedLong': '74d35.3',
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test400_030_ShouldReturnMissingAltitudeError(self):
        input = {
            'op': 'correct',
            'lat' : '89d20.1',
            'long' :'154d5.4',
            # 'altitude' :'37d17.4',
            'assumedLat': '35d59.7',
            'assumedLong': '74d35.3',
        }
        output = {
            'op': 'correct',
            'lat' : '89d20.1',
            'error': 'mandatory information is missing',
            'long' :'154d5.4',
            # 'altitude' :'37d17.4',
            'assumedLat': '35d59.7',
            'assumedLong': '74d35.3',
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test400_040_ShouldReturnMissingAssumedLatError(self):
        input = {
            'op': 'correct',
            'lat' : '89d20.1',
            'long' :'154d5.4',
            'altitude' :'37d17.4',
            # 'assumedLat': '35d59.7',
            'assumedLong': '74d35.3',
        }
        output = {
            'op': 'correct',
            'lat' : '89d20.1',
            'error': 'mandatory information is missing',
            'long' :'154d5.4',
            'altitude' :'37d17.4',
            # 'assumedLat': '35d59.7',
            'assumedLong': '74d35.3',
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test400_050_ShouldReturnMissingAssumedLongError(self):
        input = {
            'op': 'correct',
            'lat' : '89d20.1',
            'long' :'154d5.4',
            'altitude' :'37d17.4',
            'assumedLat': '35d59.7',
            # 'assumedLong': '74d35.3',
        }
        output = {
            'op': 'correct',
            'lat' : '89d20.1',
            'error': 'mandatory information is missing',
            'long' :'154d5.4',
            'altitude' :'37d17.4',
            'assumedLat': '35d59.7',
            # 'assumedLong': '74d35.3',
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test400_060_ShouldReturnCorrectedDistanceExistsError(self):
        input = {
            'op': 'correct',
            'lat' : '89d20.1',
            'long' :'154d5.4',
            'altitude' :'37d17.4',
            'assumedLat': '35d59.7',
            'assumedLong': '74d35.3',
            'correctedDistance': 'sdf',
        }
        output = {
            'op': 'correct',
            'lat' : '89d20.1',
            'correctedDistance': 'sdf',
            'error': 'correctedDistance already exists',
            'long' :'154d5.4',
            'altitude' :'37d17.4',
            'assumedLat': '35d59.7',
            'assumedLong': '74d35.3',
        }
        self.assertDictEqual(nav.dispatch(input), output)

    def test400_070_ShouldReturnCorrectedAzimuthExistsError(self):
        input = {
            'op': 'correct',
            'lat' : '89d20.1',
            'long' :'154d5.4',
            'altitude' :'37d17.4',
            'assumedLat': '35d59.7',
            'assumedLong': '74d35.3',
            'correctedAzimuth': 'sdf',
        }
        output = {
            'op': 'correct',
            'lat' : '89d20.1',
            'correctedAzimuth': 'sdf',
            'error': 'correctedAzimuth already exists',
            'long' :'154d5.4',
            'altitude' :'37d17.4',
            'assumedLat': '35d59.7',
            'assumedLong': '74d35.3',
        }
        self.assertDictEqual(nav.dispatch(input), output)
