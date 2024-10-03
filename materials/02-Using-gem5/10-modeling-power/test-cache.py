"""
A simple run script using a specialized CHI cache hierarchy with a power model
for the L3 cache.
This script runs a simple test with a linear generator.

> gem5 run-test.py
"""

from three_level import PrivateL1PrivateL2SharedL3CacheHierarchy

from gem5.components.boards.test_board import TestBoard
from gem5.components.memory.multi_channel import DualChannelDDR4_2400
from gem5.components.processors.linear_generator import LinearGenerator

from gem5.simulate.simulator import Simulator

# Note: hack since the stdlib doesn't support adding power models
def _instantiate(simulator):
    from m5.objects import Root
    import m5
    simulator._board._pre_instantiate()

    root = Root(
        full_system=(
            simulator._full_system
            if simulator._full_system is not None
            else simulator._board.is_fullsystem()
        ),
        board=simulator._board,
    )
    set_up_power_model(simulator._board)

    simulator._root = root
    m5.instantiate(simulator._checkpoint_path)
    simulator._instantiated = True
    simulator._board._post_instantiate()


board = TestBoard(
    generator=LinearGenerator(num_cores=4, max_addr=2**22, rd_perc=75),
    cache_hierarchy=PrivateL1PrivateL2SharedL3CacheHierarchy(
        l1d_size="32KiB",
        l1d_assoc=8,
        l1i_size="32KiB",
        l1i_assoc=8,
        l2_size="256KiB",
        l2_assoc=16,
        l3_size="2MiB",
        l3_assoc=32,
    ),
    memory=DualChannelDDR4_2400(size="2GiB"),
    clk_freq="3GHz",
)

def set_up_power_model(board):
    board.get_cache_hierarchy().add_power_model()


sim = Simulator(board)

# Note, this is a hack until we fix the interface to allow for these update
# functions.
_instantiate(sim)
sim.run()
