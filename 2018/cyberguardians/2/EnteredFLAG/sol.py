import angr

def main():
  proj = angr.Project("EnteredFLAG")
  initial_state = proj.factory.entry_state()
  pg = proj.factory.simgr(initial_state, veritesting=False)
  pg.explore(find=0x400df9)
  print pg
  print repr(pg.found[0].posix.dumps(0))

if __name__ == '__main__':
  main()
