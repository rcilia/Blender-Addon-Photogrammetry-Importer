import os
import bpy
from bpy.props import StringProperty, CollectionProperty, EnumProperty
from bpy_extras.io_utils import ExportHelper

from photogrammetry_importer.file_handlers.colmap_file_handler import (
    ColmapFileHandler,
)
from photogrammetry_importer.operators.export_op import ExportOperator


class ExportColmapOperator(ExportOperator, ExportHelper):
    """:code:`Blender` operator to export a :code:`Colmap` model."""

    bl_idname = "export_scene.colmap"
    bl_label = "Export Colmap"
    bl_options = {"PRESET"}

    # https://docs.blender.org/api/current/bpy.types.FileSelectParams.html
    directory: StringProperty()

    files: CollectionProperty(
        name="Directory Path",
        description="Directory path used for exporting the Colmap model",
        type=bpy.types.OperatorFileListElement,
    )

    camera_model: EnumProperty(
        name="Camera Model",
        description="Choose the camera model for export",
        items=[
            ("SIMPLE_PINHOLE", "Simple Pinhole", "Single focal length (f, cx, cy)"),
            ("PINHOLE", "Pinhole", "Separate focal lengths (fx, fy, cx, cy)"),
        ],
        default="SIMPLE_PINHOLE",
    )

    filename_ext = ""
    # filter_folder : BoolProperty(default=True, options={'HIDDEN'})

    def execute(self, context):
        """Export selected cameras and points as :code:`Colmap` model."""
        assert len(self.files) == 1
        odp = os.path.join(self.directory, self.files[0].name)

        cameras, points = self.get_selected_cameras_and_vertices_of_meshes(odp)
        for cam in cameras:
            assert cam.get_calibration_mat() is not None

        ColmapFileHandler.write_colmap_model(odp, cameras, points, camera_model=self.camera_model, op=self)

        return {"FINISHED"}
