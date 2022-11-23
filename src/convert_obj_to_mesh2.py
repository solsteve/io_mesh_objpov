#!/usr/bin/env python3
#/ ====================================================================== BEGIN FILE ====X
#/ **                      C O N V E R T _ O B J _ T O _ M E S H 2                      **
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
#/ @brief   .
#/
#/ @details Provides interface and methods for
#/
#/ @author  Stephen W. Soliday
#/ @date    2021-Feb-07
#/
#/ =======================================================================================

import sys, os, time
from . import TLogger
logger = TLogger.getInstance()

#/ =======================================================================================
def NameOf( name, prefix=None ):
    #/ -----------------------------------------------------------------------------------

    fname = name.replace(' ','').replace('.','').replace('-','').replace('+','').strip()

    if ( None == prefix ):
        return fname

    return '%s_%s' % (prefix, fname,)


#/ =======================================================================================
def RGB( rgb ):
    #/ -----------------------------------------------------------------------------------
    return [ float(rgb[0]), float(rgb[1]), float(rgb[2]) ]


#/ =======================================================================================
class Mesh:
    #/ -----------------------------------------------------------------------------------
    def __init__( self, name ):
        #/ -------------------------------------------------------------------------------
        #print( '*** New Mesh:', name )
        self.name     = NameOf(name)
        self.vertex   = []
        self.normal   = []
        self.uv       = []
        self.face     = []
        self.material = None
        self.smooth   = False

        self.materials       = []
        self.materials_index = -1

    #/ ===================================================================================
    def addMaterial( self, name ):
        #/ -------------------------------------------------------------------------------
        self.materials.append( NameOf( name ) )
        self.materials_index += 1
        return self.materials_index
        

    #/ ===================================================================================
    def write( self, fp, mat ):
        #/ -------------------------------------------------------------------------------

        has_image = False
        for key in self.materials:
            if ( mat[key].isImage() ):
                has_image = True

        if ( has_image ):
            print( "one of the %d textures is an image" % ( len(self.materials), ) )
        
        fp.write('// =======================================================================================\n' )
        fp.write( '#declare %s = mesh2 {\n' % ( self.name, ) )
        fp.write('  // -------------------------------------------------------------------------------------\n' )

        #/ ----- write vectors -----------------------------------------------
        
        fp.write( '  vertex_vectors {\n    %d,\n' % (len(self.vertex),) )
        for i in range(len(self.vertex)):
            x = self.vertex[i][0]
            y = self.vertex[i][1]
            z = self.vertex[i][2]
            fp.write( '    <%f,%f,%f>, // %d\n' % ( x,y,z,i ) )
        fp.write( '  }\n\n' )

        if ( 0 < len(self.normal) ):
            fp.write( '  normal_vectors {\n    %d,\n' % (len(self.normal),) )
            for i in range(len(self.normal)):
                nx = self.normal[i][0]
                ny = self.normal[i][1]
                nz = self.normal[i][2]
                fp.write( '    <%f,%f,%f>, // %d\n' % ( nx,ny,nz,i ) )
            fp.write( '  }\n\n' )

        if ( 0 < len(self.normal) ):
            fp.write( '  uv_vectors {\n    %d,\n' % (len(self.uv),) )
            for i in range(len(self.uv)):
                s = self.uv[i][0]
                t = self.uv[i][1]
                fp.write( '    <%f,%f>, // %d\n' % ( s,t,i ) )
            fp.write( '  }\n\n' )

        #/ ----- write lists -------------------------------------------------

        if ( 1 < len(self.materials) ):
            fp.write( '  texture_list {\n    %d,\n' % (len(self.materials),) )
            for mat_key in self.materials:
                fp.write( '    texture { %s }\n' % (mat[mat_key].name,) )
            fp.write( '  }\n\n' )
        
        #/ ----- write indices -----------------------------------------------
        

        fp.write( '  face_indices {\n    %d,\n' % (len(self.face),) )

        if (( has_image ) or ( 1 == len(self.materials) )):
            for i in range(len(self.face)):
                v0 = self.face[i]['v'][0]
                v1 = self.face[i]['v'][1]
                v2 = self.face[i]['v'][2]
                fp.write( '    <%d,%d,%d>,\n' % (v0, v1, v2) )
        else:
            for i in range(len(self.face)):
                v0 = self.face[i]['v'][0]
                v1 = self.face[i]['v'][1]
                v2 = self.face[i]['v'][2]
                m  = self.face[i]['m']
                fp.write( '    <%d,%d,%d>,%d\n' % (v0, v1, v2, m) )

        fp.write( '  }\n\n' )




        
        fp.write( '  normal_indices {\n    %d,\n' % (len(self.face),) )
        for i in range(len(self.face)):
            v0 = self.face[i]['n'][0]
            v1 = self.face[i]['n'][1]
            v2 = self.face[i]['n'][2]
            fp.write( '    <%d,%d,%d>,\n' % (v0, v1, v2) )
        fp.write( '  }\n\n' )

        fp.write( '  uv_indices {\n    %d,\n' % (len(self.face),) )
        for i in range(len(self.face)):
            v0 = self.face[i]['t'][0]
            v1 = self.face[i]['t'][1]
            v2 = self.face[i]['t'][2]
            fp.write( '    <%d,%d,%d>,\n' % (v0, v1, v2) )
        fp.write( '  }\n\n' )

        if ( has_image ):
            fp.write( '  uv_mapping' )
            fp.write( '  texture { %s }\n' % ( self.materials[0] ) )
        elif ( 1 == len(self.materials) ):
            fp.write( '  texture { %s }\n' % ( self.materials[0] ) )

        fp.write( 'scale <-1,1,1>\n' )
        fp.write( '} // end mesh2 %s\n\n' % (self.name,) )


