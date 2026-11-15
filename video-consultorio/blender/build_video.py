"""
Video explicativo · Consultorio virtual Paola Velásquez
Construye toda la animación (10 escenas) en Blender 4.0, sincronizada con la voz.

Uso:
  blender -b --factory-startup --python build_video.py -- <carpeta_fuentes> <archivo.blend> [ancho alto]
Luego renderizar:
  blender -b <archivo.blend> -a
"""
import bpy, bmesh, math, random, sys
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
import os
FONT_DIR = os.path.abspath(argv[0] if len(argv) > 0 else "fonts")
OUT_BLEND = argv[1] if len(argv) > 1 else "video.blend"
RES_X = int(argv[2]) if len(argv) > 2 else 1920
RES_Y = int(argv[3]) if len(argv) > 3 else 1080

FPS = 24
DURATION = 82.0  # 79 s de voz + cierre
random.seed(7)


def F(t):
    return int(round(t * FPS)) + 1


def lin(h):
    """Color hex sRGB -> RGBA lineal."""
    h = h.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, 1.0)


# Paleta de marca (paolavelasquez.com)
BG = "#1C1018"
PINK = "#E0679A"
MAUVE = "#C98BBF"
LIGHT = "#F0B6D2"
INK = "#F6E9F0"
MUTED = "#C7AABB"
GREEN = "#4FBF7A"

# ---------------------------------------------------------------- escena base
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = RES_X
scene.render.resolution_y = RES_Y
scene.render.fps = FPS
scene.frame_start = 1
scene.frame_end = F(DURATION)
ee = scene.eevee
ee.taa_render_samples = 16
ee.use_bloom = True
ee.bloom_intensity = 0.06
ee.bloom_threshold = 0.9
ee.bloom_radius = 5.5
ee.use_ssr = False
ee.use_gtao = True
ee.gtao_distance = 1.0
ee.use_soft_shadows = False
ee.shadow_cube_size = "512"
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "None"
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.render.use_overwrite = False
scene.render.use_placeholder = True

world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = lin(BG)
world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

FONTS = {
    "serif": bpy.data.fonts.load(f"{FONT_DIR}/Playfair-SemiBold.ttf"),
    "italic": bpy.data.fonts.load(f"{FONT_DIR}/Playfair-Italic.ttf"),
    "sans": bpy.data.fonts.load(f"{FONT_DIR}/Poppins-Regular.ttf"),
    "medium": bpy.data.fonts.load(f"{FONT_DIR}/Poppins-Medium.ttf"),
    "semi": bpy.data.fonts.load(f"{FONT_DIR}/Poppins-SemiBold.ttf"),
}

SPACING = 40.0  # distancia entre "estaciones" (una por escena)


def link(obj):
    scene.collection.objects.link(obj)
    return obj


# ---------------------------------------------------------------- materiales
def key_input(sock, value, frame):
    sock.default_value = value
    sock.keyframe_insert("default_value", frame=frame)


def mat_emit(color, strength=1.0, visible=True):
    """Emisión plana con mezcla a transparente (para aparecer/desaparecer)."""
    m = bpy.data.materials.new("emit")
    m.use_nodes = True
    m.blend_method = "BLEND"
    m.shadow_method = "NONE"
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = lin(color) if isinstance(color, str) else color
    em.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.inputs[0].default_value = 1.0 if visible else 0.0
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    m["mix"] = mix.name
    m["em"] = em.name
    return m


def mat_soft(color, rough=0.45, emit=0.0, emit_color=None, alpha_mix=False):
    """Superficie suave (principled) con opción de emisión y fundido."""
    m = bpy.data.materials.new("soft")
    m.use_nodes = True
    m.blend_method = "BLEND" if alpha_mix else "OPAQUE"
    m.shadow_method = "HASHED" if alpha_mix else "OPAQUE"
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    p = nt.nodes.new("ShaderNodeBsdfPrincipled")
    p.inputs["Base Color"].default_value = lin(color)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Emission Color"].default_value = lin(emit_color or color)
    p.inputs["Emission Strength"].default_value = emit
    if "Coat Weight" in p.inputs:
        p.inputs["Coat Weight"].default_value = 0.25
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.inputs[0].default_value = 1.0
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(p.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    m["mix"] = mix.name
    m["bsdf"] = p.name
    return m


def mix_of(obj):
    m = obj.active_material
    return m.node_tree.nodes[m["mix"]]


def fade(obj, t, dur=0.5, to=1.0, frm=None):
    """Funde el material de obj hasta `to` empezando en t."""
    mix = mix_of(obj)
    start = mix.inputs[0].default_value if frm is None else frm
    key_input(mix.inputs[0], start, F(t))
    key_input(mix.inputs[0], to, F(t + dur))


def hide_until(obj, t, dur=0.5, rise=0.35):
    mix = mix_of(obj)
    key_input(mix.inputs[0], 0.0, 1)
    key_input(mix.inputs[0], 0.0, F(t))
    key_input(mix.inputs[0], 1.0, F(t + dur))
    if rise:
        z = obj.location.z
        obj.location.z = z - rise
        obj.keyframe_insert("location", index=2, frame=F(t))
        obj.location.z = z
        obj.keyframe_insert("location", index=2, frame=F(t + dur))


def pop(obj, t, dur=0.45, s=1.0):
    base = Vector(obj.scale) * s
    obj.scale = base * 0.001
    obj.keyframe_insert("scale", frame=1)
    obj.keyframe_insert("scale", frame=F(t))
    obj.scale = base * 1.08
    obj.keyframe_insert("scale", frame=F(t + dur * 0.75))
    obj.scale = base
    obj.keyframe_insert("scale", frame=F(t + dur))


def spin(obj, t0, t1, turns=1.0, axis=2):
    r = list(obj.rotation_euler)
    obj.keyframe_insert("rotation_euler", index=axis, frame=F(t0))
    r[axis] += turns * 2 * math.pi
    obj.rotation_euler = r
    obj.keyframe_insert("rotation_euler", index=axis, frame=F(t1))
    fc = obj.animation_data.action.fcurves.find("rotation_euler", index=axis)
    for k in fc.keyframe_points:
        k.interpolation = "LINEAR"


# ---------------------------------------------------------------- objetos
def text(body, font="sans", size=0.4, loc=(0, 0, 0), color=INK, align="CENTER",
         strength=1.0, spacing=1.0, depth=0.0, visible=False, line_h=1.1):
    cu = bpy.data.curves.new("txt", "FONT")
    cu.body = body
    cu.font = FONTS[font]
    cu.size = size
    cu.align_x = align
    cu.align_y = "CENTER"
    cu.space_character = spacing
    cu.space_line = line_h
    cu.extrude = depth
    ob = link(bpy.data.objects.new("txt", cu))
    ob.location = loc
    ob.rotation_euler = (math.pi / 2, 0, 0)
    ob.data.materials.append(mat_emit(color, strength, visible))
    return ob


def mesh_obj(name, bm, mat):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = link(bpy.data.objects.new(name, me))
    ob.data.materials.append(mat)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def sphere(r, loc, mat, seg=48):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=r)
    ob = mesh_obj("sphere", bm, mat)
    ob.location = loc
    return ob


def cone(r1, r2, depth, loc, mat, seg=48):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r1, radius2=r2, depth=depth)
    ob = mesh_obj("cone", bm, mat)
    ob.location = loc
    return ob


def box(size, loc, mat, bevel=0.06):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    ob = mesh_obj("box", bm, mat)
    ob.location = loc
    if bevel:
        mod = ob.modifiers.new("bev", "BEVEL")
        mod.width = bevel
        mod.segments = 4
    for p in ob.data.polygons:
        p.use_smooth = False
    return ob


def torus(R, r, loc, mat, rot=(math.pi / 2, 0, 0)):
    bm = bmesh.new()
    seg, ring = 96, 16
    verts = []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        row = []
        for j in range(ring):
            b = 2 * math.pi * j / ring
            x = (R + r * math.cos(b)) * math.cos(a)
            y = (R + r * math.cos(b)) * math.sin(a)
            z = r * math.sin(b)
            row.append(bm.verts.new((x, y, z)))
        verts.append(row)
    for i in range(seg):
        for j in range(ring):
            bm.faces.new((verts[i][j], verts[(i + 1) % seg][j], verts[(i + 1) % seg][(j + 1) % ring], verts[i][(j + 1) % ring]))
    ob = mesh_obj("torus", bm, mat)
    ob.location = loc
    ob.rotation_euler = rot
    return ob


def person(loc, scale, mat, head_mat=None):
    """Figura humana estilizada: cabeza + vestido/torso. Devuelve el empty padre."""
    root = link(bpy.data.objects.new("person", None))
    root.location = loc
    body = cone(0.62 * scale, 0.2 * scale, 1.6 * scale, (0, 0, 0), mat)
    head = sphere(0.3 * scale, (0, 0, 1.15 * scale), head_mat or mat)
    for o in (body, head):
        o.parent = root
    return root, body, head


def heart(size, loc, mat):
    cu = bpy.data.curves.new("heart", "CURVE")
    cu.dimensions = "2D"
    cu.fill_mode = "BOTH"
    cu.extrude = 0.14
    cu.bevel_depth = 0.0
    sp = cu.splines.new("POLY")
    pts = []
    for i in range(80):
        t = 2 * math.pi * i / 80
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((x * size / 16, y * size / 16, 0, 1))
    sp.points.add(len(pts) - 1)
    for p, c in zip(sp.points, pts):
        p.co = c
    sp.use_cyclic_u = True
    ob = link(bpy.data.objects.new("heart", cu))
    ob.data.materials.append(mat)
    ob.location = loc
    ob.rotation_euler = (math.pi / 2, 0, 0)
    return ob


