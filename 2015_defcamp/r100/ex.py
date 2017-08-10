import angr

project = angr.Project("./r100", load_options={'auto_load_libs':False})
ex = project.surveyors.Explorer(find=(0x400849),avoid=(0x400855))
ex.run()

print ex.found[0].state.posix.dumps(0)
