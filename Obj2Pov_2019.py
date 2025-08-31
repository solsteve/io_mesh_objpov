#!/usr/bin/python
#/ ====================================================================== BEGIN FILE =====
#/ **                                   O B J 2 P O V                                   **
#/ =======================================================================================
#/ **                                                                                   **
#/ **  Copyright (c) 2019, Stephen W. Soliday                                           **
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
#/ @brief  Object to POVRAY.
#/
#/ @details Convert WaveFront Object to POVRAY 3.7 Mesh2.
#/
#/ @author  Stephen W. Soliday
#/ @date    2019-03-10
#/
#/ =======================================================================================

import sys

#/ =======================================================================================
def parseVertex( mask ):
    #/ -----------------------------------------------------------------------------------
    x   = mask.split('/')
    c   = len(x)
    pnt = None
    nrm = None
    tex = None

    if ( 0 < c ):
        pnt = int(x[0])
        if ( 1 > pnt ):
            sys.stderr.write( '\nUnsupported: negative index - vertex [%s]' % (x[1],) )
            raise ValueError

    if ( 1 < c ):
        if ( 0 < len(x[1]) ):
            tex = int(x[1])

    if ( 2 < c ):
        nrm = int(x[2])
        if ( 1 > nrm ):
            sys.stderr.write( '\nUnsupported: negative index - normal [%s]' % (x[2],) )
            raise ValueError

    return (pnt,nrm,tex)

#/ =======================================================================================
def parseWavefrontObject( objFile ):
    #/ -----------------------------------------------------------------------------------

    try:
        fp = open( objFile, 'r' )
    except IOError:
        sys.stderr.write( '\nCannot open %s for reading\n\n' % ( objFile ) )
        return None

    sys.stderr.write( '\nParsing %s\n\n' % ( objFile, ) )
    data = []

    obj  = None
    master_vert = [(0.0,0.0,0.0),]
    master_norm = [(0.0,0.0,0.0),]
    face = []

    line = 0
    for raw in fp:
        line += 1
        code = raw[0:2]

        #/ ----- new object --------------------------------------------------------------
        if ( 'o ' == code ):
            if ( None != obj ):
                data.append( obj )
            oname = raw.split()[1].strip().replace('.','_')
            sys.stdout.write( '  Object: %s\n' % (oname,) )
            face = []
            obj = { 'name':oname, 'face':face }

        #/ ----- normals -----------------------------------------------------------------
        if ( 'vn' == code ):
            try:
                N = raw.split()
                x = float(N[1])
                y = float(N[2])
                z = float(N[3])
                master_norm.append( (x,y,z,) )
            except ValueError:
                sys.stderr.write( '\nParse error (normal) in line %d of %s\n\n' %
                                  ( line, objFile, ) )
                fp.close()
                return (None, None, None)

        #/ ----- vertices ----------------------------------------------------------------
        if ( 'v ' == code ):
            try:
                V = raw.split()
                x = float(V[1])
                y = float(V[2])
                z = float(V[3])
                master_vert.append( (x,y,z,) )
            except ValueError:
                sys.stderr.write( '\nParse error (vertex) in line %d of %s\n\n' %
                                  ( line, objFile, ) )
                fp.close()
                return (None, None, None)

        #/ ----- face --------------------------------------------------------------------
        if ( 'f ' == code ):
            V = raw.split()[1:]
            #/ ----- three point face ----------------------------------------------------
            if ( 3 == len(V) ):
                try:
                    A = parseVertex( V[0] )
                    B = parseVertex( V[1] )
                    C = parseVertex( V[2] )
                    face.append( (A,B,C) )
                except ValueError:
                    sys.stderr.write( '\nParse error (3-face) in line %d of %s\n\n' %
                                      ( line, objFile, ) )
                    fp.close()
                    return (None, None, None)

            #/ ----- four point face -----------------------------------------------------
            elif ( 4 == len(V) ):
                try:
                    A = parseVertex( V[0] )
                    B = parseVertex( V[1] )
                    C = parseVertex( V[2] )
                    D = parseVertex( V[3] )
                    face.append( (A,B,C) )
                    face.append( (C,D,A) )
                except ValueError:
                    sys.stderr.write( '\nParse error (3-face) in line %d of %s\n\n' %
                                      ( line, objFile, ) )
                    fp.close()
                    return (None, None, None)

            #/ ----- unsupported face ----------------------------------------------------
            else:
                sys.stderr.write( '\nUnsupported: Face found at line %d of %s with ' +
                                  'other than 3 of 4 vertices\n\n' % ( line, objFile, ) )
                return (None, None, None)

        #/ ----- unsupported tags --------------------------------------------------------
        if ( 'vt' == code ):
            sys.stderr.write( '\nUnsupported: Texture vertices found at ' +
                              'line %d of %s\n\n' % ( line, objFile, ) )
            return (None, None, None)

        if ( 'p ' == code ):
            sys.stderr.write( '\nUnsupported: Point found at line %d ' +
                              'of %s\n\n' % ( line, objFile, ) )
            return (None, None, None)

        if ( 'l ' == code ):
            sys.stderr.write( '\nUnsupported: Line found at line %d ' +
                              'of %s\n\n' % ( line, objFile, ) )
            return (None, None, None)

        if ( 'g ' == code ):
            sys.stderr.write( '\nUnsupported: Group found at line %d ' +
                              'of %s\n\n' % ( line, objFile, ) )
            return (None, None, None)

    if ( None != obj ):
        data.append( obj )

    fp.close()

    return (data,master_vert,master_norm)

