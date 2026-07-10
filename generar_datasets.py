# MANIFEST de assets multimodales, Ejercicio 2

Los archivos binarios (imagenes y audios) no se versionan en este repositorio.
Este manifiesto especifica **exactamente** que debe contener cada asset, que defecto
encarna y cual es el veredicto correcto segun `politica_gastos.pdf`.

Producirlos toma unos 20 minutos: fotografiar boletas reales (o imprimir las
plantillas de `plantillas_boleta.md`), y grabar los audios con el celular.

Nomenclatura: `NN_descripcion.ext`. Cargar todo en `imagenes/` y `audios/`.

---

## Imagenes

| # | Archivo | Contenido | Defecto plantado | Veredicto correcto |
|---|---|---|---|---|
| 1 | `01_boleta_almuerzo.jpg` | Boleta de restaurante. RUT 76.412.883-K, 03-07-2026, total $18.400. CC-1010. | ninguno | APROBAR |
| 2 | `02_boleta_bencina.jpg` | Boleta de servicentro. RUT 96.856.780-2, 03-07-2026, total $52.000. Categoria Transporte. CC-1020. | supera el tope de $40.000 | ESCALAR a jefatura |
| 3 | `03_boleta_materiales.jpg` | Boleta ferreteria. RUT 77.033.190-4, 01-07-2026, total $96.500. CC-2010. | ninguno | APROBAR |
| 4 | `04_boleta_borrosa.jpg` | Misma boleta que #3, fotografiada fuera de foco. El total no se lee. | ilegibilidad, confianza esperada < 0,70 | ESCALAR a revision manual |
| 5 | `05_boleta_duplicada.jpg` | La boleta #1 fotografiada desde otro angulo y con otra luz. | duplicidad: mismo RUT + fecha + total | RECHAZAR por duplicidad |
| 6 | `06_planilla_manuscrita.jpg` | Hoja cuadriculada escrita a mano con tres gastos y una suma. Sin RUT emisor. | no es boleta ni factura | RECHAZAR |
| 7 | `07_captura_dashboard.png` | Captura de un dashboard de Power BI con un KPI de gasto mensual. | no es respaldo de gasto, es un reporte | RECHAZAR |
| 8 | `08_foto_perro.jpg` | Fotografia de un perro. | entrada fuera de dominio | RECHAZAR |
| 9 | `09_boleta_cc_cerrado.jpg` | Boleta valida, RUT 76.100.220-1, 02-07-2026, total $14.900, imputada a **CC-9090**. | centro de costo con `activo = 0` | RECHAZAR |

## Audios

| # | Archivo | Guion aproximado (30 s) | Defecto plantado | Efecto esperado |
|---|---|---|---|---|
| A | `A_relato_coherente.mp3` | "Almorce con el cliente el tres de julio, gaste dieciocho mil cuatrocientos pesos, va al centro de costo diez diez." | ninguno | refuerza APROBAR de #1 |
| B | `B_relato_contradictorio.mp3` | "Cargue bencina el tres de julio, fueron treinta y ocho mil pesos, alcanza justo dentro del tope." | contradice el total de #2 ($52.000 en la boleta) | RECHAZAR y escalar a Contraloria |

---

## Plantillas de boleta (si no dispone de boletas reales)

Genere las boletas #1, #2, #3, #5 y #9 con `plantillas_boleta.md`, imprimalas,
arruguelas un poco y fotografielas con el celular. La imperfeccion es parte del
ejercicio: una imagen escaneada y perfecta no ensena nada sobre extraccion multimodal.

Para la #4, fotografie la #3 con la camara en movimiento.

## Regla del facilitador

No revele el veredicto correcto antes de la ronda de validacion. El valor pedagogico
esta en que cada participante descubra, de boca de su vecino de dupla, que su propio
agente aprobo la foto del perro.
