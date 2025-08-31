#/ ====================================================================== BEGIN FILE =====
#/ **                                  _ _ I N I T _ _                                  **
#/ =======================================================================================
#
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
# <pep8-80 compliant>
#
#/ ----- Modification History ------------------------------------------------------------
#/
#/ Originally written by: Campbell Barton, Bastien Montagne
#/
#/ Modified by: Stephen W. Soliday
#/ Date:        Feb. 7, 2021
#/ Reason:      This Blender addon was modified to act as a temporary wrapper.
#/              Importer was removed, options were preselected, and output
#/              was directed to a temporary directory.
#/              The OBJ to PovRayMesh2 is called on completion.
#/
#/ =======================================================================================
bl_info = {
    'name'        : 'POVRAY Mesh2 (wrapper)',
    'author'      : 'Stephen Soliday',
    'version'     : (1, 0, 3),
    'blender'     : (4, 5, 2),
    'location'    : 'File > Import/Export',
    'description' : 'Export PovRay Mesh2 (.inc)',
    'warning'     : '',
    'doc_url'     : '{BLENDER_MANUAL_URL}/addons/import_export/povray_mesh.html',
    'support'     : 'COMMUNITY',
    'category'    : 'Import-Export',
}
#/ =======================================================================================

import sys, os, time

if "bpy" in locals():
    import importlib
    if "import_obj" in locals():
        importlib.reload(import_obj)
    if "export_obj" in locals():
        importlib.reload(export_obj)
    if "convert_obj_to_mesh2" in locals():
        importlib.reload(convert_obj_to_mesh2)
    if 'TLogger' in locals():
        importlib.reload(TLogger)

import bpy
from . import TLogger

from bpy.props import (
        BoolProperty,
        FloatProperty,
        StringProperty,
        EnumProperty,
        )

from bpy_extras.io_utils import (
        ImportHelper,
        ExportHelper,
        orientation_helper,
        path_reference_mode,
        axis_conversion,
        )


logger = TLogger.getInstance()


