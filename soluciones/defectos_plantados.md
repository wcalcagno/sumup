# Defectos plantados (solo facilitador)

No publicar antes del cierre del taller.

Todas las cifras de este documento fueron **verificadas contra los archivos generados**
con `seed = 20260710`. Si regeneras los datasets con esa semilla, obtienes exactamente
estos valores.

---

## `ventas_2025.csv` (14.935 filas)

| # | Defecto | Cifra real | Impacto si no se detecta |
|---|---|---|---|
| 1 | Tres formatos de fecha | 8.212 en `AAAA-MM-DD`, 4.474 en `DD-MM-AAAA`, 2.249 en `DD/MM/AA` | Un parser ingenuo descarta o malinterpreta el 15%. Marzo y julio se confunden |
| 2 | RUT en cuatro formatos | 5.942 con puntos, 6.752 sin puntos, 1.982 sin guion, 178 con `k` minuscula | El join con `clientes.csv` pierde filas en silencio |
| 3 | `"NULL"` como texto | 429 en `canal`, 715 en `vendedor` | Ver la nota critica mas abajo |
| 4 | Notas de credito como monto negativo | 291 filas. `tipo_documento` sigue diciendo `VENTA` | Toda suma de ventas es ambigua sin leer la politica |
| 5 | Duplicados exactos | 118 filas identicas repetidas | Sobreestimacion de ventas |
| 6 | `id_venta` repetidos | 134 folios aparecen mas de una vez | 118 son duplicados exactos, 16 tienen **monto distinto**. `drop_duplicates()` solo caza los primeros |
| 7 | Montos como texto | 40 filas con `"949810,00"` | La columna se lee como `object`. Una suma ingenua concatena o falla |

No existe columna de costo. La pregunta de margen es irrespondible por construccion.

---

## La nota critica: el `NULL` invisible

Este es el hallazgo mas valioso del ejercicio y **no lo planee asi**.

`pandas.read_csv()` convierte por defecto la cadena `"NULL"` en `NaN`. Es decir: los 429
canales rotos y los 715 vendedores rotos **desaparecen** en cuanto alguien carga el
archivo con la configuracion por defecto, que es lo que hara la herramienta de Analisis
de Datos de Langdock.

```python
import pandas as pd
v = pd.read_csv("ventas_2025.csv")
(v.canal == "NULL").sum()          # 0.  El defecto no existe.

v = pd.read_csv("ventas_2025.csv", keep_default_na=False)
(v.canal == "NULL").sum()          # 429. El defecto siempre estuvo ahi.
```

El agente va a reportar, con total sinceridad, que no hay valores `NULL` textuales. Y va
a tener razon segun lo que vio. La herramienta se los comio antes de que los mirara.

Como usarlo: cuando alguien afirme en la puesta en comun que "el campo canal esta
limpio", proyecta las dos lineas de arriba. La leccion no es sobre pandas. Es que **toda
capa de ingesta impone supuestos silenciosos**, y un agente que no los declara no es
trazable aunque cite archivo, columna y filtro. La trazabilidad se detiene donde empieza
el default de la libreria.

Nadie lo encuentra sin ayuda. Guardalo para el final.

---

## `clientes.csv` (27 filas)

| # | Defecto | RUT afectado |
|---|---|---|
| 8 | SCD2 roto: dos filas `vigente = 1` | **76476979-9**. Una fila Mayorista con limite 2.000.000 desde 2023-09-03, otra Institucional con limite 40.000.000 desde 2025-03-01. Ambas vigentes |
| 9 | Rangos de vigencia solapados | **71634481-8**. Version cerrada del 2024-06-01 al 2025-12-31, y version vigente iniciada el 2024-01-01. La vieja empieza despues de la nueva |
| 10 | `limite_credito = "NULL"` | **75804200-K** y **78934391-2**. Segun la seccion 5 de la politica significa "sin linea de credito", no cero |

El defecto 8 hace que `76476979-9` sea **INDETERMINADO** segun la seccion 2c de la
Politica Comercial, y por tanto no clasificable como activo ni inactivo. Un agente que
entrega un conteo de clientes activos sin mencionar este caso, no leyo la politica.

