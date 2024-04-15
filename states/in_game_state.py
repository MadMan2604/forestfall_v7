import os
import sys
import math
import random
import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
#from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.settings import * 
from states.base_state import BaseState
from scripts.pm_buttons import PauseButton





# class for the main game 
## includes game loop and assets loaded 
class InGame(BaseState):

    # initialise variables 
    def __init__(self, game):
        super().__init__(game)

        # pygame screen setup variables
        pygame.display.set_caption('forestfall')
        self.screen = self.game.screen
        self.display = pygame.Surface((WIDTH / 4, HEIGHT / 4))


        self.clock = pygame.time.Clock()

        # define pause state 
        self.pause = False
        
        self.movement = [False, False]
        
        # the asset files of what is being loaded in the window 
        ## grabbed from editor.py as it creates the level that is being drawn
        self.assets = {
            'decor': load_images('tiles/decor'),
            'buildings': load_images('tiles/buildings'),
            'trees': load_images('tiles/trees'),
            'cave_stone': load_images('tiles/cave_stone'),
            'alt_tiles_1': load_images('tiles/alt_tiles_1'), 
            'alt_large_decor_1': load_images('tiles/alt_large_decor_1'),
            #'portal_1': load_image('tiles/portal_1'),
            #'portal_2': load_image('tiles/portal_2'),
            #'portal_3': load_image('tiles/portal_3'),
            'grass': load_images('tiles/grass'),
            'grass1': load_images('tiles/grass1'),
            'dirt': load_images('tiles/dirt'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'background': load_image('backgrounds/background.png'),
            'bgstone': load_images('tiles/bgtiles'),
            'player': load_image('entities/player.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=2),
            'player/run': Animation(load_images('entities/player/run'), img_dur=6),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
            
        }
        
        # LOADS 
        self.sfx = {
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
        }
        #self.clouds = Clouds(self.assets['clouds'], count=16)

        # background assets for the game
        self.backgrounds = {
            0: 'backgrounds/background.png',
            1: 'backgrounds/background1.png',
            2: 'backgrounds/background2.jpeg',
            3: 'backgrounds/background3.png'
        }

        self.sfx['ambience'].set_volume(0.7)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['hit'].set_volume(0.2)
        
        
        self.player = Player(self, (50, 50), (8, 15))
        
        self.tilemap = Tilemap(self, tile_size=16)

        # level state (what is showing on screen)
        self.level = 0
        self.load_level(self.level)
        
        self.screenshake = 0
  
    # functiton thtat loads the levels (1 --> 5)    
    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        
        background_path = self.backgrounds.get(map_id)
        if background_path is not None:
            print("Background file:", background_path)
            self.assets['background'] = load_image(background_path)
        else:
            print(f"Error: Background image not found for map_id {map_id}")
        
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        for tree in self.tilemap.extract([('trees', 10)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
            
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))
            
        self.projectiles = []
        self.particles = []
        self.sparks = []
        
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30
    
    def draw_pause(self):
        # draw a semi-transparent rectangle that covers the entire screen
        ## the (128, 128, 128, 150) represents the colour that I want my bg to be and the level of transparency 
        ### 150 = level of transparency 
        pause_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) 
        pygame.draw.rect(pause_surface, (29, 30, 60, 150), [0, 0, WIDTH, HEIGHT])
        self.screen.blit(pause_surface, (0, 0))
        
    # The main game game state funciton     
    def run(self):

        # Load the music
        pygame.mixer.music.load('data/music/lvl1_test.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # Define the pause state 
        self.pause = False 

        # The main game loop
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == pygame.K_LSHIFT:
                        self.player.dash()
                    if event.key == pygame.K_ESCAPE:
                        self.pause = not self.pause
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
          
            
            if self.pause == False:
                self.display.blit(self.assets['background'], (0, 0))

                
                
                self.screenshake = max(0, self.screenshake - 1)
                
                if not len(self.enemies):
                    self.transition += 1
                    if self.transition > 30:
                        self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                        self.load_level(self.level)
                if self.transition < 0:
                    self.transition += 1
                
                if self.dead:
                    self.dead += 1
                    if self.dead >= 10:
                        self.transition = min(30, self.transition - 1)
                    if self.dead > 40:
                        self.load_level(self.level)
                
                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
                
                for rect in self.leaf_spawners:
                    if random.random() * 49999 < rect.width * rect.height:
                        pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                        self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
                
                #self.clouds.update()
                #self.clouds.render(self.display, offset=render_scroll)
                
                self.tilemap.render(self.display, offset=render_scroll)

            
                
                for enemy in self.enemies.copy():
                    kill = enemy.update(self.tilemap, (0, 0))
                    enemy.render(self.display, offset=render_scroll)
                    if kill:
                        self.enemies.remove(enemy)
                
                if not self.dead:
                    self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                    self.player.render(self.display, offset=render_scroll)
                
                # [[x, y], direction, timer]
                for projectile in self.projectiles.copy():
                    projectile[0][0] += projectile[1]
                    projectile[2] += 1
                    img = self.assets['projectile']
                    self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                    if self.tilemap.solid_check(projectile[0]):
                        self.projectiles.remove(projectile)
                        for i in range(4):
                            self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                    elif projectile[2] > 360:
                        self.projectiles.remove(projectile)
                    elif abs(self.player.dashing) < 50:
                        if self.player.rect().collidepoint(projectile[0]):
                            self.projectiles.remove(projectile)
                            self.dead += 1
                            self.screenshake = max(16, self.screenshake)
                            for i in range(30):
                                angle = random.random() * math.pi * 2
                                speed = random.random() * 5
                                self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                                self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                            
                for spark in self.sparks.copy():
                    kill = spark.update()
                    spark.render(self.display, offset=render_scroll)
                    if kill:
                        self.sparks.remove(spark)
                
                for particle in self.particles.copy():
                    kill = particle.update()
                    particle.render(self.display, offset=render_scroll)
                    if particle.type == 'leaf':
                        particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                    if kill:
                        self.particles.remove(particle)
                         
                if self.transition:
                    transition_surf = pygame.Surface(self.display.get_size())
                    pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                    transition_surf.set_colorkey((255, 255, 255))
                    self.display.blit(transition_surf, (0, 0))
                
                screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), screenshake_offset)
                pygame.display.update()
                self.clock.tick(60)
            
            # Draw the pause screen
            else:


                self.screen.fill(BLACK)
    
