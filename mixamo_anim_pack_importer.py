import bpy
import os


# CONFIG
FOLDER = "/path/to/your/fbx_folder"
MASTER_ARMATURE_NAME = "Player"
START_FRAME = 0
FRAME_PADDING = 10  # space between animations


master = bpy.data.objects.get(MASTER_ARMATURE_NAME)

if not master:
    raise Exception(f"[ERROR] Master armature '{MASTER_ARMATURE_NAME}' not found")

master.animation_data_create()

current_frame = START_FRAME

print("\n=== MIXAMO BATCH IMPORT START ===\n")


# MAIN LOOP
for file in sorted(os.listdir(FOLDER)):
    if not file.lower().endswith(".fbx"):
        continue

    filepath = os.path.join(FOLDER, file)
    anim_name = os.path.splitext(file)[0]

    print(f"\n--- Importing: {file} ---")

    # Track objects before import
    before = set(bpy.data.objects)

    # Import FBX
    bpy.ops.import_scene.fbx(filepath=filepath)

    # Detect new objects
    after = set(bpy.data.objects)
    new_objects = after - before

    print(f"[INFO] Imported {len(new_objects)} new objects")

    # Find imported armature
    armature = next((obj for obj in new_objects if obj.type == 'ARMATURE'), None)

    if not armature:
        print("[WARNING] No armature found, skipping")
        continue

    print(f"[INFO] Found armature: {armature.name}")

    # Get action
    action = None
    if armature.animation_data:
        action = armature.animation_data.action

    if not action:
        print("[WARNING] No action found, skipping")
        continue

    # Rename action
    old_name = action.name
    action.name = anim_name
    print(f"[INFO] Renamed action: '{old_name}' → '{anim_name}'")

    # Determine frame range
    start, end = map(int, action.frame_range)
    length = end - start

    print(f"[INFO] Frame range: {start} → {end} (len={length})")

    # Create NLA track + strip
    track = master.animation_data.nla_tracks.new()
    track.name = anim_name
    track.mute = True

    strip = track.strips.new(anim_name, current_frame, action)

    # Scale strip to match original length
    strip.frame_start = current_frame
    strip.frame_end = current_frame + length

    print(f"[INFO] Placed at frame {current_frame}")

    # Advance timeline
    current_frame += length + FRAME_PADDING

    # CLEANUP
    deleted = 0

    for obj in new_objects:
        if obj.type == 'ARMATURE' and obj != master:
            bpy.data.objects.remove(obj, do_unlink=True)
            deleted += 1

        elif obj.type == 'MESH':
            bpy.data.objects.remove(obj, do_unlink=True)
            deleted += 1

    print(f"[INFO] Cleaned up {deleted} objects")

print("\n=== IMPORT COMPLETE ===")
print(f"[INFO] Total timeline length: {current_frame} frames\n")
