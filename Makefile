#/ ====================================================================== BEGIN FILE =====
#/ **                      M O O N B A S E   T R A N Q U I L I T Y                      **
#/ =======================================================================================
#/ **                                                                                   **
#/ **  Copyright (c) 1977-2021, Stephen W. Soliday                                      **
#/ **                           stephen.soliday@trncmp.org                              **
#/ **                           http://research.trncmp.org                              **
#/ **                                                                                   **
#/ **  -------------------------------------------------------------------------------  **
#/ **                                                                                   **
#/ **  This file is part of the Moonbase Tranquility research project.                  **
#/ **  This project is in a development phase. This file is not free software; you may  **
#/ **  not redistribute it and/or modify it. No part of this research has been publicly **
#/ **  distributed. The author retains ALL RIGHTS to these files.                       **
#/ **                                                                                   **
#/ ----- Modification History ------------------------------------------------------------
#/
#/  @file Makefile
#/   Provides the build for the Blender addon.
#/
#/  @author Stephen W. Soliday
#/  @date 2021-Mar-06
#/
#/ =======================================================================================

all:
	ls -lpa

install:
	make -C src $@

clean:
	make -C src $@

fullclean: clean
	rm -f *~
	make -C src $@

distclean: fullclean
	make -C src $@

#/ =======================================================================================
#/ **                      M O O N B A S E   T R A N Q U I L I T Y                      **
#/ =========================================================================== END FILE ==
