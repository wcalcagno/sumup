# Taller 3: IA Avanzada

**Plataforma:** Langdock
**Duracion:** 2 horas
**Facilitador:** Walter E. Calcagno, Microsoft MVP Data Platform

> La IA acelera. El criterio firma.

---

## Que vas a construir

Dos cosas, y ninguna es un chatbot que responda bien.

**Un agente** que contesta preguntas de negocio sobre datasets internos, que cita el
archivo y la columna de cada cifra que entrega, y que se niega explicitamente cuando la
respuesta no esta en sus fuentes.

**Un workflow multimodal** que procesa fotografias, audio y documentos, y que escala a un
humano antes de aprobar lo que no debe aprobar solo.

No es un taller de prompting. Es un taller sobre donde poner la firma humana en un
proceso automatizado.

## Contenidos

- Integracion con datasets internos
- Analisis multimodal aplicado a casos de negocio
- Prototipos rapidos de soluciones internas

## Agenda

| Bloque | Min | Contenido |
|---|---|---|
| Apertura | 10 | Encuadre y reglas |
| Ejercicio 1 | 45 | El Analista de Cartera que no puede mentir |
| Puesta en comun | 10 | Autopsia de errores |
| Ejercicio 2 | 45 | Mesa de Recepcion Multimodal |
| Cierre | 10 | Rubrica y checklist de produccion |

---

## Antes de empezar

**No hay nada que instalar.** Langdock corre en el navegador y Python se ejecuta en el
servidor. No necesitas Python, ni Anaconda, ni Git.

Verifica estos cinco puntos hoy, te toma cinco minutos:

1. Abro Langdock en Chrome o Edge y veo mi workspace
2. En el selector de modelo aparecen Claude Opus, Sonnet y Haiku
3. Abro un chat, adjunto un CSV cualquiera y le pido que cuente las filas. Responde con
   un numero
4. Veo la opcion de crear un **Agente**
5. Veo la opcion de crear un **Workflow**

Si alguno falla, avisa antes de la sesion. Es configuracion de administrador.

**Descarga este repositorio y descomprimelo en tu escritorio**, con los archivos a un
clic. El dialogo de adjuntar archivo del navegador es donde se pierden los minutos.

## Los datos

Los datasets ya estan generados y versionados. **No hay que ejecutar nada.** Trabaja
directamente sobre:

- `datasets/ejercicio1/` para el Analista de Cartera
- `datasets/ejercicio2/` para la Mesa de Recepcion

Los datos son sinteticos. Retail Andes SpA no existe. Los defectos que encuentres en
ellos, en cambio, existen en todas partes.

---

## Formato

**Trabajo individual.** Cada uno construye su agente completo, de principio a fin. Nadie
se apoya en el compañero que sabe Python.

**Validacion cruzada en duplas.** Terminada la construccion, te sientas frente al
notebook de tu vecino y aplicas la bateria de `validacion/bateria_adversarial.md` sobre
su agente, mientras el hace lo mismo con el tuyo. Despues se devuelven los hallazgos.

Atacar el agente propio prueba la honestidad intelectual de uno. Atacar el agente ajeno
prueba el artefacto. Solo lo segundo produce un hallazgo que el autor no habia
anticipado, porque nadie encuentra el supuesto que no sabe que tiene.

Se ataca el artefacto, no a la persona. Un hallazgo se enuncia "el agente aprobo X sin
citar la politica", nunca "configuraste mal el prompt".

### Convencion de nombres, obligatoria

Somos muchos en un mismo workspace. Sufija tus objetos con tus iniciales:

| Objeto | Nombre |
|---|---|
| Agente ejercicio 1 | `analista_cartera_XX` |
| Workflow ejercicio 2 | `mesa_recepcion_XX` |
| Formulario del trigger | `rendicion_XX` |

La Carpeta de Conocimiento la crea el facilitador **una sola vez** y la comparte en rol
Viewer. Nadie sube el PDF de nuevo. Treinta copias del mismo documento embebido, sin
version canonica y sin forma de saber cual leyo cada agente, es precisamente el problema
que este taller enseña a no cometer.

### Los prompts

En `prompts/` estan los system prompts listos para pegar. Usarlos no es hacer trampa: la
nota no esta en escribir el prompt, esta en lo que sobrevive al ataque de tu vecino.

---

## Ejercicio 1: El Analista de Cartera que no puede mentir

Retail Andes SpA. La Gerencia Comercial pide cifras de cartera. Exige que toda cifra sea
auditable contra el dato fuente y que toda pregunta fuera de alcance reciba una negativa
explicita.

| Min | Tarea | Como |
|---|---|---|
| 8 | Diagnostico de ingesta con Analisis de Datos. Anota cinco defectos por escrito | individual |
| 4 | Intenta subir el CSV a una Carpeta de Conocimiento. Observa que pasa | individual |
| 20 | Construye `analista_cartera_XX` con el prompt de `prompts/agente_analista.md` | individual |
| 7 | Ejecuta la bateria adversarial sobre el agente de tu vecino | en duplas |
| 6 | Recibe los hallazgos sobre el tuyo y clasificalos | en duplas |

**Entregable.** Agente compartido con el facilitador en rol Viewer, la hoja de las cinco
pruebas anotada por tu vecino, y un parrafo respondiendo: que defecto de dato haria
inviable poner esto en produccion mañana?

## Ejercicio 2: Mesa de Recepcion Multimodal

Rendiciones de gastos de terreno. Entran fotos de boletas, un audio del trabajador y a
veces una planilla escrita a mano. Salen tres veredictos posibles: aprobar, rechazar o
escalar, con la regla de la politica citada textualmente.

| Min | Tarea | Como |
|---|---|---|
| 12 | Extraccion multimodal a JSON estricto, con escala de confianza | individual |
| 8 | Cruce contra `centros_costo.csv` y `politica_gastos.pdf` | individual |
| 20 | Prototipo `mesa_recepcion_XX` con Guardrails y Human in the Loop | individual |
| 5 | Somete al workflow de tu vecino el caso que crees que lo rompe | en duplas |

**Entregable.** Workflow publicado en v1.0.0, captura de una corrida que atrapo un caso
invalido, y una linea sobre que decision de ese flujo jamas deberia quedar sin firma
humana.

---

## Reglas

1. Nadie entrega una cifra sin trazabilidad.
2. Cada uno construye su propio agente. No se reparte el trabajo.
3. Nadie valida su propio agente.
4. Un agente que responde todo esta reprobado antes de empezar.
5. Al cierre, cada uno nombra en voz alta la decision de su flujo que requiere firma
   humana. Sin leer. Si no la recuerda, no la diseño.

## Estructura

```
datasets/       insumos de ambos ejercicios
prompts/        system prompts listos para pegar en Langdock
workflows/      especificacion nodo por nodo
validacion/     bateria adversarial y rubrica
```

El solucionario y los generadores de datos se publican **al cierre del taller**, no antes.

## Licencia

CC BY 4.0. Atribucion: Walter E. Calcagno, autor de *Arquitectura e Ingenieria de Datos*
(Anaya Multimedia, 2024).
