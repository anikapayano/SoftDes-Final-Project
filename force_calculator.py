import numpy as np
from itertools import chain


class Calculator():

	def __init__(self):
		pass

	def single_force(self, ux, uy, vx, vy):
		'''
		calculates force of v onto u
		subtracts position x of v from x position of u
		subtracts y position of v from y position of u
		'''
		x_force = ux-vx
		y_force = uy-vy
		return([x_force, y_force])

	def sum_force_unit(self, information, index):
		'''information as list of lists
		calculates fx and for unit at index
		returns fx, fy'''
		force_x = 0
		force_y = 0
		current_unit = information[index]
		# Calculates forces exerted by units
		for unit in information[:-2]:
			if current_unit != unit:
				# checks if unit exists
				if unit[-1] == 1:

					# if units are on opposing teams, forces will be a vector that points away from thing
					# if units are on same team, forces will be a vector that points toward thing
					if current_unit[2] != unit[2]:
						forces = self.single_force(current_unit[0], current_unit[1], unit[0], unit[1])
					else:
						forces = self.single_force(unit[0], unit[1], current_unit[0], current_unit[1])
					force_x += forces[0]
					force_y += forces[1]

		# Calculates forces exerted by flags
		for flag in information[-2:]:
			# checks if flag and unit are on same team
			# if on same team, 
			if current_unit[2] != flag[2]:
				forces = self.single_force(unit[0], unit[1], current_unit[0], current_unit[1])
				force_x += forces[0]
				force_y += forces[1]

		return force_x, force_y
		

	def sum_forces_all(self, information):
		'''information is list of lists'''
		final_forces = []
		for i, thing in enumerate(information):
			if i < 6:
				final_forces.append(self.sum_force_unit(information, i))

		final_forces = list(chain(*final_forces))
		return(final_forces)

