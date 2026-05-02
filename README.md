Python script for importing Animation Packs downloaded from Mixamo into Blender for a single armature.

When downloading animation packs from Mixamo.com, they come in a folder with the Pack name containing an FBX file for each animation, with the animation name as the file name.

However when you import all these FBXs into Blender with your main Armature, it imports an armature per FBX, and assigns that animation to that armature, and then neither the armature that is imported or the animation itself has the animation name, so you are left guessing which animation is which trying to rename them. Then you have to push each animation individually to the NLA stack and then get rid of the armatures and just leave your main armature. Its annoying.

Instead do this:
1. Import your main model/armature into your Blender scene, and rename the armature to "Player".
2. Open the text editor, make a new file and name it mixamo_anim_pack_importer.py.
3. In Edit tab click Save to save as to save the file somewhere.
4. Copy and paste this script into the text editor and save.
5. Paste your absolute path to your Animation Pack folder in the FOLDER variable in the script.
6. Run the script and all the animations in that folder will be imported into your scene, and can be used immediately by your main armature with no extra armatures in the scene.

For a video tutorial, see here:
