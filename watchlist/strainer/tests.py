from django.test import TestCase

from .services import Radar


class RadarTest(TestCase):
    def setUp(self):
        self.action = 'TEST11'
        self.price = 10.40
        self.user = {
            'email': 'teste@email.com',
            'watchlist': {
                'TEST11': {
                    'buy': 10.1,
                    'sell': 10.3
                },
                'TEST4': {
                    'buy': 10.0,
                    'sell': 10.3
                }
            },
            'radar': '{}'
        }

    def testCheckRadarBuy(self, action='buy'):
        print('Running strainer.tests.RadarTest')
        self.assertEqual(Radar.check_radar(self.user, action, 'TEST11'), False)
        self.user['radar'] = {'buy': ['TEST11']}
        self.assertEqual(Radar.check_radar(self.user, action, 'TEST11'), True)

    def testCheckRadarSell(self, action='sell'):
        self.assertEqual(Radar.check_radar(self.user, action, 'TEST11'), False)

