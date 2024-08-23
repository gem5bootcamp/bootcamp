"""
A simple run script using a specialized CHI cache hierarchy.
This script runs a simple test with a linear generator.

> gem5 run-test.py
"""

from hierarchy import PrivateL1SharedL2CacheHierarchy

from gem5.components.boards.test_board import TestBoard
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.linear_generator import LinearGenerator

from gem5.simulate.simulator import Simulator

board = TestBoard(
    generator=LinearGenerator(num_cores=4, max_addr=2**22, rd_perc=75),
    cache_hierarchy=PrivateL1SharedL2CacheHierarchy(
        l1_size="32KiB",
        l1_assoc=8,
        l2_size="2MiB",
        l2_assoc=16,
    ),
    memory=SingleChannelDDR4_2400(size="2GiB"),
    clk_freq="3GHz",
)

sim = Simulator(board)
sim.run()
