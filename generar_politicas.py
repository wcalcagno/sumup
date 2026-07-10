"""Genera los dos PDF de politica usados como Carpeta de Conocimiento."""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=15, spaceAfter=10)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=11.5, spaceBefore=10, spaceAfter=5)
P = ParagraphStyle("P", parent=ss["BodyText"], fontSize=9.5, leading=13.5, spaceAfter=5)

TSTYLE = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#333333")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
])


def build(path, flow):
    SimpleDocTemplate(
        path, pagesize=LETTER,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    ).build(flow)
    print("OK", path)


# ===========================================================================
# 1. Politica comercial
# ===========================================================================
f = []
f.append(Paragraph("Retail Andes SpA", H1))
f.append(Paragraph("Politica Comercial 2026 (vigente desde 01-01-2026)", P))
f.append(Paragraph("Documento interno. Version 3.2. Aprobado por Directorio, sesion N 118.", P))
f.append(Spacer(1, 8))

f.append(Paragraph("1. Alcance", H2))
f.append(Paragraph(
    "Este documento norma la clasificacion de clientes, la politica de descuentos y los "
    "limites de credito de Retail Andes SpA. <b>Este documento no define costos, margenes "
    "ni rentabilidad.</b> Todo calculo de margen requiere informacion del sistema de costos "
    "(SAP CO), el cual se encuentra fuera del alcance de esta politica y de los datasets "
    "publicados por Comercial.", P))

f.append(Paragraph("2. Definicion oficial de Cliente Activo", H2))
f.append(Paragraph(
    "Un cliente se considera <b>ACTIVO</b> a una fecha de corte determinada si, y solo si, "
    "cumple simultaneamente las tres condiciones siguientes:", P))
f.append(Paragraph(
    "a) Registra al menos una venta facturada en los ultimos 90 dias corridos anteriores a la "
    "fecha de corte.<br/>"
    "b) El valor absoluto de sus notas de credito en ese periodo no supera el 20% del monto "
    "bruto facturado en el mismo periodo.<br/>"
    "c) Su ficha maestra presenta exactamente <b>una</b> fila vigente. Un cliente con cero o "
    "con dos o mas filas vigentes se considera <b>INDETERMINADO</b> y no puede ser clasificado "
    "hasta que Datos Maestros corrija la ficha.", P))
f.append(Paragraph(
    "La fecha de corte oficial para los reportes del ejercicio 2025 es el <b>31-12-2025</b>.", P))

f.append(Paragraph("3. Registro de notas de credito", H2))
f.append(Paragraph(
    "Por una limitacion historica del ERP, las notas de credito se registran en la misma tabla "
    "de ventas con el campo <b>monto_neto</b> en valor negativo, conservando el valor "
    "'VENTA' en el campo tipo_documento. No existe hoy un indicador que las distinga. "
    "Toda suma de ventas debe explicitar si incluye o excluye montos negativos.", P))

f.append(Paragraph("4. Descuentos maximos por segmento", H2))
f.append(Table([
    ["Segmento", "Descuento maximo", "Autoriza"],
    ["Minorista", "8%", "Ejecutivo de cuenta"],
    ["Mayorista", "15%", "Jefe Comercial"],
    ["Institucional", "22%", "Gerente Comercial"],
], colWidths=[5 * cm, 5 * cm, 6 * cm], style=TSTYLE))

f.append(Paragraph("5. Limites de credito", H2))
f.append(Paragraph(
    "El campo limite_credito de la ficha maestra expresa pesos chilenos. Un valor ausente o "
    "no numerico significa que el cliente <b>no tiene linea de credito asignada</b> y opera "
    "unicamente al contado. No debe interpretarse como limite cero ni como limite infinito.", P))

f.append(Paragraph("6. Canales de venta reconocidos", H2))
f.append(Paragraph(
    "Tienda, Ecommerce, Televenta y Distribuidor. Cualquier otro valor en el campo canal, "
    "incluido el texto 'NULL', corresponde a un registro incompleto y debe ser reportado, "
    "no imputado.", P))

f.append(Paragraph("7. Trazabilidad", H2))
f.append(Paragraph(
    "Toda cifra reportada a la Gerencia debe poder reconstruirse indicando: archivo fuente, "
    "columna, filtro aplicado y tratamiento de duplicados. Un reporte sin trazabilidad se "
    "considera no emitido.", P))

build("datasets/ejercicio1/politica_comercial_2026.pdf", f)


# ===========================================================================
# 2. Politica de gastos
# ===========================================================================
f = []
f.append(Paragraph("Retail Andes SpA", H1))
f.append(Paragraph("Politica de Rendicion de Gastos de Terreno. Version 2.1", P))
f.append(Spacer(1, 8))

f.append(Paragraph("1. Topes por categoria", H2))
f.append(Table([
    ["Categoria", "Tope", "Unidad"],
    ["Alimentacion", "$25.000", "por dia por persona"],
    ["Transporte", "$40.000", "por dia"],
    ["Alojamiento", "$60.000", "por noche"],
    ["Materiales", "$150.000", "por evento"],
    ["Otros", "$20.000", "por evento"],
], colWidths=[5.5 * cm, 4.5 * cm, 6 * cm], style=TSTYLE))
f.append(Paragraph(
    "Los topes se expresan sobre el <b>monto total con IVA incluido</b>. La tasa de IVA "
    "vigente es 19%.", P))

f.append(Paragraph("2. Requisitos de respaldo", H2))
f.append(Paragraph(
    "a) Boleta o factura legible que permita leer, como minimo: RUT del emisor, fecha de "
    "emision y monto total.<br/>"
    "b) Centro de costo indicado y con estado activo = 1 en la maestra de centros de costo. "
    "Un gasto imputado a un centro de costo inactivo se rechaza sin excepcion.<br/>"
    "c) El relato verbal del trabajador es informacion complementaria. <b>No sustituye el "
    "respaldo documental.</b> Si el relato contradice el documento, prevalece el documento y "
    "el caso se escala.", P))

f.append(Paragraph("3. Reglas de decision", H2))
f.append(Table([
    ["Condicion", "Veredicto"],
    ["Respaldo legible, centro activo, total <= tope", "APROBAR"],
    ["Total > tope de la categoria", "ESCALAR a jefatura del centro de costo"],
    ["Confianza de extraccion menor a 0,70", "ESCALAR a revision manual"],
    ["Campo obligatorio ilegible o ausente", "ESCALAR a revision manual"],
    ["Centro de costo con activo = 0", "RECHAZAR"],
    ["El documento no es una boleta ni factura", "RECHAZAR"],
    ["Relato en audio contradice el documento", "RECHAZAR y escalar a Contraloria"],
    ["Mismo RUT emisor + fecha + total ya rendido", "RECHAZAR por duplicidad"],
], colWidths=[9.5 * cm, 6.5 * cm], style=TSTYLE))

f.append(Paragraph("4. Duplicidad", H2))
f.append(Paragraph(
    "Dos rendiciones son el mismo gasto si coinciden RUT del emisor, fecha de emision y monto "
    "total, aunque las fotografias sean distintas, esten tomadas desde otro angulo o tengan "
    "distinta iluminacion.", P))

f.append(Paragraph("5. Autoridad de firma", H2))
f.append(Paragraph(
    "Ningun gasto superior a $100.000 puede quedar aprobado sin firma humana registrada, "
    "cualquiera sea el nivel de confianza del sistema de extraccion automatica. La "
    "automatizacion propone; la jefatura firma.", P))

build("datasets/ejercicio2/politica_gastos.pdf", f)
