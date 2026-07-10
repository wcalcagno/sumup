---
noteId: "1ed427307c6411f182a82541cc79c7e6"
tags: []

---

# Taller 3: IA Avanzada

**Plataforma:** Langdock
**Duracion:** 2 horas
**Facilitador:** Walter E. Calcagno, Microsoft MVP Data Platform
**Fecha:** 10 de julio de 2026

> La IA acelera. El criterio firma.

---

## Contenidos

- Integracion con datasets internos
- Analisis multimodal aplicado a casos de negocio
- Prototipos rapidos de soluciones internas

## Agenda

| Bloque | Min | Contenido |
|---|---|---|
| Apertura | 10 | Encuadre y reglas del taller |
| Ejercicio 1 | 45 | El Analista de Cartera que no puede mentir |
| Puesta en comun | 10 | Autopsia de errores |
| Ejercicio 2 | 45 | Mesa de Recepcion Multimodal |
| Cierre | 10 | Rubrica y checklist de produccion |

## Formato

**Trabajo individual.** Cada participante tiene su propio notebook y su propia sesion en
Langdock. Cada uno construye su agente completo, de principio a fin. Nadie se apoya en
el compañero que sabe Python.

La validacion, en cambio, es **cruzada y en duplas**. Terminada la construccion, cada
participante se sienta frente al notebook del vecino y aplica la bateria adversarial
sobre el agente ajeno, mientras el vecino hace lo mismo con el suyo. Luego se devuelven
los hallazgos.

El motivo es sencillo: atacar el agente propio prueba la honestidad intelectual de uno.
Atacar el agente ajeno prueba el artefacto. Solo lo segundo produce un hallazgo que el
autor no habia anticipado, porque nadie encuentra el supuesto que no sabe que tiene.

Si el numero de participantes es impar, el facilitador toma el notebook sobrante y ataca
sin piedad. Es la mejor demostracion del dia.

### Convencion de nombres (obligatoria)

Con 20 o 30 personas en un mismo workspace, los objetos colisionan. Cada participante
sufija sus objetos con sus iniciales:

| Objeto | Nombre |
|---|---|
| Agente ejercicio 1 | `analista_cartera_XX` |
| Workflow ejercicio 2 | `mesa_recepcion_XX` |
| Formulario | `rendicion_XX` |

La **Carpeta de Conocimiento la crea el facilitador una sola vez** (`politica_retail_andes`)
y la comparte con todo el workspace en rol Viewer. Nadie sube el PDF de nuevo. Treinta
copias del mismo documento embebido es exactamente el problema de gobierno de datos que
este taller enseña a no cometer.

## Prerrequisitos

- Un notebook por participante, con sesion iniciada antes de que empiece el taller
- Cuenta en Langdock con acceso a modelos Anthropic (Claude Opus, Sonnet, Haiku)
- Herramientas habilitadas por el administrador: Analisis de Datos, Carpetas de
  Conocimiento, Workflows
- Permiso para crear Agentes y compartirlos en el workspace

Verificar antes del taller: una herramienta esta disponible solo si esta habilitada en
el workspace, habilitada en las preferencias del usuario, habilitada en el agente, y
soportada por el modelo elegido. Las cuatro condiciones, simultaneamente.

## Por que tres modelos

| Nodo | Modelo | Razon |
|---|---|---|
| Analista, extraccion, contraste | Claude Sonnet | Salida estructurada y tool use, temperatura baja |
| Validacion adversarial | Claude Opus | Razonamiento sobre reglas en conflicto |
| Clasificacion de veredicto | Claude Haiku | Alto volumen, decision determinista, costo bajo |

Elegir modelo es una decision de arquitectura, no de gusto. Un pipeline con un solo
modelo para todo o paga de mas o razona de menos.

## Estructura

```
datasets/       insumos con defectos plantados (ver soluciones/)
prompts/        system prompts listos para pegar en Langdock
workflows/      especificacion nodo por nodo
validacion/     bateria adversarial y rubrica
soluciones/     solucionario (publicar al cierre)
deck/           presentacion del taller
```

## Ejercicio 1: El Analista de Cartera que no puede mentir

Retail Andes SpA. La Gerencia pide cifras de cartera. Exige que toda cifra sea
auditable contra el dato fuente y que toda pregunta fuera de alcance reciba una
negativa explicita.

1. Diagnostico de ingesta con Analisis de Datos (8 min, individual)
2. Trampa deliberada: intentar subir el CSV a una Carpeta de Conocimiento (4 min)
3. Construccion del agente `analista_cartera_XX` (20 min, individual)
4. Validacion cruzada en duplas (13 min): 7 minutos atacando el agente del vecino,
   6 minutos recibiendo y clasificando los hallazgos sobre el propio

**Entregable:** agente compartido **con el facilitador** en rol Viewer (no con todo el
workspace), tabla de las cinco pruebas anotada por el vecino, y un parrafo respondiendo:
que defecto de dato haria inviable poner esto en produccion manana?

## Ejercicio 2: Mesa de Recepcion Multimodal

Rendiciones de gastos de terreno: fotos de boletas, audio del trabajador, planillas
manuscritas. Extraer, validar contra la politica, y decidir.

1. Extraccion multimodal con esquema JSON y escala de confianza (12 min, individual)
2. Cruce con dato interno (8 min, individual)
3. Prototipo en Workflow `mesa_recepcion_XX` con Guardrails y Human in the Loop (20 min)
4. El caso que debe fallar (5 min, en duplas: cada uno somete el audio contradictorio al
   workflow del vecino)

**Entregable:** workflow publicado en v1.0.0, captura del run que atrapo la
contradiccion, y una linea sobre que decision de ese flujo jamas deberia quedar sin
firma humana.

## Reglas del taller

1. Nadie entrega una cifra sin trazabilidad.
2. Cada participante construye su propio agente. No se reparte el trabajo.
3. Nadie valida su propio agente. Se valida el del vecino, y el vecino valida el suyo.
4. Un agente que responde todo esta reprobado antes de empezar.
5. Al cierre, cada participante nombra en voz alta la decision de su flujo que requiere
   firma humana. Sin leer. Si no la recuerda, no la diseño.

## Generar los datasets

```bash
python generar_datasets.py
python generar_politicas.py
```

Los assets multimodales (imagenes y audios) se producen segun
`datasets/ejercicio2/MANIFEST.md`.

## Licencia

CC BY 4.0. Atribucion: Walter E. Calcagno, autor de *Arquitectura e Ingenieria de
Datos* (Anaya Multimedia, 2024).