def line_draw(points, loc, mat, thickness=0.025, t=0.0, dur=0.8):
    """Línea que se dibuja sola (bevel_factor_end animado)."""
    cu = bpy.data.curves.new("line", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = thickness
    cu.bevel_resolution = 4
    sp = cu.splines.new("POLY")
    sp.points.add(len(points) - 1)
    for p, c in zip(sp.points, points):
        p.co = (*c, 1)
    ob = link(bpy.data.objects.new("line", cu))
    ob.location = loc
    ob.data.materials.append(mat)
    cu.bevel_factor_end = 0.0
    cu.keyframe_insert("bevel_factor_end", frame=1)
    cu.keyframe_insert("bevel_factor_end", frame=F(t))
    cu.bevel_factor_end = 1.0
    cu.keyframe_insert("bevel_factor_end", frame=F(t + dur))
    return ob


def area_light(loc, rot, energy, color="#FFFFFF", size=6):
    ld = bpy.data.lights.new("area", "AREA")
    ld.energy = energy
    ld.size = size
    ld.color = lin(color)[:3]
    ob = link(bpy.data.objects.new("area", ld))
    ob.location = loc
    ob.rotation_euler = rot
    return ob


# ---------------------------------------------------------------- entorno global
floor_mat = mat_soft("#140B11", rough=0.32)
floor_mat.blend_method = "OPAQUE"
fl = box((SPACING * 12, 60, 0.1), (SPACING * 4.5, 10, -2.35), floor_mat, bevel=0)

# Partículas de luz (bokeh) a lo largo de todo el recorrido
bm = bmesh.new()
for _ in range(420):
    c = Vector((random.uniform(-15, SPACING * 9 + 15), random.uniform(2, 22), random.uniform(-1.5, 7)))
    r = random.uniform(0.02, 0.06)
    tmp = bmesh.new()
    bmesh.ops.create_icosphere(tmp, subdivisions=1, radius=r)
    bmesh.ops.translate(tmp, vec=c, verts=tmp.verts)
    me_tmp = bpy.data.meshes.new("tmp")
    tmp.to_mesh(me_tmp)
    tmp.free()
    bm.from_mesh(me_tmp)
    bpy.data.meshes.remove(me_tmp)
dust = mesh_obj("dust", bm, mat_emit(LIGHT, 2.5))
dust.location.z = 0
dust.keyframe_insert("location", index=2, frame=1)
dust.location.z = 1.2
dust.keyframe_insert("location", index=2, frame=F(DURATION))

# Luz general: clave rosada desde la izquierda y relleno malva desde la derecha
LIGHTS = [area_light((-6, -6, 6), (math.radians(55), 0, math.radians(-40)), 900, LIGHT, 7),
          area_light((7, -4, 3), (math.radians(70), 0, math.radians(50)), 450, MAUVE, 6),
          area_light((0, 6, 5), (math.radians(-60), 0, 0), 600, PINK, 8)]

# ---------------------------------------------------------------- cámara
cam_d = bpy.data.cameras.new("cam")
cam_d.lens = 50
cam_d.dof.use_dof = True
cam_d.dof.aperture_fstop = 4.0
cam = link(bpy.data.objects.new("cam", cam_d))
scene.camera = cam
cam.rotation_euler = (math.radians(90), 0, 0)
focus = link(bpy.data.objects.new("focus", None))
cam_d.dof.focus_object = focus
rig = link(bpy.data.objects.new("rig", None))
for L in LIGHTS:
    L.parent = rig

# Tiempos de cada escena según la voz (segundos)
SCENES = [0.0, 4.25, 11.1, 19.35, 28.15, 37.4, 48.55, 57.5, 66.9, 74.8, DURATION]
TRANS = 0.55  # duración del paso de cámara entre escenas


def station(i):
    return i * SPACING


for i in range(10):
    x = station(i)
    t0, t1 = SCENES[i], SCENES[i + 1]
    a = t0 + (TRANS / 2 if i else 0)
    b = t1 - TRANS / 2 if i < 9 else t1
    # leve acercamiento durante la escena
    cam.location = (x, -16.0, 0.35)
    cam.keyframe_insert("location", frame=F(a))
    rig.location = (x, 0, 0)
    rig.keyframe_insert("location", frame=F(a))
    rig.keyframe_insert("location", frame=F(b))
    cam.location = (x + 0.25, -15.0, 0.3)
    cam.keyframe_insert("location", frame=F(b))
    if i == 0:
        continue  # el enfoque de la escena 1 se anima aparte
    focus.location = (x, -1.0 if i == 9 else 0, 0.35)
    focus.keyframe_insert("location", frame=F(a))
    focus.location = (x + 0.25, -1.0 if i == 9 else 0, 0.3)
    focus.keyframe_insert("location", frame=F(b))

# ================================================================ ESCENA 1 · Gancho
x = station(0)
woman_mat = mat_soft(MAUVE, rough=0.5, emit=1.6, emit_color=PINK)
w_root, w_body, w_head = person((x, 3.5, -1.55), 1.05, woman_mat)
halo1 = torus(1.15, 0.025, (x, 3.8, -0.4), mat_emit(LIGHT, 3.0, True))
# enfoque: primero el texto nítido y la figura borrosa; luego la figura se aclara
cam_d.dof.aperture_fstop = 1.2
cam_d.dof.keyframe_insert("aperture_fstop", frame=1)
cam_d.dof.keyframe_insert("aperture_fstop", frame=F(4.0))
cam_d.dof.aperture_fstop = 4.0
cam_d.dof.keyframe_insert("aperture_fstop", frame=F(4.6))
cam_d.dof.keyframe_insert("aperture_fstop", frame=F(74.6))
cam_d.dof.aperture_fstop = 2.0
cam_d.dof.keyframe_insert("aperture_fstop", frame=F(75.2))
focus.location = (x, -1.2, 0.35)
focus.keyframe_insert("location", frame=1)
focus.keyframe_insert("location", frame=F(2.9))
focus.location = (x, 3.5, 0.35)
focus.keyframe_insert("location", frame=F(3.8))
focus.keyframe_insert("location", frame=F(4.0))

q1 = text("¿Sientes que entiendes lo que te pasa…", "serif", 0.46, (x, -1.2, 1.65), INK)
q2 = text("…pero no logras cambiarlo?", "italic", 0.52, (x, -1.2, 0.95), LIGHT)
hide_until(q1, 0.15, 0.6)
hide_until(q2, 2.25, 0.6)

# ================================================================ ESCENA 2 · Quién soy
x = station(1)
lotus = link(bpy.data.objects.new("lotus", None))
lotus.location = (x - 3.0, 0, -0.1)
petal_mat = mat_soft(PINK, rough=0.35, emit=0.6, emit_color=LIGHT)
inner_mat = mat_soft(LIGHT, rough=0.35, emit=0.8, emit_color=LIGHT)
petals = []
for ring, (n, rad, length, mat, open_deg) in enumerate([(8, 0.45, 1.0, petal_mat, 62), (5, 0.18, 0.8, inner_mat, 32)]):
    for k in range(n):
        ang = 2 * math.pi * k / n + ring * 0.3
        piv = link(bpy.data.objects.new("piv", None))
        piv.parent = lotus
        piv.rotation_euler = (0, 0, ang)
        hinge = link(bpy.data.objects.new("hinge", None))
        hinge.parent = piv
        hinge.location = (rad, 0, 0)
        pt = sphere(0.5, (0, 0, length * 0.5), mat, seg=32)
        pt.scale = (0.32, 0.12, length * 0.55 / 0.5 * 0.9)
        pt.parent = hinge
        hinge.rotation_euler = (0, math.radians(8), 0)
        hinge.keyframe_insert("rotation_euler", index=1, frame=F(4.3))
        hinge.rotation_euler = (0, math.radians(open_deg), 0)
        hinge.keyframe_insert("rotation_euler", index=1, frame=F(6.8))
        petals.append(hinge)
lotus.rotation_euler = (math.radians(24), 0, 0)
lotus.scale = (1.3, 1.3, 1.3)
spin(lotus, 4.0, 11.5, 0.2)
core = sphere(0.2, (0, 0, 0.15), mat_emit(LIGHT, 6.0, True), 32)
core.parent = lotus

n1 = text("Paola Velásquez", "serif", 0.82, (x - 1.4, 0, 1.05), INK, "LEFT")
n2 = text("Psicóloga  ·  Terapeuta cristiana", "medium", 0.3, (x - 1.4, 0, 0.3), LIGHT, "LEFT", spacing=1.1)
hide_until(n1, 4.45)
hide_until(n2, 5.95)
e1 = text("Entender", "sans", 0.4, (x - 1.4, 0, -0.85), MUTED, "LEFT")
hide_until(e1, 9.1, 0.4, 0.2)
line_draw([(0, 0, 0), (1.3, 0, 0)], (x + 0.6, 0, -0.85), mat_emit(PINK, 3.0), 0.03, 9.6, 0.6)
arrow_head = cone(0.12, 0.0, 0.28, (x + 2.0, 0, -0.85), mat_emit(PINK, 3.0), 24)
arrow_head.rotation_euler = (0, math.radians(90), 0)
pop(arrow_head, 10.15, 0.25)
e2 = text("Transformar", "italic", 0.5, (x + 2.35, 0, -0.85), PINK, "LEFT", strength=1.4)
hide_until(e2, 10.2, 0.5, 0.2)

# ================================================================ ESCENA 3 · Enfoque
x = station(2)
mind = link(bpy.data.objects.new("mind", None))
mind.location = (x - 3.6, 0, 0.75)
bm = bmesh.new()
bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.95)
mind_mesh = mesh_obj("mindmesh", bm, mat_emit(MAUVE, 2.0, True))
mind_mesh.parent = mind
wf = mind_mesh.modifiers.new("wf", "WIREFRAME")
wf.thickness = 0.025
nodes_m = sphere(0.42, (0, 0, 0), mat_soft(PINK, 0.3, 1.5, LIGHT), 32)
nodes_m.parent = mind
pop(mind, 11.25)
spin(mind, 11.25, 19.4, 0.6)

