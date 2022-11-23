# io_mesh_objpov

## Export Blender 3.1x UV Mesh to Povray 3.7 mesh2 files

### Install
Create a symbolic link in the top level directory. In this example I have Blender installed locally at **$HOME/Apps/blender-3.1.2-linux-x64**

    cd io_mesh_objpov
    ln -s $HOME/Apps/blender-3.1.2-linux-x64/3.1/scripts/addons/io_mesh_objpov addon
    make install
    make distclean
    cd ..
Next open blender and navigate to **Edit->Preferences->Add-ons->Testing** select [x]*Import-Export POVRAY Mesh2 (wrapper)*

It is best to save ***selected*** meshes instead of combining them in one file. I like to save my materials in a separate file, as well.
