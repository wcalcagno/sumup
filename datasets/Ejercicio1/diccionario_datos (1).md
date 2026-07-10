---
noteId: "ed98a8407c6211f182a82541cc79c7e6"
tags: []

---

# Diccionario de Datos, Comercial

Retail Andes SpA. Mantenido por el equipo de Datos Maestros.
Ultima revision: marzo 2025. Estado: **incompleto**.

> Nota del equipo: quedaron campos sin documentar tras la salida de la analista
> responsable. No asuma el significado de un campo que no aparece aqui. Preguntelo.

---

## ventas_2025.csv

| Campo | Tipo | Descripcion |
|---|---|---|
| `id_venta` | texto | Folio del documento de venta. Formato `F-nnnnnn`. Se espera unico, no esta garantizado por constraint. |
| `fecha` | texto | Fecha de emision del documento. **No esta normalizada.** Conviven al menos tres formatos de escritura. |
| `rut_cliente` | texto | RUT del cliente. Sin normalizar (con puntos, sin puntos, sin guion, digito verificador en minuscula). |
| `id_producto` | texto | (sin documentar) |
| `cantidad` | entero | (sin documentar) |
| `monto_neto` | numerico | Monto neto en pesos chilenos, sin IVA. Ver seccion 3 de la Politica Comercial 2026 antes de sumarlo. |
| `canal` | texto | (sin documentar) |
| `vendedor` | texto | (sin documentar) |
| `tipo_documento` | texto | (sin documentar) |

## clientes.csv

| Campo | Tipo | Descripcion |
|---|---|---|
| `rut_cliente` | texto | Clave de negocio. **No es clave primaria de esta tabla.** |
| `razon_social` | texto | (sin documentar) |
| `segmento` | texto | Ver Politica Comercial 2026, seccion 4. |
| `region` | texto | (sin documentar) |
| `limite_credito` | numerico o texto | Ver Politica Comercial 2026, seccion 5. |
| `fecha_inicio_vigencia` | fecha | Inicio de vigencia de la version del registro. |
| `fecha_fin_vigencia` | fecha | (sin documentar) |
| `vigente` | entero | (sin documentar) |

---

## Campos que NO existen en ninguna fuente publicada

Se dejan explicitos porque son los mas solicitados por la Gerencia:

- costo unitario
- costo de venta
- margen
- rentabilidad por producto o por cliente
- fecha de pago o de cobranza
- descuento efectivamente aplicado

Estos datos residen en SAP CO y no estan disponibles para esta iniciativa.
