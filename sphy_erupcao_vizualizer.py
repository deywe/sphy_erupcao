import hashlib
import numpy as np
import pyarrow.parquet as pq
import time
from ursina import *

# ================== CONFIGURAÇÃO ==================
PARQUET_FILE = "erupcao_solar.parquet"

# ================== CARREGAR ==================
print("Carregando Parquet...")
table = pq.read_table(PARQUET_FILE)
df = table.to_pandas()

print(f"✅ {len(df)} frames carregados")

# ================== CONVERSÃO ULTRA ROBUSTA ==================
def convert_to_vertices(vertex_data):
    """Múltiplas estratégias para converter vertices"""
    # Estratégia 1: Converter para array e reshape
    try:
        arr = np.asarray(vertex_data, dtype=np.float32)
        if arr.ndim == 2 and arr.shape[1] == 3:
            return arr
        else:
            return arr.reshape(-1, 3)
    except:
        pass
    
    # Estratégia 2: Flatten manual
    try:
        flat = []
        for point in vertex_data:
            flat.extend(point)
        arr = np.array(flat, dtype=np.float32)
        return arr.reshape(-1, 3)
    except:
        pass
    
    # Estratégia 3: Último recurso
    flat = np.fromiter((float(x) for sublist in vertex_data for x in sublist), dtype=np.float32)
    return flat.reshape(-1, 3)


print("Convertendo vértices...")
vertex_arrays = []
for i in range(len(df)):
    try:
        va = convert_to_vertices(df.iloc[i]['vertices'])
        vertex_arrays.append(va)
    except Exception as e:
        print(f"Erro no frame {i}: {e}")
        break

print(f"✅ Conversão concluída: {len(vertex_arrays)} frames")

# ================== VALIDAÇÃO SHA256 ==================
print("Validando SHA256...")
valid = 0
for i in range(len(df)):
    computed = hashlib.sha256(vertex_arrays[i].tobytes()).hexdigest()
    if computed == df.iloc[i]['sha256']:
        valid += 1
print(f"✅ {valid}/{len(df)} frames válidos\n")

# ================== VISUALIZAÇÃO ==================
app = Ursina()

GRID_SIZE = int(table.schema.metadata.get(b'grid_size', 60))

# Criar triângulos (igual ao código original)
tris = []
for x in range(GRID_SIZE - 1):
    for y in range(GRID_SIZE - 1):
        i = x * GRID_SIZE + y
        tris.append((i, i + 1, i + GRID_SIZE))
        tris.append((i + 1, i + GRID_SIZE + 1, i + GRID_SIZE))

# Primeiro frame
first_verts = vertex_arrays[0]

terrain = Entity(
    model=Mesh(vertices=[Vec3(*v) for v in first_verts], 
               triangles=tris, 
               mode='triangle'),
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
        print("🔄 Reiniciado")

EditorCamera()
Sky()
Text("🌞 Erupção Solar - Modelo Harpia\nR = Reiniciar", y=0.45, origin=(0,0), scale=1.5, background=True)

print("🎬 Iniciando visualização...")
app.run()
