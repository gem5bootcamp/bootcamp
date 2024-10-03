"""
This script is used for running a traffic generator connected to the
DRAMSim3 simulator.

"""

from gem5.components.boards.test_board import TestBoard
from gem5.components.memory.dramsim_3 import SingleChannelHBM
from gem5.components.processors.linear_generator import LinearGenerator
from gem5.simulate.simulator import Simulator

memory = SingleChannelHBM(size="1GiB")

generator = LinearGenerator(
    duration="250us",
    rate="40GiB/s",
    num_cores=1,
    max_addr=memory.get_size(),
)

board = TestBoard(
    clk_freq="3GHz", generator=generator, memory=memory, cache_hierarchy=None
)

simulator = Simulator(board=board)
simulator.run()