hrt = heart(0.85, (x, 0.0, 0.95), mat_soft(PINK, 0.3, 0.9, PINK))
pop(hrt, 13.5)
hrt.keyframe_insert("rotation_euler", index=2, frame=F(13.5))
hrt.rotation_euler.z = math.radians(25)
hrt.keyframe_insert("rotation_euler", index=2, frame=F(16.5))
hrt.rotation_euler.z = math.radians(-10)
hrt.keyframe_insert("rotation_euler", index=2, frame=F(19.4))

light_orb = sphere(0.6, (x + 3.6, 0, 0.75), mat_emit("#FFE6F1", 8.0, True), 48)
halo = torus(0.95, 0.025, (x + 3.6, 0, 0.75), mat_emit(LIGHT, 3.0, True))
pop(light_orb, 16.85)
pop(halo, 17.0)

l1 = text("Enfoque TCC", "semi", 0.36, (x - 3.6, 0, -0.75), INK)
l1b = text("base científica", "sans", 0.25, (x - 3.6, 0, -1.2), MUTED)
l2 = text("Mirada humana", "semi", 0.36, (x, 0, -0.75), INK)
l3 = text("Tu fe, si tú lo deseas", "semi", 0.36, (x + 3.6, 0, -0.75), INK)
l4 = text("Nunca impuesta.", "italic", 0.32, (x + 3.6, 0, -1.25), LIGHT)
hide_until(l1, 11.4)
hide_until(l1b, 12.3)
hide_until(l2, 13.6)
hide_until(l3, 16.9)
hide_until(l4, 18.2)
ring3 = line_draw([(math.cos(a) * 5.2, 0, math.sin(a) * 0.35) for a in [i * 2 * math.pi / 64 for i in range(65)]],
                  (x, 0.6, 0.75), mat_emit(MAUVE, 1.5), 0.012, 14.0, 4.5)

