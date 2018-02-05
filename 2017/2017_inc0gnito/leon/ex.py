import angr

project = angr.Project("./leon", load_options={'auto_load_libs':False})
path_group = project.factory.path_group()
path_group.explore(find=0x400867,avoid=0x400873)

print path_group.found[0].state.posix.dumps(0)
