import math

# Static Bodies - X position, Y position, Width, Height, Surface Friction
class StaticBody():
	
	def __init__(self, x_pos, y_pos, width, height, material):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.width = width
		self.height = height
		self.material_type = material[0]
		self.color = material[1]
		self.surface_friction = material[2]
		self.energy_return = material[3]
		self.max_bounce = material[4]
		self.materialList = material
		self.collision = False

	def get_x_pos(self):
		return self.x_pos

	def get_y_pos(self):
		return self.y_pos

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

	# Return positional data of body
	def get_body_parameters(self):
		return [self.x_pos, self.y_pos, self.width, self.height, self.surface_friction, self.energy_return, self.max_bounce]

	def get_material_type(self):
		return self.material_type

	def get_material_list(self):
		return self.materialList

	def get_color(self):
		return self.color

	def set_x_pos(self, x_pos):
		self.x_pos = x_pos

	def set_y_pos(self, y_pos):
		self.y_pos = y_pos

	# List of body Parameters - Masks are rectangular defined by [x_pos, y_pos, body_width, body_height]
	def detect_collision(self, body_parameters):
		self.collision = False

		# Collision from the left
		if self.x_pos <= body_parameters[0] + body_parameters[2] and self.x_pos >= body_parameters[0]:
			if self.y_pos + self.height >= body_parameters[1] and self.y_pos <= body_parameters[1]:
				self.collision = True
			elif self.y_pos <= body_parameters[1] + body_parameters[3] and self.y_pos >= body_parameters[1]:
				self.collision = True
		# Collision from the right
		elif self.x_pos + self.width >= body_parameters[0] and self.x_pos <= body_parameters[0]:
			if self.y_pos + self.height >= body_parameters[1] and self.y_pos <= body_parameters[1]:
				self.collision = True
			elif self.y_pos <= body_parameters[1] + body_parameters[3] and self.y_pos >= body_parameters[1]:
				self.collision = True

