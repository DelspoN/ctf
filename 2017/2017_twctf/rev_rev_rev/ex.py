import angr

project = angr.Project("./rev_rev_rev", load_options={'auto_load_libs':False})
path_group = project.factory.path_group()
path_group.explore(find=0x08048679,avoid=0x0804868B)

print path_group.found[0].state.posix.dumps(0)