# ================================================================ ESCENA 4 · Mujeres
x = station(3)
fig_mat = mat_soft(MAUVE, rough=0.45, emit=0.2, emit_color=PINK)
fr, fb, fh = person((x - 1.8, 0, -1.25), 1.45, fig_mat)
pop(fr, 19.5, 0.5, 1.0)
bsdf = fig_mat.node_tree.nodes[fig_mat["bsdf"]]
key_input(bsdf.inputs["Emission Strength"], 0.2, F(24.8))
key_input(bsdf.inputs["Emission Strength"], 2.2, F(26.2))
glow_ring = torus(1.7, 0.03, (x - 1.8, 0.6, 0.35), mat_emit(PINK, 4.0, True))
pop(glow_ring, 25.2, 0.8)
spin(glow_ring, 25.2, 28.4, 0.15, axis=1)

tag_specs = [("Madre", (-3.75, 0.95)), ("Pareja", (-1.8, 2.15)), ("Cuidadora", (-3.6, -0.55))]
for k, (word, (dx, dz)) in enumerate(tag_specs):
    tag = link(bpy.data.objects.new("tag", None))
    tag.location = (x + dx, -0.6, dz)
    plate = box((0.27 * len(word) * 0.62 + 0.5, 0.04, 0.5), (0, 0.04, 0), mat_soft("#5A3450", 0.4, alpha_mix=True), bevel=0.12)
    plate.parent = tag
    tw = text(word, "medium", 0.27, (0, -0.03, 0), LIGHT, visible=True)
    tw.parent = tag
    pop(tag, 20.0 + 0.35 * k, 0.4)
    # se alejan y se desvanecen cuando la voz dice "más allá de los roles"
    out_dir = Vector((dx + 1.8, 0, dz - 0.35)).normalized()
    tag.keyframe_insert("location", frame=F(26.0 + 0.5 * k))
    tag.location = tag.location + out_dir * 2.8 + Vector((0, 1.5, 0))
    tag.keyframe_insert("location", frame=F(27.6 + 0.3 * k))
    fade(plate, 26.4 + 0.5 * k, 0.9, 0.0, 1.0)
    fade(tw, 26.4 + 0.5 * k, 0.9, 0.0, 1.0)

m1 = text("MUJERES", "semi", 0.3, (x + 0.9, 0, 1.2), PINK, "LEFT", spacing=1.35)
m2 = text("Identidad\ny seguridad", "serif", 0.7, (x + 0.9, 0, 0.1), INK, "LEFT", line_h=0.95)
m3 = text("Proceso individual  ·  3 meses", "sans", 0.28, (x + 0.9, 0, -1.05), MUTED, "LEFT")
hide_until(m1, 19.6)
hide_until(m2, 23.4)
hide_until(m3, 21.3)

# ================================================================ ESCENA 5 · Parejas
x = station(4)
cx, cz = x - 2.2, 0.4
couple = link(bpy.data.objects.new("couple", None))
couple.location = (cx, 0, cz)
couple.rotation_euler = (math.radians(70), 0, 0)
orbA = link(bpy.data.objects.new("orbA", None))
orbA.parent = couple
orbB = link(bpy.data.objects.new("orbB", None))
orbB.parent = couple
sA = sphere(0.42, (1.5, 0, 0), mat_soft(PINK, 0.25, 1.0, PINK))
sA.parent = orbA
sB = sphere(0.42, (-1.5, 0, 0), mat_soft(MAUVE, 0.25, 1.0, MAUVE))
sB.parent = orbB
trackA = torus(1.5, 0.012, (0, 0, 0), mat_emit(PINK, 1.6, True), rot=(0, 0, 0))
trackA.parent = couple
trackB = torus(1.5, 0.012, (0.0, 0, 0), mat_emit(MAUVE, 1.6, True), rot=(0, 0, 0))
trackB.parent = couple
# al inicio cada uno gira en su propia órbita (desfasada); luego se sincronizan
trackA.location = (-0.9, 0, 0)
trackB.location = (0.9, 0, 0)
orbA.location = (-0.9, 0, 0)
orbB.location = (0.9, 0, 0)
for o in (trackA, trackB, orbA, orbB):
    o.keyframe_insert("location", frame=F(31.0))
    o.location = (0, 0, 0)
    o.keyframe_insert("location", frame=F(35.6))
orbA.keyframe_insert("rotation_euler", index=2, frame=F(28.2))
orbA.rotation_euler.z = 2 * math.pi * 2.2
orbA.keyframe_insert("rotation_euler", index=2, frame=F(37.6))
orbB.keyframe_insert("rotation_euler", index=2, frame=F(28.2))
orbB.rotation_euler.z = -2 * math.pi * 0.9
orbB.keyframe_insert("rotation_euler", index=2, frame=F(33.0))
orbB.rotation_euler.z = 2 * math.pi * 1.1
orbB.keyframe_insert("rotation_euler", index=2, frame=F(37.6))
pop(couple, 28.3, 0.5)
core5 = sphere(0.16, (0, 0, 0), mat_emit(LIGHT, 7.0, True), 24)
core5.parent = couple
pop(core5, 35.9, 0.5)

