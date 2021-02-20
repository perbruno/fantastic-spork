from django.test import TestCase

from .services import Radar, check_crossed_borders


class RadarTest(TestCase):

    def setUp(self):
        self.stock = 'TEST11'
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


    def testCrossedBordersInvalidAction(self, direction='outside',action='hold'):
        self.assertEquals(check_crossed_borders(direction, 
                          action, self.stock, self.price, self.user),False)
        action=None
        self.assertEquals(check_crossed_borders(direction, 
                          action, self.stock, self.price, self.user),False)
                          

    def testCrossedBordersOutsideSell(self, direction='outside',action='sell'):
        self.assertEquals(check_crossed_borders(direction, 
                          action, self.stock, self.price, self.user),True)

        self.user['radar'] = {action: [self.stock]}
        self.assertEquals(check_crossed_borders(direction, 
                          action, self.stock, self.price, self.user),False)    
        
        self.price = 10.2
        self.assertEquals(check_crossed_borders(direction, 
                          action, self.stock, self.price, self.user),False)
        
        self.user['radar'] = '{}'
        self.assertEquals(check_crossed_borders(direction, 
                          action, self.stock, self.price, self.user),False)
        

    def testCrossedBordersOutsideBuy(self, direction='outside',action='buy'):
        self.price = 10.04
        self.assertEquals(check_crossed_borders(direction, 
                          action, self.stock, self.price, self.user),True)

        self.user['radar'] = {action: [self.stock]}
        self.assertEquals(check_crossed_borders(direction, 
                          action, self.stock, self.price, self.user),False)    
        
        self.price = 10.2
        self.assertEquals(check_crossed_borders(direction, 
                          action, self.stock, self.price, self.user),False)
        
        self.user['radar'] = '{}'
        self.assertEquals(check_crossed_borders(direction, 
                          action, self.stock, self.price, self.user),False)
        
