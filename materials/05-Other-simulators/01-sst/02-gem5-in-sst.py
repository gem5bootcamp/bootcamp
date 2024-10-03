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

cpu_params = {
    "frequency": cpu_clock_rate,
    "cmd": " ../../configs/example/sst/riscv_fs.py"
            + f" --cpu-clock-rate {cpu_clock_rate}"
            + f" --memory-size {memory_size_gem5}",
    "debug_flags": "",
    "ports" : " ".join(port_list)
}
