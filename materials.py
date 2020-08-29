import colors

Colors = colors.color_list

material_list = {
	# Material Key: Material Type, Coefficient of Friction, Elastic Colission Energy Return, Max Energy Return, Y Friction Ratio
	"StandardSolid" : ["Solid", Colors["white"], 0.075, 0.25, 10],
	"KinematicSolid" : ["Solid", Colors["purple"], 0.075, 0.25, 5],
	"Player": ["Solid", Colors["gray"], 0.075, 0.25, 5],
	"Trampoline" : ["Solid", Colors["red"], 0.075, 0.8, 20],
	"Sand" : ["Solid", Colors["tan"], 0.2, 0.1, 2],
	"Water" : ["Fluid", Colors["blue"], 0.2, 0, 0],
	"Ice" : ["Solid", Colors["sky_blue"], 0.025, 0.1, 5],
	"Quicksand" : ["Fluid", Colors["orange"], 0.35, 0, 0]
}