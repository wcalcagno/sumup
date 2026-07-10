"""
Generador de datasets sinteticos para el Taller 3: IA Avanzada (Langdock).
Los defectos NO son accidentales. Estan plantados y documentados en
soluciones/defectos_plantados.md

Uso: python generar_datasets.py
"""
import random
import csv
from datetime import date, timedelta

random.seed(20260710)

OUT1 = "datasets/ejercicio1"
OUT2 = "datasets/ejercicio2"

# ---------------------------------------------------------------------------
# Utilidades de RUT chileno
# ---------------------------------------------------------------------------
def dv(num: int) -> str:
    s, m = 0, 2
    for d in reversed(str(num)):
        s += int(d) * m
        m = 9 if m == 7 else m + 1
    r = 11 - (s % 11)
    return {11: "0", 10: "K"}.get(r, str(r))


def rut_limpio(num: int) -> str:
    return f"{num}-{dv(num)}"


def rut_con_puntos(num: int) -> str:
    return f"{num:,}".replace(",", ".") + "-" + dv(num)


def rut_sucio(num: int) -> str:
    """Devuelve el RUT en uno de cuatro formatos incompatibles."""
    estilo = random.random()
    if estilo < 0.40:
        return rut_con_puntos(num)
    if estilo < 0.75:
        return rut_limpio(num)
    if estilo < 0.90:
        return f"{num}{dv(num)}"              # sin guion
    return rut_limpio(num).lower()            # k minuscula


# ---------------------------------------------------------------------------
# Dimension de clientes
# ---------------------------------------------------------------------------
NOMBRES = [
    "Comercial Andina", "Distribuidora Sur", "Ferreteria El Roble", "Minimarket Ñuñoa",
    "Almacenes Pacifico", "Importadora Cordillera", "Retail Maipo", "Bodegas Elqui",
    "Abarrotes Los Andes", "Supermercados Biobio", "Casa Matriz Valparaiso",
    "Proveedora Atacama", "Mayorista Chiloe", "Tiendas Aconcagua", "Central Rancagua",
    "Depositos Talca", "Comercial Osorno", "Distribuidora Arica", "El Trebol SpA",
    "Surtidora Coronel", "Comercial Temuco", "Almacen Puerto Montt", "Insumos Iquique",
    "Grupo Curico", "Provisiones Chillan",
]
SEGMENTOS = ["Mayorista", "Minorista", "Institucional"]
REGIONES = ["RM", "Valparaiso", "Biobio", "Araucania", "Antofagasta", "Los Lagos"]

base_ruts = [random.randint(70_000_000, 79_999_999) for _ in range(25)]
clientes = []
for i, num in enumerate(base_ruts):
    inicio = date(2023, 1, 1) + timedelta(days=random.randint(0, 400))
    clientes.append({
        "rut_cliente": rut_limpio(num),
        "razon_social": NOMBRES[i],
        "segmento": random.choice(SEGMENTOS),
        "region": random.choice(REGIONES),
        "limite_credito": random.choice([2_000_000, 5_000_000, 10_000_000, 25_000_000]),
        "fecha_inicio_vigencia": inicio.isoformat(),
        "fecha_fin_vigencia": "",
        "vigente": 1,
    })

# --- DEFECTO SCD2 #1: dos filas vigentes para el mismo cliente (rut indice 3)
c = dict(clientes[3])
c["segmento"] = "Institucional"
c["limite_credito"] = 40_000_000
c["fecha_inicio_vigencia"] = "2025-03-01"
c["vigente"] = 1
clientes.append(c)

# --- DEFECTO SCD2 #2: rangos de vigencia solapados (indice 10)
c = dict(clientes[10])
c["region"] = "RM"
c["fecha_inicio_vigencia"] = "2024-06-01"
c["fecha_fin_vigencia"] = "2025-12-31"
c["vigente"] = 0
clientes.append(c)
clientes[10]["fecha_inicio_vigencia"] = "2024-01-01"   # se solapa con la fila anterior