p1 = text("PAREJAS", "semi", 0.3, (x + 1.0, 0, 1.35), PINK, "LEFT", spacing=1.35)
p2 = text("Unidos", "serif", 0.95, (x + 1.0, 0, 0.55), INK, "LEFT")
hide_until(p1, 28.6)
hide_until(p2, 29.85)
for k, (w, t) in enumerate([("Comunicación", 31.55), ("Acuerdos", 32.75), ("Manejo de conflictos", 34.1)]):
    dot = sphere(0.06, (x + 1.08, 0, -0.35 - 0.48 * k), mat_emit(PINK, 3.0, True), 16)
    pop(dot, t, 0.3)
    hide_until(text(w, "medium", 0.32, (x + 1.35, 0, -0.35 - 0.48 * k), INK, "LEFT"), t, 0.45, 0.15)
hide_until(text("Un propósito compartido", "italic", 0.36, (x + 1.0, 0, -1.9), LIGHT, "LEFT"), 35.9)

# ================================================================ ESCENA 6 · Hombres
x = station(5)
step_mats = []
for k in range(6):
    m = mat_soft("#3A2233", 0.4, 0.0, PINK)
    step_mats.append(m)
    st = box((0.72, 1.4, 0.32 + 0.3 * k), (x - 4.3 + 0.78 * k, 0.4, -2.2 + (0.32 + 0.3 * k) / 2), m, 0.04)
    pop(st, 37.6 + 0.12 * k, 0.4)
    bs = m.node_tree.nodes[m["bsdf"]]
    t_on = 42.3 + 0.95 * k  # una acción por semana
    key_input(bs.inputs["Emission Strength"], 0.0, F(t_on))
    key_input(bs.inputs["Emission Strength"], 2.6, F(t_on + 0.35))
    num = text(str(k + 1), "semi", 0.3, (x - 4.3 + 0.78 * k, -0.35, -2.2 + 0.32 + 0.3 * k + 0.32), LIGHT)
    hide_until(num, t_on, 0.35, 0.15)
walker_mat = mat_soft(LIGHT, 0.4, 1.2, LIGHT)
wr, wb, wh = person((x - 4.3, 0.4, -2.2 + 0.32 + 0.55), 0.55, walker_mat)
pop(wr, 41.6, 0.4, 1.0)
for k in range(6):
    t_on = 42.3 + 0.95 * k
    wr.location = (x - 4.3 + 0.78 * k, 0.4, -2.2 + 0.32 + 0.3 * k + 0.55)
    wr.keyframe_insert("location", frame=F(t_on + 0.3))
    if k < 5:
        wr.keyframe_insert("location", frame=F(t_on + 0.7))

h1 = text("HOMBRES  ·  ESPOSOS  ·  PADRES", "semi", 0.26, (x + 0.6, 0, 1.4), PINK, "LEFT", spacing=1.25)
h2 = text("De saber\na hacer", "serif", 0.82, (x + 0.6, 0, 0.35), INK, "LEFT", line_h=0.95)
h3 = text("Mentoría  ·  6 semanas  ·  1 acción por semana", "sans", 0.25, (x + 0.6, 0, -0.85), MUTED, "LEFT")
h4 = text("Más dirección y coherencia con su fe", "italic", 0.32, (x + 0.6, 0, -1.4), LIGHT, "LEFT")
h5 = text("Mentoría y formación · no es terapia", "sans", 0.2, (x + 0.6, 0, -2.0), MUTED, "LEFT")
hide_until(h1, 37.6)
hide_until(h2, 39.9)
hide_until(h3, 41.5)
hide_until(h4, 45.5)
hide_until(h5, 46.0)

# ================================================================ ESCENA 7 · Padres
x = station(6)
hx = x - 2.5
wall_mat = mat_soft("#6A3B5C", 0.5, 0.25, MAUVE)
blocks = []
k = 0
for row in range(3):
    for col in range(4):
        bx = hx - 1.35 + col * 0.9 + (0.45 if row % 2 else 0) * 0
        b = box((0.86, 0.9, 0.5), (bx, 0.6, -2.0 + 0.27 + row * 0.52), wall_mat, 0.05)
        b.keyframe_insert("location", index=2, frame=F(48.6 + 0.08 * k))
        z = b.location.z
        b.location.z = z + 4.0
        b.keyframe_insert("location", index=2, frame=1)
        b.keyframe_insert("location", index=2, frame=F(48.6 + 0.08 * k - 0.0001) if False else 1)
        b.location.z = z
        # caen en su sitio
        fcz = None
        blocks.append((b, 48.6 + 0.08 * k))
        k += 1
for b, t in blocks:
    z = b.location.z
    b.animation_data_clear()
    b.location.z = z + 4.5
    b.keyframe_insert("location", index=2, frame=F(t))
    b.location.z = z
    b.keyframe_insert("location", index=2, frame=F(t + 0.45))
