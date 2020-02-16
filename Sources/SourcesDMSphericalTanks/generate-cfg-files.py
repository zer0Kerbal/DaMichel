#!/bin/env python
import rocket
import os, sys, string, math

template = """
PART
{
	// --- general parameters ---
	name = DM-SphericalTank-125-${MODEL_ID}
	module = Part
	author = DaMichel

	// --- asset parameters ---
	MODEL
	{
		model = DMTanks/Parts/sphericalTank-c125-r${MODEL_ID}
		scale = 1.0, 1.0, 1.0
	}
	scale = 1
	rescaleFactor = 1

	// --- node definitions ---
	node_stack_top = 0.0, ${Y_OFFSET}, 0.0, 0.0, 1.0, 0.0, 1
	node_stack_bottom = 0.0, -${Y_OFFSET}, 0.0, 0.0, 1.0, 0.0, 1
	node_attach = ${RADIUS}, 0.0, 0.0, 1.0, 0.0, 0.0, 1

	// --- editor parameters ---
	cost = 4000
	TechRequired = ${TECH}
	entryCost = 4000
	category = Propulsion
	subcategory = 0
	title = KIS-1250-${NAME} Spherical Fuel Tank
	manufacturer = Kichel Space Travel Supplies
	description = A 1.25m base ${MASS}t spherical tank!

	// attachment rules: stack, srfAttach, allowStack, allowSrfAttach, allowCollision
	attachRules = 1,1,1,1,0

	// --- standard part parameters ---
	mass = ${DRY_MASS}
	dragModelType = default
	maximum_drag = 0.3
	minimum_drag = 0.25
	angularDrag = 2
	crashTolerance = 6
	breakingForce = 200
	breakingTorque = 200
	maxTemp = 1450

	RESOURCE
	{
		name = LiquidFuel
		amount = ${LF_FUEL_UNITS}
		maxAmount = ${LF_FUEL_UNITS}
	}

	RESOURCE
	{
		name = Oxidizer
		amount = ${O_FUEL_UNITS}
		maxAmount = ${O_FUEL_UNITS}
	}
}
"""

density = 5./rocket.sv(1.11)

def round2(x):
  return round(x,-int(math.floor(math.log10(x))))

tankdata = [
  ('55', 0.55, 0.68, 'basicRocketry',0.6125,'0055'),
  ('70', 0.7, 0.84, 'start',1.25,'0070'),
  ('88', 0.88, 1.02, 'basicRocketry',2.5,'0088'),
  ('111', 1.11, 1.24, 'advRocketry',5,'0111'),
  ('140', 1.4, 1.53, 'advConstruction',10,'0140'),
]
for id, r, yoffset, tech, mfuel, name in tankdata:
  #real_mfuel = rocket.sv(r)*density
  mdry  = rocket.mdry_mfuel_ratio*mfuel
  mdry  = round2(mdry)
  lf_units = rocket.lf_fraction*rocket.fuel_count_per_mass*mfuel
  oxi_units = (1.-rocket.lf_fraction)*rocket.fuel_count_per_mass*mfuel
  s = string.Template(template).substitute(dict(
    MODEL_ID = id,
    TECH = tech,
    Y_OFFSET = yoffset,
    RADIUS = r,
    MASS = mfuel,
    DRY_MASS = ('%.03f' % mdry),
    LF_FUEL_UNITS = int(round(lf_units)),
    O_FUEL_UNITS = int(round(oxi_units)),
    NAME = name
  ))
  print id, 'vfuel = ',lf_units, 'dry mass = ', mdry, ' fuel mass =', mfuel
  with open('../KSPGamedata/MWTanks/Parts/c125-r%s-SphericalTank.cfg' % name,'w') as f:
    f.write(s)
