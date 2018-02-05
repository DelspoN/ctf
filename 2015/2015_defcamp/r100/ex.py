import angr

project = angr.Project("./r100", load_options={'auto_load_libs':False})
path_group = project.factory.path_group()
path_group.explore(find=0x400849,avoid=0x400855)

print path_group.found[0].state.posix.dumps(0)
