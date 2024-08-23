# Copyright (c) 2024 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# system components
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy

# simulation components
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import BinaryResource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.isas import ISA
from pathlib import Path

import m5

from m5.objects import LocalInstTracker, GlobalInstTracker

'''

Usage:

/workspaces/2024/gem5/build/X86/gem5.fast -re --outdir=simple-sim-m5out simple-sim.py

'''


binary_path = Path("/workspaces/2024/materials/03-Developing-gem5-models/09-extending-gem5-models/simple-omp-workload/simple_workload")


cache_hierarchy = PrivateL1CacheHierarchy(
    l1d_size="64KiB",
    l1i_size="64KiB",
)

memory = SingleChannelDDR4_2400("1GiB")

processor = SimpleProcessor(
    cpu_type = CPUTypes.TIMING,
    num_cores = 8,
    isa = ISA.X86
)

global_inst_tracker = GlobalInstTracker(
    inst_threshold = 100000
)
all_trackers = []

for core in processor.get_cores():
    tracker = LocalInstTracker(
        global_inst_tracker = global_inst_tracker,
        start_listening = False,
    )
    core.core.probeListener = tracker
    all_trackers.append(tracker)


board = SimpleBoard(
    clk_freq="1GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

board.set_se_binary_workload(
    binary = BinaryResource(
        local_path=binary_path.as_posix()
    )
)

def workbegin_handler():
    print("Reached workbegin")
    print("Dump and reset stats")
    m5.stats.reset()
    print("Start listening for instructions")
    for tracker in all_trackers:
        tracker.startListening()
    yield False

def workend_handler():
    print("Reached workend")
    yield False

def max_inst_handler():
    print("Reached MAX_INSTS")
    print("Exiting simulation")
    yield True

simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.MAX_INSTS: max_inst_handler(),
        ExitEvent.WORKBEGIN: workbegin_handler(),
        ExitEvent.WORKEND: workend_handler(),
    }
)

simulator.run()
print("Simulation Done")

