# Python 2D Physics Engine #

This project is a simple 2D Physics Engine made with Python and Pygame.

It may be used to build a game later on, but for now the engine itself is still under development.

#### Bodies ####

The engine is based off of bodies, shapes with a position and size that can be collided with.

__Static Body VS Kinematic Body__

The __Static Body__ is the base class for all bodies. These bodies cannot move - they are in a fixed position. They have a material type, coefficient of friction and elastic collision energy return value.

The __Kinematic Body__ inherits from the __Static Body__. These bodies can move - They have mass, velocity, acceleration, force, coefficient of friction, gravitational acceleration, air resistance and momentum transfer (with each other)

### What Needs Work? ###

Currently, the momentum transfer is the feature that needs the most work. While it works correctly on the X axis, high velocity downwards collisions on the Y axis cause infinite energy transfer and incredibly fast oscillation of the Bodies.
