"""
This script correlates with the slides on MemCtrl() and MemInterface().

This script currently has no memory system.

Add a memory controller and memory interface to the system.
Connect the memory controller to the memory bus.

to run this script, use the following command:
$ gem5/build/NULL/gem5.opt /workspaces/2024/materials/02-Using-gem5/\
06-memory/blank_memory.py


"""
# import the m5 (gem5) library created when gem5 is built
import m5
# import all of the SimObjects
from m5.objects import *
from m5.util.convert import *

import argparse
import math


# Helper Functions
def createLinearTraffic(tgen):
    yield tgen.createLinear(1_000_000_000,
                            0,
                            512_000_000,
                            64,
                            12000,
                            12000,
                            60, 0)
    yield tgen.createExit(0)

# create the system we are going to simulate
system = System()

# Set the clock fequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MiB')] # Create an address range
addr_range = system.mem_ranges[0]

system.tgen = PyTrafficGen() # Create a traffic generator

system.membus = SystemXBar(width = 64, max_routing_table_size = 16777216)

system.tgen.port = system.membus.cpu_side_ports

## insert memory controller and interface here


##


root = Root(full_system = False, system = system)
# instantiate all of the objects we've created above
m5.instantiate()

system.tgen.start(createLinearTraffic(system.tgen))


print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))










