#/ ====================================================================== BEGIN FILE =====
#/ **                                   T L O G G E R                                   **
#/ =======================================================================================
#/ **                                                                                   **
#/ **  Copyright (c) 2013, Stephen W. Soliday                                           **
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
"""
Author: Stephen W. Soliday
Date:   2013-Jul-14
"""
#/ =======================================================================================

import sys
import inspect, datetime

UNSET    = 0
CRITICAL = 1
ERROR    = 2
WARNING  = 3
INFO     = 4
DEBUG    = 5

#/ =======================================================================================
class AbortHandler:
    #/ -----------------------------------------------------------------------------------
    def __init__( self, rep_handler = None ):
        #/ -------------------------------------------------------------------------------
        if ( rep_handler ):
            self.abortFunction = rep_handler
        else:
            self.abortFunction = self.default_handler_function

    #/ ===================================================================================
    def handle( self, n ):
        #/ -------------------------------------------------------------------------------
        if ( not self.abortFunction ):
            raise Exception( "No handler has been registered" )
        self.abortFunction( n )

    #/ ===================================================================================
    def default_handler_function( self, n ):
        #/ -------------------------------------------------------------------------------
        sys.stderr.write("Performing a default TLogger abort with exit code: %d\n" % (n,))
        sys.exit(n)

#/ =======================================================================================
def TimeStamp():
    #/ -----------------------------------------------------------------------------------
    return datetime.datetime.now().strftime("%Y%m.%d %H:%M:%S.%f")

#/ =======================================================================================
def LOCATION( level = 1 ):
    #/ -----------------------------------------------------------------------------------
    try:
        sobj     = inspect.stack()
        temp     = sobj[level]
        filename = temp[1].split('/')[-1:][0]
        lineno   = temp[2]
        funcname = temp[3]
        return "%s: %s: %d" % (filename, funcname, lineno)
    except:
        pass
    return "?: ?: ?"