# Kinematic Bodies - Vectors, Gravity, Acceleration, Max Velocities, Frictional Constants
class KinematicBody(StaticBody):

	MAX_COEFFICIENT_FRICTION = 0.9
	MIN_X_VELO = 0.3
	MIN_Y_VELO = 0.3
	MIN_BOUNCE_VELO = 2
	YF_RATIO = 0.1
	FRICTION_THRESHOLD = 0.1

	def __init__(self, x_pos, y_pos, width, height, material, mass, gravity_magnitude, max_x_velo, max_y_velo, temp_friction_x, temp_friction_y):
		super().__init__(x_pos, y_pos, width, height, material)
		self.mass = mass
		self.gravity_magnitude = gravity_magnitude
		self.max_x_velo = max_x_velo
		self.max_y_velo = max_y_velo
		self.x_velo = 0
		self.y_velo = 0
		self.accel_x = 0
		self.accel_y = 0
		self.prev_x_velo = 0
		self.prev_y_velo = 0
		self.constant_friction_x = temp_friction_x
		self.constant_friction_y = temp_friction_y
		self.temp_friction_x = 0
		self.temp_friction_y = 0
		self.future_x_velo = None
		self.future_y_velo = None
		self.future_x_pos = None
		self.future_y_pos = None

	def get_x_velo(self):
		return self.x_velo

	def get_y_velo(self):
		return self.y_velo

	def get_prev_x(self):
		return self.prev_x_velo

	def get_prev_y(self):
		return self.prev_y_velo

	def get_mass(self):
		return self.mass

	def set_x_vector(self, magnitude_x):
		self.x_velo = magnitude_x

	# Give body vectors
	def set_y_vector(self, magnitude_y):
		self.y_velo = magnitude_y

	def temp_max_x_vector(self, max_min, magnitude):
		if max_min == "max" and self.x_velo > magnitude:
			self.x_velo = magnitude
		elif max_min == "min" and self.x_velo < magnitude:
			self.x_velo = magnitude

	def temp_max_y_vector(self, max_min, magnitude):
		if max_min == "max" and self.y_velo > magnitude:
			self.y_velo = magnitude
		elif max_min == "min" and self.y_velo < magnitude:
			self.y_velo = magnitude

	# Give body acceleration
	def accelerate(self, magnitude_x, magnitude_y):
		self.accel_x += magnitude_x
		self.accel_y += magnitude_y

	def apply_force(self, force_x, force_y):
		self.accel_x += force_x / self.mass
		self.accel_y += force_y / self.mass

	def apply_momentum(self, momentum_x, momentum_y):
		self.x_velo += momentum_x
		self.y_velo += momentum_y

	def get_x_force(self):
		return self.accel_x * self.mass

	def get_y_force(self):
		return self.accel_y * self.mass

	def gravity(self):
		self.accelerate(0, self.gravity_magnitude)

	def temp_x_friction(self, temp_friction_x):
		self.temp_friction_x = temp_friction_x

	def temp_y_friction(self, temp_friction_y):
		self.temp_friction_y = temp_friction_y

	def friction_x(self, x_velo, prev_x, temp_friction_x):

		if abs(prev_x) > KinematicBody.MIN_X_VELO:
			if temp_friction_x != None:
				if abs(x_velo) > KinematicBody.MIN_X_VELO:
					self.friction_force_x = (self.mass * x_velo * temp_friction_x)
				else:
					self.friction_force_x = self.x_velo * self.mass
			else:
				if abs(x_velo) > KinematicBody.MIN_X_VELO:
					self.friction_force_x = (self.mass * x_velo * self.constant_friction_x)
				else:
					self.friction_force_x = self.x_velo * self.mass
		elif abs(self.x_velo) > KinematicBody.MIN_X_VELO:
			self.friction_force_x = self.x_velo * self.mass
		elif self.accel_x == 0:
			self.friction_force_x = self.x_velo * self.mass
		else:
			self.friction_force_x = 0

		self.temp_x_friction(None)

		return -self.friction_force_x

	def friction_y(self, y_velo, prev_y, temp_friction_y):

		if abs(prev_y) > KinematicBody.MIN_Y_VELO:
			if temp_friction_y != None:
				if abs(y_velo) > KinematicBody.MIN_Y_VELO:
					self.friction_force_y = (self.mass * y_velo * temp_friction_y)
				else:
					self.friction_force_y = self.y_velo * self.mass
			else:
				if abs(y_velo) > KinematicBody.MIN_Y_VELO:
					self.friction_force_y = (self.mass * y_velo * self.constant_friction_y)
				else:
					self.friction_force_y = self.y_velo * self.mass
		elif abs(self.y_velo) > KinematicBody.MIN_Y_VELO:
			self.friction_force_y = self.y_velo * self.mass
		elif self.accel_y == 0:
			self.friction_force_y = self.y_velo * self.mass
		else:
			self.friction_force_y = 0

		self.temp_y_friction(None)

		return -self.friction_force_y

	def detect_collision(self, *args):
		KinematicCollision = False
		x_collision = False
		net_x = self.x_velo
		net_y = self.y_velo
		difference_x = self.x_velo
		difference_y = self.y_velo
		prev_difference_x = self.prev_x_velo
		prev_difference_y = self.prev_y_velo

		for body in args:
			body_parameters = body.get_body_parameters()
			super().detect_collision(body_parameters)
			material_type = body.get_material_type()
			self.sides = {"top": self.y_pos, "bottom": self.y_pos + self.height, "left": self.x_pos, "right": self.x_pos + self.width}
			body_sides = {"top": body_parameters[1], "bottom": body_parameters[1] + body_parameters[3], "left": body_parameters[0], "right": body_parameters[0] + body_parameters[2]}

			if self.collision == True:
				bodyMaterial = body.get_material_list()
				side_collisions = {	"b": abs(self.sides["bottom"] - body_sides["top"]),
								"t": abs(self.sides["top"] - body_sides["bottom"]),
								"l": abs(self.sides["left"] - body_sides["right"]),
								"r": abs(self.sides["right"] - body_sides["left"])
								}

				if type(body).__name__ !=  "KinematicBody":

					if abs(self.x_velo) > KinematicBody.MIN_BOUNCE_VELO:
						self.bounce_x = abs(self.x_velo) * body_parameters[5]
					else:
						self.bounce_x = 0

					if abs(self.y_velo) > KinematicBody.MIN_BOUNCE_VELO:
						self.bounce_y = abs(self.y_velo) * body_parameters[5]
					else:
						self.bounce_y = 0

					if self.bounce_x > body_parameters[6]:
						self.bounce_x = body_parameters[6]

					if self.bounce_y > body_parameters[6]:
						self.bounce_y = body_parameters[6]

					if material_type != "Fluid":
						if side_collisions["t"] < side_collisions["b"] and side_collisions["t"] < side_collisions["l"] and side_collisions["t"] < side_collisions["r"]:
							self.temp_max_y_vector("max", 0)
							self.set_y_pos(body_parameters[1] + body_parameters[3])
							self.temp_x_friction(body_parameters[4])
							self.accelerate(0, -self.bounce_y)
						elif side_collisions["b"] < side_collisions["t"] and side_collisions["b"] < side_collisions["l"] and side_collisions["b"] < side_collisions["r"]:	
							self.temp_max_y_vector("min", 0)				
							self.set_y_pos(body_parameters[1] - self.height)
							self.temp_x_friction(body_parameters[4])		
							self.accelerate(0, self.bounce_y)	
						elif side_collisions["l"] < side_collisions["r"] and side_collisions["l"] < side_collisions["t"] and side_collisions["l"] < side_collisions["b"]:
							self.temp_max_x_vector("min", 0)
							self.set_x_pos(body_parameters[0] + body_parameters[2])
							self.temp_y_friction(body_parameters[4])
							self.accelerate(self.bounce_x, 0)
						elif side_collisions["r"] < side_collisions["l"] and side_collisions["r"] < side_collisions["t"] and side_collisions["r"] < side_collisions["b"]:
							self.temp_max_x_vector("max", 0)
							self.set_x_pos(body_parameters[0] - self.width)
							self.temp_y_friction(body_parameters[4])
							self.accelerate(-self.bounce_x, 0)

					else:
						self.temp_x_friction(body_parameters[4])
						self.temp_y_friction(body_parameters[4])
				else:

					KinematicCollision = True
					net_x += body.get_x_velo()
					net_x += body.get_y_velo()
					difference_x -= body.get_x_velo()
					difference_y -= body.get_y_velo()
					prev_difference_x -= body.get_prev_x()
					prev_difference_y -= body.get_prev_y()

					mass = body.get_mass()
					net_mass = self.mass + mass
					self.systemic_mass = self.mass / net_mass
					systemic_mass = mass / net_mass

					if side_collisions["t"] < side_collisions["b"] and side_collisions["t"] < side_collisions["l"] and side_collisions["t"] < side_collisions["r"]:
						if body.get_y_velo() < self.prev_y_velo:
							net_y = self.y_velo + body.get_y_velo()
							difference_x = self.x_velo - body.get_x_velo()
							prev_difference_x = self.prev_x_velo - body.get_prev_x()
							self.future_y_velo = net_y * (1 - self.systemic_mass)
							self.future_y_pos = body_parameters[1] + body_parameters[3]
					elif side_collisions["b"] < side_collisions["t"] and side_collisions["b"] < side_collisions["l"] and side_collisions["b"] < side_collisions["r"]:				
						if body.get_y_velo() > self.prev_y_velo:
							net_y = self.y_velo + body.get_y_velo()
							difference_x = self.x_velo - body.get_x_velo()
							prev_difference_x = self.prev_x_velo - body.get_prev_x()
							self.future_y_velo = net_y * (1 - self.systemic_mass)
							self.future_y_pos = body_parameters[1] - self.height
					elif side_collisions["l"] < side_collisions["r"] and side_collisions["l"] < side_collisions["t"] and side_collisions["l"] < side_collisions["b"]:
						x_collision = True
						if body.get_x_velo() > self.prev_x_velo:
							net_x = self.x_velo + body.get_x_velo()
							difference_y = self.y_velo - body.get_y_velo()
							prev_difference_y = self.prev_y_velo - body.get_prev_y()		
							self.future_x_velo = net_x * (1 - self.systemic_mass)
							self.future_x_pos = body_parameters[0] + body_parameters[2]
					elif side_collisions["r"] < side_collisions["l"] and side_collisions["r"] < side_collisions["t"] and side_collisions["r"] < side_collisions["b"]:
						x_collision = True
						if body.get_x_velo() < self.prev_x_velo:
							net_x = self.x_velo + body.get_x_velo()
							difference_y = self.y_velo - body.get_y_velo()
							prev_difference_y = self.prev_y_velo - body.get_prev_y()				
							self.future_x_velo = net_x * (1 - self.systemic_mass)

		if KinematicCollision == True:
			KinematicCollision = False
			if x_collision == True:
				self.apply_force(0, self.friction_y(difference_y, prev_difference_y, body_parameters[4]))
			else:
				self.apply_force(self.friction_x(difference_x, prev_difference_x, body_parameters[4]), 0)

	def interact(self, *args):
		self.gravity()
		self.detect_collision(*args)
		self.apply_force(self.friction_x(self.x_velo, self.prev_x_velo, self.temp_friction_x), self.friction_y(self.y_velo, self.prev_y_velo, self.temp_friction_y))

	# Update postion of body with vectors
	def update(self, *args):

		self.x_velo += self.accel_x
		self.y_velo += self.accel_y

		if abs(self.x_velo) > self.max_x_velo:
			self.x_velo = self.max_x_velo * (abs(self.x_velo) / self.x_velo)
		elif self.future_x_velo != None:
			if abs(self.future_x_velo) > self.max_x_velo:
				self.future_x_velo = self.max_x_velo * (abs(self.future_x_velo) / self.future_x_velo)
				self.x_velo = self.future_x_velo + self.accel_x
			else:
				self.x_velo = self.future_x_velo + self.accel_x

		if abs(self.y_velo) > self.max_y_velo:
			self.y_velo = self.max_y_velo * (abs(self.y_velo) / self.y_velo)
		elif self.future_y_velo != None:
			if abs(self.future_y_velo) > self.max_y_velo:
				self.future_y_velo = self.max_y_velo * (abs(self.future_y_velo) / self.future_y_velo)
				self.y_velo = self.future_y_velo + self.accel_y
			else:
				self.y_velo = self.future_y_velo + self.accel_y

		if self.future_x_pos != None:
			self.x_pos = self.future_x_pos + self.x_velo
		else:
			self.x_pos += self.x_velo

		if self.future_y_pos != None:
			self.y_pos = self.future_y_pos + self.y_velo
		else:
			self.y_pos -= self.y_velo

		self.prev_y_velo = self.y_velo
		self.prev_x_velo = self.x_velo

		self.accel_x = 0
		self.accel_y = 0
		self.future_x_pos = None
		self.future_y_pos = None
		self.future_x_velo = None
		self.future_y_velo = None