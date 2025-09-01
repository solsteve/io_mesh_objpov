#/ ====================================================================== BEGIN FILE =====
#/ **                                  M A K E F I L E                                  **
#/ =======================================================================================
#/ **                                                                                   **
#/ **  Copyright (c) 2021, Stephen W. Soliday                                           **
#/ **                      stephen.soliday@trncmp.org                                   **
#/ **                      http://research.trncmp.org                                   **
#/ **                                                                                   **
#/ **  -------------------------------------------------------------------------------  **
#/ **                                                                                   **
#/ **  This program is free software: you can redistribute it and/or modify it under    **
#/ **  the terms of the GNU General Public License as published by the Free Software    **
#/ **  Foundation, either version 3 of the License, or (at your option)                 **
#/ **  any later version.                                                               **
#/ **                                                                                   **
#/ **  This program is distributed in the hope that it will be useful, but WITHOUT      **
#/ **  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS    **
#/ **  FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.   **
#/ **                                                                                   **
#/ **  You should have received a copy of the GNU General Public License along with     **
#/ **  this program. If not, see <http://www.gnu.org/licenses/>.                        **
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

clean:
	@echo Done $@

fullclean: clean
	rm -f *~
	@echo Done $@

distclean: fullclean
	@echo Done $@

install:
	mkdir -p ../addon/io_mesh_objpov
	/bin/cp -f *.py  ../addon/io_mesh_objpov
	/bin/cp -f *.txt ../addon/io_mesh_objpov

#/ =======================================================================================
#/ **                                  M A K E F I L E                                  **
#/ =========================================================================== END FILE ==
