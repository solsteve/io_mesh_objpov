# io_mesh_objpov

## Export Blender 4.5.2 LTS UV Mesh to Povray 3.7 mesh2 files

### Install
Create a symbolic link in the top level directory. In this example I have Blender installed locally at **${HOME}/Apps/blender-4.5.2-linux-x64**

    cd io_mesh_objpov
    ln -s ${HOME}/Apps/blender-4.5.2-linux-x64/4.5/scripts/addons_core addon
    make install
    make distclean
    cd ..
Next open blender and navigate to **Edit->Preferences->Add-ons** select [x]*POVRAY Mesh2 (wrapper)*

I find it best best to save ***selected*** meshes instead of combining them in one file. I like to save my materials in a separate file, as well.
