import json
import math
from pathlib import Path

import bpy
from mathutils import Vector

# DORÉ FILM Camera Spine importer.
# The JSON remains the source of truth; Blender is only a previs/editor view.
JSON_PATH = Path(bpy.path.abspath("//")) / "camera-spine-experiment-01.json"
COLLECTION = "DORE_CAMERA_SPINE"


def clear_collection(name):
    old = bpy.data.collections.get(name)
    if old:
        for obj in list(old.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old)
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def link_only(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()


def main():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    nodes = data["nodes"]
    col = clear_collection(COLLECTION)

    curve_data = bpy.data.curves.new("CameraSpinePath", "CURVE")
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 24
    spline = curve_data.splines.new('NURBS')
    spline.points.add(len(nodes) - 1)
    for point, node in zip(spline.points, nodes):
        x, y, z = node["p"]
        point.co = (x, y, z, 1.0)
    spline.order_u = min(4, len(nodes))
    spline.use_endpoint_u = True
    path = bpy.data.objects.new("CameraSpinePath", curve_data)
    col.objects.link(path)

    for node in nodes:
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=node["p"])
        marker = bpy.context.object
        marker.name = node["id"]
        marker["beat"] = node["beat"]
        marker["grammar"] = node["grammar"]
        marker["action"] = node["action"]
        marker["speed"] = node.get("speed", 0.0)
        marker["dwell"] = node.get("dwell", 0.0)
        if node.get("timeBridge"):
            marker["timeBridge"] = node["timeBridge"]
        link_only(marker, col)

    cam_data = bpy.data.cameras.new("DoreFilmCamera")
    camera = bpy.data.objects.new("DoreFilmCamera", cam_data)
    col.objects.link(camera)
    first = nodes[0]
    camera.location = first["p"]
    cam_data.lens = first.get("lens", 45)
    look_at(camera, first["look"])
    bpy.context.scene.camera = camera

    # Keyframes are deliberately generated from authored speed + dwell.
    # Dwell is literal seconds; travel duration is proportional to distance/speed.
    fps = 24
    bpy.context.scene.render.fps = fps
    dwell_total = sum(float(n.get("dwell", 0)) for n in nodes)
    target_seconds = 52.0
    raw = []
    for a, b in zip(nodes[:-1], nodes[1:]):
        dist = (Vector(a["p"]) - Vector(b["p"])).length
        speed = max(0.001, (float(a.get("speed", .2)) + float(b.get("speed", .2))) / 2)
        raw.append(dist / speed)
    travel_budget = max(8.0, target_seconds - dwell_total)
    raw_total = sum(raw)
    travel = [v / raw_total * travel_budget for v in raw]

    sec = 0.0
    for i, node in enumerate(nodes):
        camera.location = node["p"]
        cam_data.lens = node.get("lens", 45)
        look_at(camera, node["look"])
        frame = round(sec * fps) + 1
        camera.keyframe_insert("location", frame=frame)
        camera.keyframe_insert("rotation_euler", frame=frame)
        cam_data.keyframe_insert("lens", frame=frame)

        sec += float(node.get("dwell", 0))
        hold = round(sec * fps) + 1
        camera.keyframe_insert("location", frame=hold)
        camera.keyframe_insert("rotation_euler", frame=hold)
        cam_data.keyframe_insert("lens", frame=hold)
        if i < len(nodes) - 1:
            sec += travel[i]

    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = round(sec * fps) + 1
    print(f"Imported {len(nodes)} Camera Spine nodes; duration={sec:.2f}s; frames={bpy.context.scene.frame_end}")


if __name__ == "__main__":
    main()
