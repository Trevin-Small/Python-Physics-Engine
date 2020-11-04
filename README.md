# Python Physics Engine (2D)#

This project is a simple 2D Physics Engine made with Python and Pygame.

It may be used to build a game later on, but for now the engine itself is still under development.


![Physics Engine Running](https://github.com/Trevin-S/Python-Physics-Engine/blob/master/readme_images/engineRunning.png)


### Bodies ###

The engine is based off of bodies, shapes with a position and size that can be collided with.

__Static Body VS Kinematic Body__

The __Static Body__ is the base class for all bodies. These bodies cannot move - they are in a fixed position. They have a material type, coefficient of friction and elastic collision energy return value.

The __Kinematic Body__ inherits from the __Static Body__. These bodies can move - They have mass, velocity, acceleration, force, coefficient of friction, gravitational acceleration, air resistance and momentum transfer (with each other)

### What Comes Next? ###

The collision system needs to be completely rewritten. Overtime it has become spaghetti-code that is increasinlgy hard to debug, and the way it is structured could be improved. Currently, collisions are a method of the bodies themselves, which was a poor choice. Instead, body interactions/collisions should be its own class, taking in two bodies as parameters and dealing with both of them at synchronously in an organized fashion.


### Possible Future Features ###

__Body Linking__ 

__Rotational Motion__ 

__Ramps__ 

__Circular Collision Masks__ 