#/ =======================================================================================
@orientation_helper(axis_forward='Z', axis_up='Y')
class ExportOBJW(bpy.types.Operator, ExportHelper):
    #/ -----------------------------------------------------------------------------------
    """Save a PovRay File"""

    logger.info( 'Enter class ExportPOVRAY' )

    bl_idname  = "export_scene.povray"
    bl_label   = 'Export INC'
    bl_options = {'PRESET'}

    filename_ext = ".inc"
    filter_glob: StringProperty(
        default="*.inc;*.pov",
        options={'HIDDEN'},
    )


    #/ ----- add to include --------------------------------------------------------------

    use_materials: BoolProperty(
        name        = "Include Texture Section",
        description = "False: mesh2 without texture",
        default     = True,
    )

    use_seaprate_files: BoolProperty(
        name        = "Separate texture (.inc)",
        description = "Place textures in separate file *_texture.inc",
        default     = False,
    )

    use_license: BoolProperty(
        name        = "Include License",
        description = "Include a license in the header",
        default     = True,
    )

    #/ ----- keep these in include -------------------------------------------------------

    use_selection: BoolProperty(
        name        = "Selection Only",
        description = "Export selected objects only",
        default     = False,
    )

    #/ ----- keep these in transform -----------------------------------------------------

    global_scale: FloatProperty(
        name    = "Scale",
        min     = 0.0001,
        max     = 1000.0,
        default = 1.0,
    )

    #/ ----- keep these in geometry ------------------------------------------------------

    use_normals: BoolProperty(
        name        = "Write Normals",
        description = "Export one normal per vertex and per face, " +
        "to represent flat faces and sharp edges",
        default     = True,
    )

    use_uvs: BoolProperty(
        name="Include UVs",
        description="Write out the active UV coordinates",
        default=True,
    )

    #/ ----- remove from include display -------------------------------------------------

    use_blen_objects: BoolProperty(
        name        = "PovRay Mesh",
        description = "Export Blender objects as PovRay meshes",
        default     = True,
    )

    group_by_object: BoolProperty(
        name="PovRay Meshes",
        description="Export Blender objects as PovRay meshes",
        default=False,
    )

    group_by_material: BoolProperty(
        name="Material Groups",
        description="Generate a PovRay group for each part of a geometry using a different material",
        default=False,
    )

    use_animation: BoolProperty(
        name="Animation",
        description="Write out a PovRay file for each frame",
        default=False,
    )

    use_edges: BoolProperty(
        name="Include Edges",
        description="",
        default=True,
    )

    #/ ----- remove from transform display -----------------------------------------------


    #/ ----- remove from geometry display ------------------------------------------------

    use_mesh_modifiers: BoolProperty(
        name="Apply Modifiers",
        description="Apply modifiers",
        default=True,
    )

    # Non working in Blender 2.8 currently.
    # ~ use_mesh_modifiers_render: BoolProperty(
            # ~ name="Use Modifiers Render Settings",
            # ~ description="Use render settings when applying modifiers to mesh objects",
            # ~ default=False,
            # ~ )

    use_smooth_groups: BoolProperty(
        name="Smooth Groups",
        description="Write sharp edges as smooth groups",
        default=False,
    )

    use_smooth_groups_bitflags: BoolProperty(
        name="Bitflag Smooth Groups",
        description="Same as 'Smooth Groups', but generate smooth groups IDs as bitflags "
        "(produces at most 32 different smooth groups, usually much less)",
        default=False,
    )

    use_triangles: BoolProperty(
        name="Triangulate Faces",
        description="Convert all faces to triangles",
        default=True,
    )

    use_nurbs: BoolProperty(
        name="Write Nurbs",
        description="Write nurbs curves as PovRay nurbs rather than "
        "converting to geometry",
        default=False,
    )

    use_vertex_groups: BoolProperty(
        name="Polygroups",
        description="",
        default=False,
    )

    keep_vertex_order: BoolProperty(
        name="Keep Vertex Order",
        description="",
        default=False,
    )

    path_mode: path_reference_mode

    check_extension = True

    #/ ===================================================================================
    def execute(self, context):
        #/ -------------------------------------------------------------------------------

        logger.info( 'execute IO_MESH_POV::Mesh2 wrapper' )

        from . import export_obj
        from . import convert_obj_to_mesh2

        from mathutils import Matrix

        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "global_scale",
                                            "check_existing",
                                            "filter_glob",
                                            "use_seaprate_files",
                                            "use_license",
                                            ))

        global_matrix = (Matrix.Scale(self.global_scale, 4) @
                         axis_conversion(to_forward=self.axis_forward,
                                         to_up=self.axis_up,
                                         ).to_4x4())

        keywords["global_matrix"] = global_matrix

        print( '\n\nv=====================================================v\n' )
        print( global_matrix )
        print( '\n^=====================================================^\n\n' )

        #/ -------------------------------------------------------------------------------

        user_filepath = keywords['filepath']

        user_path = os.sep.join(user_filepath.split(os.sep)[:-1])

        now = time.gmtime()

        temp_file = '%s%stmp%04d%03d_%02d%02d%02d.obj' % ( user_path, os.sep,
            now.tm_year, now.tm_yday, now.tm_hour, now.tm_min, now.tm_sec, )

        keywords['filepath'] = temp_file

        rv = export_obj.save(context, **keywords)

        #/ -------------------------------------------------------------------------------

        keywords = self.as_keywords()

        include_textures      = keywords['use_materials']
        separate_texture_file = keywords['use_seaprate_files']
        put_license_in_header = keywords['use_license']

        convert_obj_to_mesh2.ConvertObj2Mesh2(
            temp_file, user_filepath,
            use_textures      = include_textures,
            make_texture_file = separate_texture_file,
            include_license   = put_license_in_header )

        return rv

    #/ ===================================================================================
    def draw(self, context):
        #/ -------------------------------------------------------------------------------
        pass