# --- DEFECTO: limite_credito como texto "NULL" en dos filas
clientes[7]["limite_credito"] = "NULL"
clientes[18]["limite_credito"] = "NULL"

random.shuffle(clientes)
with open(f"{OUT1}/clientes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(clientes[0].keys()))
    w.writeheader()
    w.writerows(clientes)

# ---------------------------------------------------------------------------
# Hechos de venta
# ---------------------------------------------------------------------------
PRODUCTOS = [f"SKU-{n:04d}" for n in range(1001, 1041)]
CANALES = ["Tienda", "Ecommerce", "Televenta", "Distribuidor"]
VENDEDORES = ["V-01", "V-02", "V-03", "V-04", "V-05", "V-06"]

def fecha_sucia(d: date) -> str:
    estilo = random.random()
    if estilo < 0.55:
        return d.isoformat()                       # 2025-03-14
    if estilo < 0.85:
        return d.strftime("%d-%m-%Y")              # 14-03-2025
    return d.strftime("%d/%m/%y")                  # 14/03/25


filas = []
inicio = date(2025, 1, 1)
for i in range(1, 14_801):
    d = inicio + timedelta(days=random.randint(0, 364))
    cantidad = random.randint(1, 60)
    unitario = random.choice([1990, 3490, 5990, 8990, 12990, 24990, 49990])
    neto = cantidad * unitario
    tipo = "VENTA"
    # --- DEFECTO: notas de credito como monto negativo, sin columna que las marque
    if random.random() < 0.022:
        neto = -neto
        tipo = "VENTA"          # a proposito: el tipo NO revela la nota de credito
    filas.append({
        "id_venta": f"F-{i:06d}",
        "fecha": fecha_sucia(d),
        "rut_cliente": rut_sucio(random.choice(base_ruts)),
        "id_producto": random.choice(PRODUCTOS),
        "cantidad": cantidad,
        "monto_neto": neto,
        "canal": random.choice(CANALES) if random.random() > 0.03 else "NULL",
        "vendedor": random.choice(VENDEDORES) if random.random() > 0.05 else "NULL",
        "tipo_documento": tipo,
    })

# --- DEFECTO: 120 duplicados exactos
for f_ in random.sample(filas, 120):
    filas.append(dict(f_))

# --- DEFECTO: 15 id_venta repetidos con montos distintos (duplicado NO exacto)
for f_ in random.sample(filas[:14_800], 15):
    g = dict(f_)
    g["monto_neto"] = int(g["monto_neto"]) + random.randint(1000, 90_000)
    filas.append(g)

# --- DEFECTO: 40 filas con monto como string y coma decimal
for f_ in random.sample(filas, 40):
    f_["monto_neto"] = f"{abs(int(f_['monto_neto']))},00"

random.shuffle(filas)
with open(f"{OUT1}/ventas_2025.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
    w.writeheader()
    w.writerows(filas)

# ---------------------------------------------------------------------------
# Centros de costo (Ejercicio 2)
# ---------------------------------------------------------------------------
centros = [
    ("CC-1010", "Operaciones Terreno Norte", "M. Fuentes", 1_200_000, 1),
    ("CC-1020", "Operaciones Terreno Centro", "P. Alvarado", 1_800_000, 1),
    ("CC-1030", "Operaciones Terreno Sur", "R. Sandoval", 900_000, 1),
    ("CC-2010", "Mantenimiento", "J. Rivas", 2_500_000, 1),
    ("CC-2020", "Logistica", "C. Herrera", 3_000_000, 1),
    ("CC-3010", "Comercial", "A. Bustos", 1_500_000, 1),
    ("CC-9090", "Proyecto Piloto Cerrado", "sin asignar", 0, 0),   # activo = 0, trampa
]
with open(f"{OUT2}/centros_costo.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["codigo", "nombre", "responsable", "tope_mensual_clp", "activo"])
    w.writerows(centros)

print("Datasets generados.")
print(f"  ventas_2025.csv : {len(filas)} filas")
print(f"  clientes.csv    : {len(clientes)} filas")
print(f"  centros_costo.csv: {len(centros)} filas")
