"""
This example demonstrates how to set up a simple gem5 simulation using
the prebuilt x86 demo board to run a static 'hello world' binary. The
steps include:

1. Importing necessary gem5 modules.
2. Creating an instance of the X86DemoBoard.
3. Setting a 'hello world' workload on the board.
4. Running the simulation.
"""
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400

from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA

from gem5.resources.resource import obtain_resource

from gem5.simulate.simulator import Simulator

memory = SingleChannelDDR4_2400(size="2GiB")

caches = PrivateL1SharedL2CacheHierarchy(
    l1d_size="32KiB",
    l1d_assoc=8,
    l1i_size="32KiB",
    l1i_assoc=8,
    l2_size="256KiB",
    l2_assoc=16,
)

processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING, num_cores=1, isa=ISA.X86
)

board = SimpleBoard(
    processor=processor,
    memory=memory,
    cache_hierarchy=caches,
    clk_freq="3GHz",
)

board.set_se_binary_workload(obtain_resource("x86-hello64-static"))

simulator = Simulator(board=board)
simulator.run()
