import unittest
import pygame
from pygame.sprite import Sprite
from juego import Tanque, Laser, Soldado  

class TestTanque(unittest.TestCase):
    def setUp(self):
        pygame.init()  
        self.tanque = Tanque()  

    def test_inicializacion(self):
        
        self.assertEqual(self.tanque.rect.bottomleft, (50, 575))  

    def test_update(self):
       
        self.tanque.dx = 5
        self.tanque.update(0.1)  
        self.assertEqual(self.tanque.rect.x, 50 + 5)  
class TestLaser(unittest.TestCase):
    def setUp(self):
        pygame.init()  
        self.tanque = Tanque()  
        self.laser = Laser(self.tanque.rect.right, self.tanque.rect.centery)  

    def test_inicializacion_laser(self):
        
        self.assertEqual(self.laser.rect.center, (self.tanque.rect.right, self.tanque.rect.centery))

    def test_update_laser(self):
       
        initial_x = self.laser.rect.x
        self.laser.update(0.1)  
        self.assertGreater(self.laser.rect.x, initial_x)  

    def test_colision(self):
        
        soldado = Soldado(500, 525)  
        soldado_group = pygame.sprite.Group(soldado)
        self.laser.rect.center = soldado.rect.center  
        self.laser.update(0.1) ()
        self.assertEqual(len(soldado_group), 1)  
        self.assertEqual(soldado.respawn_count, 2) 

class TestSoldado(unittest.TestCase):
    def setUp(self):
        pygame.init()  
        self.soldado = Soldado(500, 525)  

    def test_inicializacion_soldado(self):
       
        self.assertEqual(self.soldado.rect.topleft, (500, 525))

    def test_respawn(self):
       
        initial_position = self.soldado.rect.topleft
        self.soldado.kill_and_respawn()  
        self.assertNotEqual(self.soldado.rect.topleft, initial_position)  
        self.assertEqual(self.soldado.respawn_count, 2) 


