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
# X pos, Y pos, width, height, material, mass, gravity accel, terminal x, terminal y, air_friction
AIR_FRICTION = 0.001
GRAVITY = -0.45
MAX_VELO = 10

#Create Player Kinematic Body
Player = KinematicBody(160, 290, 30, 30, Materials["Player"], 20, GRAVITY, MAX_VELO, MAX_VELO, AIR_FRICTION)
Box = KinematicBody(270, 270, 30, 30, Materials["KinematicSolid"], 10, GRAVITY, MAX_VELO, MAX_VELO, AIR_FRICTION)
Box_two = KinematicBody(350, 290, 30, 30, Materials["KinematicSolid"], 10, GRAVITY, MAX_VELO, MAX_VELO, AIR_FRICTION)

StaticBodies = [
	#Create Static Bodies
	# X pos, Y pos, width, height, surface friction
	StaticBody(20, screen_size[1] - 20, 390, 20, Materials["StandardSolid"]), # Floor
	StaticBody(0, 0, screen_size[0], 20, Materials["StandardSolid"]), # Ceiling
	StaticBody(400, 200, 20, 60, Materials["StandardSolid"]), # Left Trampoline Wall
	StaticBody(420, 200, 220, 20, Materials["Trampoline"]), # Trampoline
	StaticBody(200, 100, 220, 20, Materials["StandardSolid"]), # Top Platform
	StaticBody(620, 20, 20, 300, Materials["StandardSolid"]), # Right hand wall
	StaticBody(20, screen_size[1] - 80, 100, 60, Materials["Quicksand"]), # Quicksand
	StaticBody(120, 240, 20, 80, Materials["StandardSolid"]), # Quicksand wall
	StaticBody(0, 20, 20, 300, Materials["StandardSolid"]), # Left hand wall
	StaticBody(0, 160, 200, 20, Materials["StandardSolid"]), # Pool Bottom
	StaticBody(200, 110, 20, 70, Materials["StandardSolid"]), # Pool Right hand Wall
	StaticBody(20, 100, 180, 60, Materials["Water"]), # Pool Water
	StaticBody(390, 300, 250, 20, Materials["Ice"]) # Ice
]

def PlayerControls():
	global running 
	UP_FORCE = 130
	RIGHT_ACCEL = 0.3
	LEFT_ACCEL = -0.3
	MAX_X_VELO = 5

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
				Player.apply_force(0, UP_FORCE)

	keys = pygame.key.get_pressed()
	if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and Player.get_x_velo() < MAX_X_VELO:
		Player.accelerate(RIGHT_ACCEL, 0)
	elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and abs(Player.get_x_velo()) < MAX_X_VELO:
		Player.accelerate(LEFT_ACCEL, 0)

def fill_screen(color):
	screen.fill(color)

def screen_blit(Bodies, *args):

	for body in Bodies + list(args):
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
	Player.interact(StaticBodies, Box, Box_two)
	Box.interact(StaticBodies, Player, Box_two)
	Box_two.interact(StaticBodies, Player, Box)
	Box.update()
	Box_two.update()
	Player.update()

	fill_screen(Colors["black"])
	screen_blit(StaticBodies, Box, Box_two, Player)
	update_screen(60)
	print(clock.get_fps())

# Game Exit
pygame.quit()
quit()