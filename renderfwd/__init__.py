import bpy
from bpy.props import StringProperty, IntProperty
from bpy.app.handlers import persistent
import logging
import socket

bl_info = {
    "name": "renderfwd",
    "description": "Forward the output image path utf-8 encoded via UDP on renders",
    "author": "Emanuel Buholzer",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Preferences > Add-ons > renderfwd",
    "doc_url": "https://https://github.com/emanuelbuholzer/blender-render-forwarder",
    "tracker_url": "https://github.com/emanuelbuholzer/blender-render-forwarder/issues",
    "support": "COMMUNITY",
    "category": "Render"
}

logger = logging.getLogger(__name__)


class Properties(bpy.types.PropertyGroup):
    ip: StringProperty(name='Ip', default='127.0.0.1')
    port: IntProperty(name='Port', default=9889)


class Preferences(bpy.types.AddonPreferences):
    bl_idname = 'renderfwd'

    def draw(self, context):
        self.layout.prop(context.window_manager.renderfwd, 'ip')
        self.layout.prop(context.window_manager.renderfwd, 'port')


@persistent
def render_write_handler(_):
    ip = bpy.context.window_manager.renderfwd.ip
    port = bpy.context.window_manager.renderfwd.port

    file_path = bpy.context.scene.render.filepath
    file_extension = bpy.context.scene.render.file_extension
    output_image_path = f"{file_path}{file_extension}"

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        logger.debug(f"Forwarding {output_image_path} to {ip}:{port}")
        sock.sendto(output_image_path.encode('utf-8'), (ip, port))


bpy.app.handlers.render_write.append(render_write_handler)


def register():
    bpy.utils.register_class(Properties)
    bpy.types.WindowManager.renderfwd = bpy.props.PointerProperty(type=Properties)

    bpy.utils.register_class(Preferences)


def unregister():
    bpy.utils.unregister_class(Preferences)

    bpy.utils.unregister_class(Properties)