roof = cone(2.6, 0.0, 1.3, (hx, 0.6, -0.15 + 1.55), mat_soft(PINK, 0.35, 0.4, PINK), seg=4)
roof.rotation_euler = (0, 0, math.radians(45))
roof.scale = (1.0, 0.45, 1.0)
roof.keyframe_insert("location", index=2, frame=F(49.8))
rz = roof.location.z
roof.location.z = rz + 5
roof.keyframe_insert("location", index=2, frame=1)
roof.keyframe_insert("location", index=2, frame=F(49.6))
roof.location.z = rz
roof.keyframe_insert("location", index=2, frame=F(50.1))
fam_mat = mat_soft(LIGHT, 0.4, 0.0, LIGHT)
fam = []
for dx, sc in ((-0.75, 0.62), (0.75, 0.62), (0.0, 0.42)):
    r, bdy, hd = person((hx + dx, -0.3, -2.25 + 0.62 * sc / 0.62 * 0.8 + 0.05), sc, fam_mat)
    fam.append(r)
    pop(r, 51.6 + 0.2 * len(fam), 0.4, 1.0)
fb_ = fam_mat.node_tree.nodes[fam_mat["bsdf"]]
key_input(fb_.inputs["Emission Strength"], 0.0, F(55.3))
key_input(fb_.inputs["Emission Strength"], 2.5, F(56.4))
heart_small = heart(0.35, (hx, -0.3, 0.9), mat_emit(PINK, 3.5, True))
pop(heart_small, 56.4, 0.5)

c1 = text("PADRES", "semi", 0.3, (x + 0.7, 0, 1.35), PINK, "LEFT", spacing=1.35)
c2 = text("Crianza con\npropósito", "serif", 0.8, (x + 0.7, 0, 0.3), INK, "LEFT", line_h=0.95)
hide_until(c1, 48.7)
hide_until(c2, 50.0)
for k2, (w, t) in enumerate([("Pautas coherentes con tus valores", 52.6), ("Límites", 55.6), ("Acompañamiento emocional", 56.4)]):
    dot = sphere(0.055, (x + 0.78, 0, -0.85 - 0.45 * k2), mat_emit(PINK, 3.0, True), 16)
    pop(dot, t, 0.3)
    hide_until(text(w, "medium", 0.29, (x + 1.02, 0, -0.85 - 0.45 * k2), INK, "LEFT"), t, 0.45, 0.15)

# ================================================================ ESCENA 8 · Objetivo
x = station(7)
stem_mat = mat_soft("#7FBF9A", 0.5, 0.6, "#9AD9B4")
stem = cone(0.06, 0.04, 2.6, (x - 2.6, 0, -2.2 + 1.3), stem_mat, 16)
stem.scale = (1, 1, 0.001)
stem.location.z = -2.2
stem.keyframe_insert("scale", frame=F(58.6))
stem.keyframe_insert("location", frame=F(58.6))
stem.scale = (1, 1, 1)
stem.location.z = -2.2 + 1.3
stem.keyframe_insert("scale", frame=F(65.0))
stem.keyframe_insert("location", frame=F(65.0))
leaf_times = [59.0, 60.4, 62.0, 63.4]
for k, t in enumerate(leaf_times):
    side = -1 if k % 2 else 1
    lf = sphere(0.5, (x - 2.6 + side * 0.42, 0, -1.6 + 0.6 * k), stem_mat, 24)
    lf.scale = (0.62, 0.1, 0.2)
    lf.rotation_euler = (0, math.radians(-25 * side), 0)
    pop(lf, t + 0.1, 0.5, 1.0)
bud = sphere(0.36, (x - 2.6, 0, 0.75), mat_soft(PINK, 0.3, 2.0, LIGHT), 32)
pop(bud, 64.9, 0.6)
spiral_pts = []
for i in range(160):
    a = i / 159 * 4 * math.pi
    r = 0.6 + i / 159 * 1.4
    spiral_pts.append((math.cos(a) * r, math.sin(a) * r * 0.35, -1.8 + i / 159 * 2.9))
line_draw(spiral_pts, (x - 2.6, 0.2, 0), mat_emit(MAUVE, 1.8), 0.015, 58.8, 6.5)

o1 = text("¿El objetivo?", "serif", 0.75, (x + 0.2, 0, 1.4), INK, "LEFT")
hide_until(o1, 57.7)
for k, (w, t) in enumerate([("Comprender tu historia", 59.0), ("Regular tus emociones", 60.4),
                            ("Poner límites sanos", 62.0), ("Relacionarte mejor", 63.4)]):
    num = text(f"0{k + 1}", "semi", 0.26, (x + 0.25, 0, 0.45 - 0.5 * k), PINK, "LEFT")
    hide_until(num, t, 0.4, 0.15)
    hide_until(text(w, "medium", 0.34, (x + 0.8, 0, 0.45 - 0.5 * k), INK, "LEFT"), t, 0.45, 0.15)
hide_until(text("Con pasos pequeños y concretos", "italic", 0.36, (x + 0.2, 0, -1.75), LIGHT, "LEFT"), 64.85)