#/ =======================================================================================
class Material:
    #/ -----------------------------------------------------------------------------------
    """
    Ilumination Model:
    0. Color on and Ambient off
    1. Color on and Ambient on
    2. Highlight on
    3. Reflection on and Ray trace on
    4. Transparency: Glass on, Reflection: Ray trace on
    5. Reflection: Fresnel on and Ray trace on
    6. Transparency: Refraction on, Reflection: Fresnel off and Ray trace on
    7. Transparency: Refraction on, Reflection: Fresnel on and Ray trace on
    8. Reflection on and Ray trace off
    9. Transparency: Glass on, Reflection: Ray trace off
    10. Casts shadows onto invisible surfaces
    """
    #/ -----------------------------------------------------------------------------------
    def __init__( self, name ):
        #/ -------------------------------------------------------------------------------
        self.name = NameOf(name)
        self.ambient      = [ 1.0, 1.0, 1.0 ]
        self.difuse       = [ 1.0, 1.0, 1.0 ]
        self.specular     = [ 1.0, 1.0, 1.0 ]
        self.specular_exp = 1.0
        self.opaque       = 1.0
        self.trans_filter = [ 1.0, 1.0, 1.0 ]
        self.refraction   = 0.0
        self.emissive     = 0.0
        self.uvimage      = None
        self.model        = 0

        
    #/ ===================================================================================
    def isImage( self ):
        #/ -------------------------------------------------------------------------------
        return ( None != self.uvimage )

    
    #/ ===================================================================================
    def write( self, fp, local=False ):
        #/ -------------------------------------------------------------------------------

        if ( local ):
            fp.write( '  #local ' )
        else:
            fp.write( '#declare ' )

        fp.write( ' %s = texture {\n' % (self.name,) )

        if ( self.isImage() ):
            img_ext = self.uvimage.split('.')[-1]
            fp.write('  pigment {\n')
            fp.write('    image_map { %s "%s" }\n' % (img_ext, self.uvimage, ) )
            fp.write('  }\n')

        else:
    
            fp.write( '  pigment {\n' )
            fp.write( '  color rgb <%f,%f,%f>\n' % (
                self.difuse[0], self.difuse[1], self.difuse[2], ) )
            fp.write( '  }\n' )
        
        fp.write( '} // end texture %s\n\n' % (self.name,) )

#/ =======================================================================================
def ParseMaterialFile( mtr_filename, mat_dict ):
    #/ -----------------------------------------------------------------------------------
    #/ https://en.wikipedia.org/wiki/Wavefront_.obj_file
    #/ -----------------------------------------------------------------------------------
        
    fp = open( mtr_filename, 'r' )

    mat = None
    
    for raw in fp:
        line = raw.strip().split()
        if ( 0 < len(line) ):
            key = line[0].strip()
            if ( 'newmtl' == key ):
                mat = Material( line[1] )
                mat_dict[ mat.name ] = mat
            
            elif ( 'Ka' == key ): #/ Ambient color
                mat.ambient = RGB( line[1:4] )
                
            elif ( 'Kd' == key ): #/ Difuse color
                mat.difuse = RGB( line[1:4] )
                
            elif ( 'Ks' == key ): #/ Specular color
                mat.specular = RGB( line[1:4] )

            elif ( 'Ns' == key ): #/ Specular exponent
                mat.specular_exp = float( line[1] )

            elif ( 'd' == key ): #/ opaqueness
                mat.opaque = float( line[1] )
            
            elif ( 'Tr' == key ): #/ transparent
                 mat.opaque = 1.0 - float( line[1] )

            elif ( 'Tf' == key ): #/ transmision fileter
                 mat.trans_filter = RGB( line[1:4] )

            elif ( 'Ni' == key ): #/ index of refraction (optical density)
                mat.refraction = float( line[1] )

            elif ( 'illum' == key ): #/ Ilumination model
                mat.model = int( line[1] );

            elif ( 'map_Kd' == key ): #/ Ambient texture image
                mat.uvimage = line[1].strip()

            elif ( 'Ke' == key ): #/ comment line
                mat.emissive = float( line[1] )

            #elif ( 'Pr' == key ): #/ roughness
            #    mat.roughness = float( line[1] )

            #elif ( 'Pm' == key ): #/ metalic
            #    mat.metalic = float( line[1] )

            elif ( '#' == key ): #/ comment line
                pass

            else:
                print( '\nFailed material key=', key, ' val=', line[1:], '\n\n' )


#/ =======================================================================================
def DisplayLicense( fp ):
    #/ -----------------------------------------------------------------------------------
    import os

    dir = os.sep.join( __file__.split( os.sep )[:-1] )
    
    fspc = '%s/license.txt' % (dir,)

    try:
        file = open( fspc, 'r' )
        fp.write( '//\n// ---------------------------------------------------------------------------------------\n' )
        for line in file:
            fp.write( '// %s' % (line,) )
        file.close()
        fp.write( '// ---------------------------------------------------------------------------------------\n' )
    except IOError:
        pass

#/ =======================================================================================
def PovRayHeader( fp, show=False ):
    #/ -----------------------------------------------------------------------------------
    tm = time.gmtime()

    fp.write('// ====================================================================== BEGIN FILE =====\n' )

    if ( show ):
        fp.write( '//\n// Copyright %04d\n' % (tm.tm_year, ) )
        DisplayLicense(fp)

    fp.write("""//
// Created by: Blender AddOn: io_mesh_povray
// Date:       %s
// 
// =======================================================================================
""" % (time.asctime(tm),) )


#/ =======================================================================================
def PovRayTrailer(fp):
    #/ -----------------------------------------------------------------------------------
    fp.write('\n// =========================================================================== END FILE ==\n' )


#/ =======================================================================================
def Separator(fp):
    #/ -----------------------------------------------------------------------------------
    fp.write('// =======================================================================================\n' )





#/ =======================================================================================
def MakeTextureFile( inc_filename, materials, show=False ):
    #/ -----------------------------------------------------------------------------------

    basename = inc_filename.replace('.inc','').replace('.pov','')

    mat_filename = '%s-texture.inc' % (basename,)

    fp = open( mat_filename, 'w' )

    PovRayHeader( fp, show=show )

    fp.write( '//\n' )
    for mat in materials:
        materials[mat].write(fp)

    PovRayTrailer( fp )

    fp.close()

    return mat_filename.split(os.sep)[-1]



    