#/ =======================================================================================
class OBJW_PT_export_include(bpy.types.Panel):
    #/ -----------------------------------------------------------------------------------
    bl_space_type  = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label       = "Include"
    bl_parent_id   = "FILE_PT_operator"

    #/ ===================================================================================
    @classmethod
    def poll(cls, context):
        #/ -------------------------------------------------------------------------------
        sfile    = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_povray"

    #/ ===================================================================================
    def draw(self, context):
        #/ -------------------------------------------------------------------------------
        layout = self.layout
        layout.use_property_split    = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        col = layout.column(heading="Limit to")
        col.prop(operator, 'use_selection')

        layout.prop(operator, 'use_materials')
        layout.prop(operator, 'use_seaprate_files')
        layout.prop(operator, 'use_license')

        #col = layout.column(heading="Objects as", align=True)
        #col.prop(operator, 'use_blen_objects')
        #col.prop(operator, 'group_by_object')
        #col.prop(operator, 'group_by_material')

        #layout.separator()

        # layout.prop(operator, 'use_animation')


#/ =======================================================================================
class OBJW_PT_export_transform(bpy.types.Panel):
    #/ -----------------------------------------------------------------------------------
    bl_space_type  = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label       = "Transform"
    bl_parent_id   = "FILE_PT_operator"

    #/ ===================================================================================
    @classmethod
    def poll(cls, context):
        #/ -------------------------------------------------------------------------------
        sfile    = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_povray"

    #/ ===================================================================================
    def draw(self, context):
        #/ -------------------------------------------------------------------------------
        layout = self.layout
        layout.use_property_split    = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, 'global_scale')
        layout.prop(operator, 'path_mode')
        layout.prop(operator, 'axis_forward')
        layout.prop(operator, 'axis_up')


#/ =======================================================================================
class OBJW_PT_export_geometry(bpy.types.Panel):
    #/ -----------------------------------------------------------------------------------
    bl_space_type  = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label       = "Geometry"
    bl_parent_id   = "FILE_PT_operator"

    #/ ===================================================================================
    @classmethod
    def poll(cls, context):
        #/ -------------------------------------------------------------------------------
        sfile    = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_povray"

    #/ ===================================================================================
    def draw(self, context):
        #/ -------------------------------------------------------------------------------
        layout = self.layout
        layout.use_property_split    = True
        layout.use_property_decorate = False  # No animation.

        sfile    = context.space_data
        operator = sfile.active_operator

        # layout.prop(operator, 'use_mesh_modifiers')
        # Property definition disabled, not working in 2.8 currently.
        # layout.prop(operator, 'use_mesh_modifiers_render')
        # layout.prop(operator, 'use_smooth_groups')
        # layout.prop(operator, 'use_smooth_groups_bitflags')
        layout.prop(operator, 'use_normals')
        layout.prop(operator, 'use_uvs')
        # layout.prop(operator, 'use_materials')
        # layout.prop(operator, 'use_triangles')
        # layout.prop(operator, 'use_nurbs', text="Curves as NURBS")
        # layout.prop(operator, 'use_vertex_groups')
        # layout.prop(operator, 'keep_vertex_order')


#/ =======================================================================================
def menu_func_export(self, context):
    #/ -----------------------------------------------------------------------------------
    self.layout.operator(ExportOBJW.bl_idname, text="PovRay Mesh2 (.inc)")


#classes = (
#    ExportOBJW,
#    OBJW_PT_export_include,
#    OBJW_PT_export_transform,
#    OBJW_PT_export_geometry,
#)

classes = (
    ExportOBJW,
    OBJW_PT_export_include,
    OBJW_PT_export_transform,
    OBJW_PT_export_geometry,
)


#/ =======================================================================================
def register():
    #/ -----------------------------------------------------------------------------------
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

    logger.info( 'Registered: PovRay Mesh2 Exporter (wrapper)' )


#/ =======================================================================================
def unregister():
    #/ -----------------------------------------------------------------------------------
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

    for cls in classes:
        bpy.utils.unregister_class(cls)

    logger.info( 'Un-registered: PovRay Mesh2 Exporter (wrapper)' )


#/ =======================================================================================
if __name__ == "__main__": register()
#/ =======================================================================================
#/ **                                  _ _ I N I T _ _                                  **
#/ =========================================================================== END FILE ==