# ================================================================ ESCENA 9 · Cómo empezar
x = station(8)
phone = link(bpy.data.objects.new("phone", None))
phone.location = (x - 2.6, -0.5, 0.05)
phone.scale = (1.15, 1.15, 1.15)
body_ph = box((1.9, 0.18, 3.7), (0, 0, 0), mat_soft("#2A1924", 0.25), bevel=0.22)
body_ph.parent = phone
screen = box((1.7, 0.02, 3.45), (0, -0.1, 0), mat_emit("#1C1018", 1.0, True), bevel=0.15)
screen.parent = phone
bubbles = [("Hola, quiero agendar", "#3A2233", INK, 0.9, -0.05, 70.0),
           ("¡Hola! Conversemos 30 min", GREEN, "#0E2A18", 0.25, 0.05, 72.5),
           ("Agenda en línea ✓", PINK, "#2B1623", -0.4, -0.05, 73.8)]
for txt_b, bg, fg, bz, bx, t in bubbles:
    bb = box((1.35, 0.02, 0.42), (bx, -0.14, bz), mat_emit(bg, 1.0, True), bevel=0.15)
    bb.parent = phone
    tb = text(txt_b.replace(" ✓", ""), "medium", 0.12, (bx, -0.17, bz), fg, visible=True)
    tb.parent = phone
    pop(bb, t, 0.35)
    pop(tb, t + 0.05, 0.35)
cal = text("100% virtual", "semi", 0.17, (0, -0.15, 1.35), LIGHT, visible=True)
cal.parent = phone
phone.rotation_euler = (0, 0, math.radians(-35))
phone.keyframe_insert("rotation_euler", index=2, frame=F(66.9))
phone.rotation_euler = (0, 0, math.radians(12))
phone.keyframe_insert("rotation_euler", index=2, frame=F(70.0))
phone.rotation_euler = (0, 0, math.radians(-8))
phone.keyframe_insert("rotation_euler", index=2, frame=F(74.8))
pop(phone, 67.0, 0.5)

v1 = text("100%", "serif", 1.05, (x + 0.4, 0, 1.25), PINK, "LEFT", strength=1.3)
v2 = text("virtual", "italic", 0.55, (x + 2.75, 0, 1.12), INK, "LEFT")
hide_until(v1, 67.5)
hide_until(v2, 68.0)
hide_until(text("Tu primer paso:", "medium", 0.3, (x + 0.45, 0, 0.25), MUTED, "LEFT"), 69.1)
hide_until(text("una conversación\nde 30 minutos", "serif", 0.46, (x + 0.45, 0, -0.55), INK, "LEFT", line_h=0.95), 70.2)
hide_until(text("WhatsApp  ·  Agenda en línea", "semi", 0.32, (x + 0.45, 0, -1.6), GREEN, "LEFT"), 72.4)

# ================================================================ ESCENA 10 · Cierre
x = station(9)
lotus2 = link(bpy.data.objects.new("lotus2", None))
lotus2.location = (x, 1.5, 1.15)
for n, rad, length, mat, open_deg, off in [(8, 0.45, 1.0, petal_mat, 62, 0), (5, 0.18, 0.8, inner_mat, 32, 0.3)]:
    for k in range(n):
        piv = link(bpy.data.objects.new("piv", None))
        piv.parent = lotus2
        piv.rotation_euler = (0, 0, 2 * math.pi * k / n + off)
        hinge = link(bpy.data.objects.new("hinge", None))
        hinge.parent = piv
        hinge.location = (rad, 0, 0)
        hinge.rotation_euler = (0, math.radians(open_deg), 0)
        pt = sphere(0.5, (0, 0, length * 0.5), mat, 32)
        pt.scale = (0.32, 0.12, length * 0.55 / 0.5 * 0.9)
        pt.parent = hinge
lotus2.rotation_euler = (math.radians(22), 0, 0)
lotus2.scale = (0.75, 0.75, 0.75)
spin(lotus2, 74.5, DURATION, 0.15)
cl1 = text("Comprende tu historia.", "serif", 0.62, (x, -1.0, -0.15), INK)
cl2 = text("Construye nuevas posibilidades.", "italic", 0.55, (x, -1.0, -0.95), PINK, strength=1.3)
cl3 = text("paolavelasquez.com   ·   @terapeutacristianapaola", "medium", 0.24, (x, -1.0, -1.75), LIGHT)
cl4 = text("Los programas y mentorías no sustituyen un proceso psicoterapéutico ni garantizan resultados específicos.",
           "sans", 0.13, (x, -1.0, -2.2), MUTED)
hide_until(cl1, 75.0)
hide_until(cl2, 76.5)
hide_until(cl3, 78.0)
hide_until(cl4, 78.6, 0.6, 0.05)

# Fundido a negro al final
fade_plane = box((40, 0.01, 30), (0, -12.0, 0), mat_emit(BG, 1.0, False), bevel=0)
fade_plane.parent = cam
fade_plane.location = (0, 0, -1.0)
fade_plane.rotation_euler = (math.radians(-90), 0, 0)
fade(fade_plane, DURATION - 1.2, 1.1, 1.0, 0.0)
mixf = mix_of(fade_plane)
key_input(mixf.inputs[0], 0.0, 1)

# Fundido desde negro al inicio
fade_in = box((40, 0.01, 30), (0, 0, -1.01), mat_emit(BG, 1.0, True), bevel=0)
fade_in.parent = cam
fade_in.rotation_euler = (math.radians(-90), 0, 0)
fade(fade_in, 0.0, 0.6, 0.0, 1.0)

# ---------------------------------------------------------------- audio y salida
scene.sequence_editor_create()
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print("BUILD_OK", OUT_BLEND, scene.frame_end)