#/ =======================================================================================
def ConvertObj2Mesh2( obj_filename, inc_filename,
                      use_textures      = True,
                      make_texture_file = False,
                      include_license   = True ):
    #/ -----------------------------------------------------------------------------------

    obj_root = os.sep.join(obj_filename.split(os.sep)[:-1])

    #/ -----------------------------------------------------------------------------------

    fp = open( obj_filename, 'r' )

    last_vertex  = 0
    last_normal  = 0
    last_uv      = 0

    count_vertex = 0
    count_normal = 0
    count_uv     = 0

    obj = []

    MaterialFiles = []
    MF_count      = 0

    mesh = None

    materials = {}

    current_material = -1

    #/ -----------------------------------------------------------------------------------

    for raw in fp:
        line = raw.strip().split()
        if ( 0 < len(line) ):
            key = line[0].strip()
            if ( 'mtllib' == key ):
                material_filename = '%s%s%s' % ( obj_root, os.sep, line[1].strip(), )
                ParseMaterialFile( material_filename, materials )
            elif ( 'o' == key ):
                mesh = Mesh( line[1].strip() )
                obj.append( mesh )
                last_vertex  = count_vertex
                last_normal  = count_normal
                last_uv      = count_uv

                #/print( '    last v:%d n:%d u:%d' % ( last_vertex, last_normal, last_uv,) )
            elif ( 'v' == key ):
                x = float( line[1] )
                y = float( line[2] )
                z = float( line[3] )
                mesh.vertex.append( [x,y,z] )
                count_vertex += 1
                #print( 'vertex', [x,y,z] )
            elif ( 'vt' == key ):
                s = float( line[1] )
                t = float( line[2] )
                mesh.uv.append( [s,t] )
                count_uv += 1
                #print( 'uv', [s,t] )
            elif ( 'vn' == key ):
                nx = float( line[1] )
                ny = float( line[2] )
                nz = float( line[3] )
                mesh.normal.append( [nx,ny,nz] )
                count_normal += 1
                #print( 'normal', [nx,ny,nz] )
            elif ( 'usemtl' == key ):
                current_material = mesh.addMaterial( line[1] )
            elif ( 'f' == key ):
                A = line[1].split('/')
                B = line[2].split('/')
                C = line[3].split('/')
                
                v1 = int(A[0]) - last_vertex - 1
                t1 = int(A[1]) - last_uv - 1
                n1 = int(A[2]) - last_normal - 1
                
                v2 = int(B[0]) - last_vertex - 1
                t2 = int(B[1]) - last_uv - 1
                n2 = int(B[2]) - last_normal - 1
                
                v3 = int(C[0]) - last_vertex - 1
                t3 = int(C[1]) - last_uv - 1
                n3 = int(C[2]) - last_normal - 1
                
                mesh.face.append( { 'v':[v1,v2,v3],
                                    't':[t1,t2,t3],
                                    'n':[n1,n2,n3],
                                    'm': current_material } )
            elif ('s' == key):
                if ( 'off' == line[1].strip() ):
                    mesh.smooth = False
                else:
                    mesh.smooth = True
            else:
                pass
            
    fp.close()

    #/ -----------------------------------------------------------------------------------

    short_name = inc_filename.split(os.sep)[-1].split('.')[0]
    
    fp = open( inc_filename, 'w' )

    PovRayHeader( fp, show=include_license )

    fp.write( '//\n// Objects:\n' )
    for o in obj:
        fp.write( '//    %s\n' % ( o.name, ) ) 
    fp.write( '//\n' )
    Separator(fp)

    if ( make_texture_file ):
        mname = MakeTextureFile( inc_filename, materials, show=include_license )
        fp.write( '\n#include "%s"\n\n' % ( mname, ) )
    else:
        fp.write( '\n' )
        for mat in materials:
            materials[mat].write(fp)

    for o in obj:
        o.write(fp,materials)

    Separator(fp)

    fp.write( '\n#declare %s = union {\n' % ( short_name, ) )
    for o in obj:
        fp.write( '  object { %s }\n' % ( o.name, ) ) 
    
    fp.write( '} // end union %s\n' % ( short_name, ) )

    PovRayTrailer( fp )

    fp.close()
    
    logger.info( '    Temp file:    %s' % ( obj_filename, ) )
    logger.info( '    PovRay file:  %s' % ( inc_filename, ) )

    logger.info( '    Objects:' )
    for o in obj:
        logger.info( '       %s' % ( o.name, ) ) 
    
    return 0





#/ =======================================================================================
def main( argc, argv ):
    #/ -----------------------------------------------------------------------------------
    if ( 3 > argc ):
        sys.stderr.write("""
OBJ 2 Mesh2 * ver 1 * 2021.02

USAGE: %s input.obj output.inc
   input.obj  - Wavefront OBJ format input file created by Blender
   output.inc - PovRay INC file containing a single Mesh2 object

Example: %s table.ply table.inc

Reads a PLY file created with the io_mesh_ply exporter in Blender 2.9+.
Write a Mesh2 object for use in PovRay 3.8+

""" % (argv[0], argv[0],) )
        return 1

    obj_filename = argv[1]
    inc_filename = argv[2]

    #/ -----------------------------------------------------------------------------------

    return ConvertObj2Mesh2( obj_filename, inc_filename,
                             use_textures      = True,
                             make_texture_file = False,
                             include_license   = True )

#/ =======================================================================================
if ( '__main__' == __name__ ): sys.exit( main( len( sys.argv ), sys.argv ) )
#/ =======================================================================================
#/ **                      C O N V E R T _ O B J _ T O _ M E S H 2                      **
#/ =========================================================================== END FILE ==