#/ =======================================================================================
class getInstance:
    #/ -----------------------------------------------------------------------------------

    #/ ===================================================================================
    class __impl:
        #/ -------------------------------------------------------------------------------

        #/ ===============================================================================
        def __init__(self):
            #/ ---------------------------------------------------------------------------
            self.console_level  = INFO;
            self.write_level    = WARNING;
            self.logfile_name   = None;
            self.abort_level    = CRITICAL;
            self.abort_handler = AbortHandler( )
            self.flag = True

            self.code = { 0:UNSET,    'UNSET':    UNSET, 
                          1:CRITICAL, 'CRITICAL': CRITICAL,
                          2:ERROR,    'ERROR':    ERROR,
                          3:WARNING,  'WARNING':  WARNING,
                          4:INFO,     'INFO':     INFO,
                          5:DEBUG,    'DEBUG':    DEBUG }

        #/ ===============================================================================
        def on(self):
            #/ ---------------------------------------------------------------------------
            """ Set debugging on without changing levels """
            #/ ---------------------------------------------------------------------------
            self.flag = True

        #/ ===============================================================================
        def off(self):
            #/ ---------------------------------------------------------------------------
            """ Set debugging off without changing levels """
            #/ ---------------------------------------------------------------------------
            self.flag = False

        #/ ===============================================================================
        def message( self, level, str1, str2 = None ):
            #/ ---------------------------------------------------------------------------
            """ """
            #/ ---------------------------------------------------------------------------
            tag = 'UCEWID'

            if ( self.flag ):
                if ( None == str2 ):
                    msg = "[%s] **%s** %s" % ( TimeStamp(), tag[level%6],
                                               str1, )
                else:
                    msg = "[%s] **%s** ( %s ) %s" % ( TimeStamp(), tag[level%6],
                                                      str1, str2, )
                #/ ----- console display (stderr) ----------------------------------------

                if (level <= self.console_level):
                    sys.stderr.write( "%s\n" % ( msg, ) )

                #/ ----- log to a file -------------------------------------------------------

                if ( self.logfile_name ):
                    if ( level <= self.write_level ):
                        try:
                            open( self.logfile_name,'a' ).write( "%s\n" % ( msg, ) )
                        except IOError:
                            msg = "[%s] **W** Failed to open log file: %s" % ( TimeStamp(),
                                                                               self.logfile_name )

	        #/ ----- abort the program if this level is reached --------------------------

                if ( level <= self.abort_level ):
                    self.abort_handler.handle( level )

        #/ ===============================================================================
        def critical(self, str1, str2 = None ):
            #/ ---------------------------------------------------------------------------
            """ Display critical message text with a date/time stamp """
            #/ ---------------------------------------------------------------------------
            self.message( CRITICAL, str1, str2 )

        #/ ===============================================================================
        def error(self, str1, str2 = None ):
            #/ ---------------------------------------------------------------------------
            """ Display error message text with a date/time stamp """
            #/ ---------------------------------------------------------------------------
            self.message( ERROR, str1, str2 )

        #/ ===============================================================================
        def warning(self, str1, str2 = None ):
            #/ ---------------------------------------------------------------------------
            """ Display warning message text with a date/time stamp """
            #/ ---------------------------------------------------------------------------
            self.message( WARNING, str1, str2 )

        #/ ===============================================================================
        def warn(self, str1, str2 = None ):
            #/ ---------------------------------------------------------------------------
            """ Display warning message text with a date/time stamp """
            #/ ---------------------------------------------------------------------------
            self.message( WARNING, str1, str2 )

        #/ ===============================================================================
        def info(self, str1, str2 = None ):
            #/ ---------------------------------------------------------------------------
            """ Display info message text with a date/time stamp """
            #/ ---------------------------------------------------------------------------
            self.message( INFO, str1, str2 )

        #/ ===============================================================================
        def debug(self, str1, str2 = None ):
            #/ ---------------------------------------------------------------------------
            """ Display debug message text with a date/time stamp """
            #/ ---------------------------------------------------------------------------
            self.message( DEBUG, str1, str2 )

        #/ ===============================================================================
        def setAbortLevel(self, n):
            #/ ---------------------------------------------------------------------------
            """ Set the minimum level that will cause a sys.exit() """
            #/ ---------------------------------------------------------------------------
            self.abort_level = self.code[n]

        #/ ===============================================================================
        def registerAbortHandler( self, ah, new_level = UNSET ):
            #/ ---------------------------------------------------------------------------
            """ Set the function to call for aborting """
            #/ ---------------------------------------------------------------------------
            self.abort_handler = ah
            if ( UNSET < new_level ):
                self.setAbortLevel( new_level )

        #/ ===============================================================================
        def setConsoleLevel(self, n):
            #/ ---------------------------------------------------------------------------
            """ set the minimum level that will display on the screen """
            #/ ---------------------------------------------------------------------------
            self.console_level = self.code[n]

        #/ ===============================================================================
        def setWriteLevel(self, n):
            #/ ---------------------------------------------------------------------------
            """ set the minimum level that will write to the log file """
            #/ ---------------------------------------------------------------------------
            self.write_level = self.code[n]

        #/ ===============================================================================
        def setLogfile(self, fspc, new_level = UNSET):
            #/ ---------------------------------------------------------------------------
            """ set the name of the log file """
            #/ ---------------------------------------------------------------------------
            self.logfile_name = fspc
            if ( UNSET < new_level ):
                self.setWriteLevel( new_level )

    #/ ===================================================================================
    # storage for the instance reference
    __instance = None

    #/ ===================================================================================
    def __init__(self):
        #/ -------------------------------------------------------------------------------
        # Check whether we already have an instance
        if getInstance.__instance is None:
            # Create and remember instance
            getInstance.__instance = getInstance.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_getInstance__instance'] = getInstance.__instance

    #/ ===================================================================================
    def __getattr__(self, attr):
        #/ -------------------------------------------------------------------------------
        return getattr(self.__instance, attr)

    #/ ===================================================================================
    def __setattr__(self, attr, value):
        #/ -------------------------------------------------------------------------------
        return setattr(self.__instance, attr, value)

#/ =======================================================================================
#/ **                                   T L O G G E R                                   **
#/ ======================================================================== END FILE =====
