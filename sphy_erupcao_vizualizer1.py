import hashlib
import numpy as np
import pyarrow.parquet as pq
import time
from ursina import *

# ================== WINDOW CONFIG - SAFE 1920x1080 ==================
window.title = "Solar Eruption - Harpia Model"
window.borderless = False

# Configurações seguras com try/except
try:
    window.size = (1920, 1080)
    print("Janela configurada em 1920x1080")
except:
    print("Não foi possível definir tamanho 1920x1080")

try:
    window.position = (0, 0)
except:
    pass

# Configurações opcionais (ignoradas se não existirem)
try:
    window.fps_counter.enabled = True
except:
    pass

try:
    window.cog_button.visible = False
except:
    pass

# ================== LOAD DATA ==================
print("\nLoading Parquet file...")
table = pq.read_table("erupcao_solar.parquet")
df = table.to_pandas()

print(f"✅ Loaded {len(df)} frames")

# ================== ROBUST VERTEX CONVERSION ==================
def convert_to_vertices(vertex_data):
    try:
        arr = np.asarray(vertex_data, dtype=np.float32)
        if arr.ndim == 2 and arr.shape[1] == 3:
            return arr
        return arr.reshape(-1, 3)
    except:
        pass
    
    try:
        flat = []
        for point in vertex_data:
            flat.extend(point)
        arr = np.array(flat, dtype=np.float32)
        return arr.reshape(-1, 3)
    except:
        pass
    
    flat = np.fromiter((float(x) for sublist in vertex_data for x in sublist), dtype=np.float32)
    return flat.reshape(-1, 3)


print("Converting vertices...")
vertex_arrays = [convert_to_vertices(df.iloc[i]['vertices']) for i in range(len(df))]
print(f"✅ Conversion completed: {len(vertex_arrays)} frames")

# ================== SHA256 VALIDATION ==================
print("Validating SHA256 signatures...")
valid = sum(1 for i in range(len(df)) 
            if hashlib.sha256(vertex_arrays[i].tobytes()).hexdigest() == df.iloc[i]['sha256'])
print(f"✅ {valid}/{len(df)} frames are valid\n")

# ================== VISUALIZATION ==================
app = Ursina()

GRID_SIZE = int(table.schema.metadata.get(b'grid_size', 60))

# Create triangles
tris = []
for x in range(GRID_SIZE - 1):
    for y in range(GRID_SIZE - 1):
        i = x * GRID_SIZE + y
        tris.append((i, i + 1, i + GRID_SIZE))
        tris.append((i + 1, i + GRID_SIZE + 1, i + GRID_SIZE))

terrain = Entity(
    model=Mesh(
        vertices=[Vec3(*v) for v in vertex_arrays[0]], 
        triangles=tris, 
        mode='triangle'
    ),
    texture='white_cube',
    color=color.orange,
    double_sided=True
)

frame_index = 0

def update():
    global frame_index
    if frame_index >= len(df):
        frame_index = 0

    verts = vertex_arrays[frame_index]
    terrain.model.vertices = [Vec3(*v) for v in verts]
    terrain.model.generate()

    if df.iloc[frame_index].get('is_erupting', False):
        terrain.color = lerp(color.yellow, color.red, (time.time() * 12 % 2))
    else:
        terrain.color = color.orange

    frame_index += 1

def input(key):
    global frame_index
    if key in ('r', 'R'):
        frame_index = 0
        print("🔄 Animation restarted")
    if key == 'escape':
        quit()

EditorCamera()
Sky()

Text("🌞 Solar Eruption - Harpia Model\nPress R to Restart", 
     y=0.45, origin=(0,0), scale=1.5, background=True)

print("🎬 Visualization started! Press R to restart")
app.run()