#/ =======================================================================================
def buildMap( face, col ):
    #/ -----------------------------------------------------------------------------------
    map = {}
    idx = 0

    for f in face:
        A  = f[0]
        B  = f[1]
        C  = f[2]

        av = A[col]
        bv = B[col]
        cv = C[col]

        if ( not map.has_key(av) ):
            map[av] = idx
            idx += 1

        if ( not map.has_key(bv) ):
            map[bv] = idx
            idx += 1

        if ( not map.has_key(cv) ):
            map[cv] = idx
            idx += 1

        rev = len(map)*[-1]
        for k in map:
            i = map[k]
            rev[i] = k

    return map, rev

#/ =======================================================================================
def createMesh2( fp, name, face, vert, norm ):
    #/ -----------------------------------------------------------------------------------
    sys.stderr.write( '  Building %s\n' % (name,) )

    vmap, vrev = buildMap( face, 0 )
    nmap, nrev = buildMap( face, 1 )

    fp.write( '#declare %s =\nmesh2 {\n' % (name,) )

    n = len(vmap)
    fp.write( '    vertex_vectors {\n        %d,\n' % (n,) )
    for idx in vrev:
        x = vert[idx][0]
        y = vert[idx][1]
        z = vert[idx][2]
        fp.write( '        <%.6f, %.6f, %.6f>,\n' % (x,y,z,) )
    fp.write( '    }\n' );

    n = len(nmap)
    fp.write( '    normal_vectors {\n        %d,\n' % (n,) )
    for idx in nrev:
        x = norm[idx][0]
        y = norm[idx][1]
        z = norm[idx][2]
        fp.write( '        <%.6f, %.6f, %.6f>,\n' % (x,y,z,) )
    fp.write( '    }\n' );

    fp.write( '    texture_list {\n        1 texture{}\n    }' )

    fp.write( '    face_indices {\n        %d,\n' % (len(face),) )
    for f in face:
        a = vmap[f[0][0]]
        b = vmap[f[1][0]]
        c = vmap[f[2][0]]
        fp.write( '        <%d, %d, %d>,\n' % (a,b,c,) )
    fp.write( '    }\n' );

    fp.write( '    normal_indices {\n        %d,\n' % (len(face),) )
    for f in face:
        a = nmap[f[0][1]]
        b = nmap[f[1][1]]
        c = nmap[f[2][1]]
        fp.write( '        <%d, %d, %d>,\n' % (a,b,c,) )
    fp.write( '    }\n' );

    fp.write( '    radiosity {\n        importance 0.5\n    }\n' )

    fp.write( '}\n\n' )


#/ =======================================================================================
def buildPovRayMesh( povFile, data, vert, norm ):
    #/ -----------------------------------------------------------------------------------
    sys.stderr.write( '\nBuilding %s\n' % ( povFile, ) )

    fp = open( povFile, 'w' )

    for obj in data:
        createMesh2( fp, obj['name'], obj['face'], vert, norm )

    sys.stderr.write( '\n' )
    return 1


#/ =======================================================================================
def buildTestRaw( rawFile, data, vert, norm ):
    #/ -----------------------------------------------------------------------------------
    sys.stderr.write( '\nBuilding %s\n' % ( rawFile, ) )

    fp = open( rawFile, 'w' )

    for obj in data:
        sys.stderr.write( '  Building %s\n' % (obj['name'],) )
        face = obj['face']

        for f in face:
            A = f[0]
            B = f[1]
            C = f[2]

            xa = vert[A[0]][0]
            ya = vert[A[0]][1]
            za = vert[A[0]][2]

            xb = vert[B[0]][0]
            yb = vert[B[0]][1]
            zb = vert[B[0]][2]

            xc = vert[C[0]][0]
            yc = vert[C[0]][1]
            zc = vert[C[0]][2]

            fp.write( '%.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f\n' %
                      ( xa, ya, za, xb, yb, zb, xc, yc, zc, ) )

    fp.close()
    sys.stderr.write( '\n' )
    return 0


#/ =======================================================================================
def process( objFile, povFile ):
    #/ -----------------------------------------------------------------------------------

    (data, vert, norm) = parseWavefrontObject( objFile )
    if ( None == data ):
        return 1

    buildTestRaw( 'test.raw', data, vert, norm )

    return buildPovRayMesh( povFile, data, vert, norm )


#/ =======================================================================================
def usage( pn, msg=None ):
    #/ -----------------------------------------------------------------------------------
    if ( None != msg ):
        sys.stderr.write( '\n%s\n' % (msg,) )

    sys.stderr.write( """
USAGE: %s input.obj output.pov
  input.obj  - path to a Wavefront OBJ file
  output.inc - path to an output PovRay include file

    Blender OBJ export needs to be set up with Y-Forward Z-Up


Example: %s BAxis.obj btest.inc

""" % ( pn, pn, ) )

    return 1


#/ =======================================================================================
def main( argc, argv ):
    #/ -----------------------------------------------------------------------------------

    sys.stderr.write( '\n======================================================' )
    sys.stderr.write( '\nOBJ2POV * Convert Wavefront OBJ to PovRay Mesh2 * 2019' )
    sys.stderr.write( '\n------------------------------------------------------\n' )

    if ( 3 != argc ):
        return usage( argv[0], 'missing arguments' )

    return process( argv[1], argv[2] )


#/ =======================================================================================
if ( '__main__' == __name__ ): sys.exit( main( len(sys.argv), sys.argv ) )
#/ =======================================================================================
#/ **                                   O B J 2 P O V                                   **
#/ =========================================================================== END FILE ==
#
#  FWD UP
#  -Z  -Y rev all
#   Z   Y rev X
#  -Z   Y rev Y
#
