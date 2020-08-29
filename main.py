from bodies import StaticBody, KinematicBody
import pygame
import colors
import materials

# Window Creation
pygame.init()
screen_size = (640, 320)
screen = pygame.display.set_mode(screen_size)
caption = pygame.display.set_caption("Physics Engine")
clock = pygame.time.Clock()

# Color Dictionary
Colors = colors.color_list

# Materials Dictionary
Materials = materials.material_list

# Create Player as a body
# X pos, Y pos, width, height, material, mass, gravity accel, terminal x, terminal y, friction x, friction y
AIR_FRICTION = 0.01
GRAVITY = -0.25
MAX_VELO = 10

#Create Player Kinematic Body
Player = KinematicBody(160, 290, 30, 30, Materials["Player"], 20, GRAVITY, MAX_VELO, MAX_VELO, AIR_FRICTION, AIR_FRICTION)
Box = KinematicBody(200, 290, 30, 30, Materials["KinematicSolid"], 1, GRAVITY, MAX_VELO, MAX_VELO, AIR_FRICTION, AIR_FRICTION)
Box_two = KinematicBody(270, 290, 30, 30, Materials["KinematicSolid"], 30, GRAVITY, MAX_VELO, MAX_VELO, AIR_FRICTION, AIR_FRICTION)

#Create Static Bodies
# X pos, Y pos, width, height, surface friction
Floor = StaticBody(20, screen_size[1] - 20, 390, 20, Materials["StandardSolid"])
Ceiling = StaticBody(0, 0, screen_size[0], 20, Materials["StandardSolid"])
Wall = StaticBody(400, 200, 20, 60, Materials["StandardSolid"])
TrampolinePlatform = StaticBody(420, 200, 220, 20, Materials["Trampoline"])
PlatformTwo = StaticBody(200, 100, 220, 20, Materials["StandardSolid"])
Wall_two = StaticBody(620, 20, 20, 300, Materials["StandardSolid"])
QuicksandPit = StaticBody(20, screen_size[1] - 80, 100, 60, Materials["Quicksand"])
PitWall = StaticBody(120, 240, 20, 80, Materials["StandardSolid"])
Wall_three = StaticBody(0, 20, 20, 300, Materials["StandardSolid"])
PoolBottom = StaticBody(0, 160, 200, 20, Materials["StandardSolid"])
PoolWall = StaticBody(200, 110, 20, 70, Materials["StandardSolid"])
PoolWater = StaticBody(20, 100, 180, 60, Materials["Water"])
Ice = StaticBody(390, 300, 250, 20, Materials["Ice"])

def PlayerControls():
	UP_FORCE = 150
	RIGHT_FORCE = 4
	LEFT_FORCE = -4
	MAX_X_VELO = 4
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
				Player.apply_force(0, UP_FORCE)

	keys = pygame.key.get_pressed()
	if keys[pygame.K_RIGHT] or keys[pygame.K_d] and Player.get_x_velo() < MAX_X_VELO:
		Player.apply_force(RIGHT_FORCE, 0)
	elif keys[pygame.K_LEFT] or keys[pygame.K_a] and abs(Player.get_x_velo()) < MAX_X_VELO:
		Player.apply_force(LEFT_FORCE, 0)

def fill_screen(color):
	screen.fill(color)

def screen_blit(*args):
	for body in args:
		color = body.get_color()
		body_parameters = body.get_body_parameters()[:-3]
		pygame.draw.rect(screen, color, body_parameters)

def update_screen(FPS):
	pygame.display.update()
	clock.tick(FPS)

# Game Loop
running = True  
while running:

	PlayerControls()
	Player.interact(Floor, Ceiling, Wall, Wall_two, TrampolinePlatform, QuicksandPit, PitWall, Ice, Wall_three, PoolBottom, PoolWall, PoolWater, PlatformTwo)
	Box.interact(Floor, Ceiling, Wall, Wall_two, TrampolinePlatform, QuicksandPit, PitWall, Wall_three, PoolBottom, PoolWall, PoolWater, PlatformTwo, Ice)
	Box_two.interact(Floor, Ceiling, Wall, Wall_two, TrampolinePlatform, QuicksandPit, PitWall, Wall_three, PoolBottom, PoolWall, PoolWater, PlatformTwo, Ice)
	Player.interact(Box, Box_two)
	Box.interact(Player, Box_two)
	Box_two.interact(Player, Box)
	Player.update()
	Box.update()
	Box_two.update()

	fill_screen(Colors["black"])
	screen_blit(Floor, Ceiling, Ice, QuicksandPit, PitWall, Wall, TrampolinePlatform, Wall_two, Wall_three, PoolBottom, PoolWall, PoolWater, PlatformTwo, Box, Box_two, Player)
	update_screen(60)

# Game Exit
pygame.quit()
quit()