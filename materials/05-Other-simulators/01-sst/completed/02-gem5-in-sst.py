"""This SST configuration script demonstrates integrating gem5 as a component
within SST. The gem5 component is connected to an SST
cache and memory system thus showing how gem5 simulations and meld with SST
simulated components.

**Note**: This is just a copy of the `example.py` file in  "ext/sst/sst"
directory in the gem5 repository.

Usage
----

```bas
sst materials/05-Other-simulators/01-sst/02-gem5-in-sst.py
```

"""

import sst

from sst import UnitAlgebra

cache_link_latency = "1ps"

bbl = "riscv-boot-exit-nodisk"
cpu_clock_rate = "3GHz"
# gem5 will send requests to physical addresses of range [0x80000000, inf) to
# memory currently, we do not subtract 0x80000000 from the request's address to
# get the "real" address so, the mem_size would always be 2GiB larger than the
# desired memory size
memory_size_gem5 = "4GiB"
memory_size_sst = "6GiB"
addr_range_end = UnitAlgebra(memory_size_sst).getRoundedValue()

l1_params = {
    "access_latency_cycles" : "1",
    "cache_frequency" : cpu_clock_rate,
    "replacement_policy" : "lru",
    "coherence_protocol" : "MESI",
    "associativity" : "4",
    "cache_line_size" : "64",
    "cache_size" : "4 KiB",
    "L1" : "1",
}

# We keep a track of all the memory ports that we have.
sst_ports = {
    "system_port" : "system.system_outgoing_bridge",
    "cache_port" : "system.memory_outgoing_bridge"
}

# We need a list of ports.
port_list = []
for port in sst_ports:
    port_list.append(port)



gem5_node = sst.Component("gem5_node", "gem5.gem5Component")
gem5_node.addParams(cpu_params)

cache_bus = sst.Component("cache_bus", "memHierarchy.Bus")
cache_bus.addParams( { "bus_frequency" : cpu_clock_rate } )

# for initialization
system_port = gem5_node.setSubComponent(port_list[0], "gem5.gem5Bridge", 0)
# tell the SubComponent the name of the corresponding SimObject
system_port.addParams({ "response_receiver_name": sst_ports["system_port"]})

# SST -> gem5
cache_port = gem5_node.setSubComponent(port_list[1], "gem5.gem5Bridge", 0)
cache_port.addParams({ "response_receiver_name": sst_ports["cache_port"]})

# L1 cache
l1_cache = sst.Component("l1_cache", "memHierarchy.Cache")
l1_cache.addParams(l1_params)

# Memory
memctrl = sst.Component("memory", "memHierarchy.MemController")
# `addr_range_end` should be changed accordingly to memory_size_sst
memctrl.addParams({
    "debug" : "0",
    "clock" : "1GHz",
    "request_width" : "64",
    "addr_range_end" : addr_range_end,
})
memory = memctrl.setSubComponent("backend", "memHierarchy.simpleMem")
memory.addParams({
    "access_time" : "30ns",
    "mem_size" : memory_size_sst
})

# Connections
# cpu <-> L1
cpu_cache_link = sst.Link("cpu_l1_cache_link")
cpu_cache_link.connect(
    (cache_port, "port", cache_link_latency),
    (cache_bus, "high_network_0", cache_link_latency)
)
system_cache_link = sst.Link("system_cache_link")
system_cache_link.connect(
    (system_port, "port", cache_link_latency),
    (cache_bus, "high_network_1", cache_link_latency)
)
cache_bus_cache_link = sst.Link("cache_bus_cache_link")
cache_bus_cache_link.connect(
    (cache_bus, "low_network_0", cache_link_latency),
    (l1_cache, "high_network_0", cache_link_latency)
)
# L1 <-> mem
cache_mem_link = sst.Link("l1_cache_mem_link")
cache_mem_link.connect(
    (l1_cache, "low_network_0", cache_link_latency),
    (memctrl, "direct_link", cache_link_latency)
)

# enable Statistics
stat_params = { "rate" : "0ns" }
sst.setStatisticLoadLevel(5)
sst.setStatisticOutput("sst.statOutputTXT", {"filepath" : "./sst-stats.txt"})
sst.enableAllStatisticsForComponentName("l1_cache", stat_params)
sst.enableAllStatisticsForComponentName("memory", stat_params)
