# stdlib / getting started commands
'''
gem5-mesi materials/archive/isca24/01-basic.py
'''

'''
gem5 materials/archive/isca24/02-components.py
'''

'''
gem5 materials/archive/isca24/03-processor.py
'''

# Sim Objects commands
'''
scons build/NULL/gem5.opt -j$(nproc)
'''

'''
cp -r materials/03-developing-gem5-models/02-debugging-gem5/step-1/bootcamp gem5/src/
'''

'''
build/NULL/gem5.opt src/bootcamp/hello-sim-object/run_hello.py
'''

'''
build/NULL/gem5.opt --debug-flags=HelloExampleFlag src/bootcamp/hello-sim-object/run_hello.py
'''