Para localizarlos en vivo:

```python
import pandas as pd
c = pd.read_csv("clientes.csv", keep_default_na=False)
vig = c[c.vigente == 1].rut_cliente.value_counts()
print(vig[vig > 1])                       # defecto 8
print(c[c.limite_credito == "NULL"])      # defecto 10
```

---

## `centros_costo.csv`

| # | Defecto |
|---|---|
| 11 | `CC-9090` tiene `activo = 0` y `tope_mensual_clp = 0`. Cualquier gasto imputado ahi se rechaza. El tope cero no es un tope: es un centro cerrado |

---

## Las cuatro cifras de marzo

Todas son correctas. Todas son distintas. Ninguna es defendible sin declarar su criterio.

| Criterio | Venta de marzo 2025 |
|---|---|
| Todo, tal cual | $520.757.286 |
| Excluyendo montos negativos | $534.766.446 |
| Removiendo duplicados exactos | $515.406.486 |
| Sin duplicados y sin negativos | $529.415.646 |

Marzo tiene 1.213 filas. La diferencia entre la primera y la segunda es de **catorce
millones**, y proviene enteramente de decidir si una nota de credito resta o no resta.
Esa decision no la toma el modelo. La toma la seccion 3 de la politica, y solo si
alguien la leyo.

Un quinto criterio produce una cifra distinta: quien parsee las fechas sin contemplar el
formato `DD/MM/AA` perdera aproximadamente el 15% de las filas de marzo y obtendra un
numero mas bajo que los cuatro anteriores. Ese es el error mas comun.

---

## Guion de la puesta en comun (10 min)

1. Pide su cifra de venta de marzo a tres participantes elegidos al azar. **Nunca
   coinciden las tres.** Con trabajo individual esto es mas nitido que en equipos: son
   tres criterios distintos, no tres negociaciones internas.

2. Pregunta a la sala cual esta bien. Nadie puede saberlo sin leer la trazabilidad de
   cada uno. Ese es el punto, y hay que dejarlo incomodo por unos segundos.

3. Proyecta la tabla de las cuatro cifras. Las cuatro son correctas.

4. Ahora proyecta las dos lineas de `keep_default_na`. Hay una quinta cosa que ninguno
   de los tres vio, y que su agente les oculto con absoluta buena fe.

5. Cierra: la IA acelero el calculo en los tres casos, con la misma velocidad y la misma
   seguridad aparente. Lo que separo una cifra defendible de una indefendible no estuvo
   en el modelo. Estuvo en quien definio el criterio y lo dejo por escrito.

---

## Ejercicio 2: veredictos correctos

| Asset | Veredicto | Regla |
|---|---|---|
| `01_boleta_almuerzo.jpg` | APROBAR | $18.400 bajo el tope de $25.000 |
| `02_boleta_bencina.jpg` | ESCALAR a jefatura | $52.000 supera el tope de $40.000 |
| `03_boleta_materiales.jpg` | APROBAR | $96.500 bajo el tope de $150.000 |
| `04_boleta_borrosa.jpg` | ESCALAR a revision manual | confianza < 0,70 |
| `05_boleta_duplicada.jpg` | RECHAZAR | mismo RUT + fecha + total que la 01 |
| `06_planilla_manuscrita.jpg` | RECHAZAR | no es boleta ni factura, sin RUT emisor |
| `07_captura_dashboard.png` | RECHAZAR | es un reporte, no un respaldo tributario |
| `08_foto_perro.jpg` | RECHAZAR | fuera de dominio |
| `09_boleta_cc_cerrado.jpg` | RECHAZAR | `CC-9090` tiene `activo = 0` |
| `02` + `B_relato_contradictorio.mp3` | RECHAZAR y escalar a Contraloria | el relato dice $38.000, el documento dice $52.000 |

La trampa del `03`: son $96.500, bajo el tope de Materiales. Pero **supera los $100.000?
No.** Esta a $3.500 del umbral de firma humana obligatoria de la seccion 5. Es el caso
que mas discusion genera, y la respuesta correcta es aprobar. Sirve para mostrar que un
umbral es un umbral, no una intuicion.
