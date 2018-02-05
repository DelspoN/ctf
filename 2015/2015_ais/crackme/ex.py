import angr

p = angr.Project("crackme", load_options={'auto_load_libs':False})
argv1 = angr.claripy.BVS("argv1",100*8)
path1 = p.factory.path(args=['./crackme1',argv1])
ex = p.factory.path_group(path1)
ex.explore(find=0x400602, avoid=0x40060E)
print ex.found[0].state.se.any_str(argv1)

