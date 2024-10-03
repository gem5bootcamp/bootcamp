"""
This gem5 configuation script creates a simple board to run an ARM
"hello world" binary.

This is to be tested by the testlib framework via the test_example.py script.
"""

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires

import argparse

requires(isa_required=ISA.ARM)

cache_hierarchy = NoCache()
memory = SingleChannelDDR3_1600(size="32MiB")
processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, isa=ISA.ARM, num_cores=1)

parser = argparse.ArgumentParser()
parser.add_argument("--to-print", type=str,
                    help="Optional to print at the end of the simulation.")
args = parser.parse_args()


board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)


board.set_se_binary_workload(
    obtain_resource("arm-hello64-static")
)

simulator = Simulator(board=board)
simulator.run()

if args.to_print:
    print(args.to_print)
