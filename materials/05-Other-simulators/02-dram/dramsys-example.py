"""
This script is used for running a traffic generator connected to the
DRAMSys simulator.

**Important Note**: DRAMSys must be compiled into the gem5 binary to use the
DRRAMSys simulator. Please consult 'ext/dramsys/README' on how to compile
correctly. If this is not done correctly this script will run with error.
"""

from gem5.components.boards.test_board import TestBoard
from gem5.components.memory.dramsys import DRAMSysMem
from gem5.components.processors.linear_generator import LinearGenerator
from gem5.simulate.simulator import Simulator

memory = DRAMSysMem(
    configuration="/workspaces/2024/gem5/ext/dramsys/DRAMSys/configs/ddr4-example.json",
    recordable=True,
    resource_directory="/workspaces/2024/gem5/ext/dramsys/DRAMSys/configs",
    size="4GiB",
)

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
