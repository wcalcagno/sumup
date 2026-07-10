# Workflow: Mesa de Recepcion Multimodal

Prerrequisito: el administrador del workspace debe tener Workflows habilitado.

Cada participante construye el suyo en su propio notebook y lo nombra `mesa_recepcion_XX`,
donde `XX` son sus iniciales. El formulario del trigger se nombra `rendicion_XX`. Sin esa
convencion, treinta workflows homonimos vuelven inutilizable el workspace en veinte
minutos.

## Grafo

```
[1] Trigger: Formulario
        |
[2] Agent: extraer_boleta            (Claude Sonnet, temp 0.1)
        |
[3] Agent: transcribir_y_contrastar  (Claude Sonnet, temp 0.1)
        |
[4] Guardrails: validar_extraccion   (G1 a G8)
        |
[5] Agent: decidir_veredicto         (Claude Haiku, temp 0)
        |
[6] Condition: enrutar
        |
        |-- rama A: APROBAR y total <= 100000
        |        -> [7] Send Notification: "Gasto aprobado"
        |
        |-- rama B: ESCALAR, o total > 100000
        |        -> [8] Human in the Loop: aprobacion de jefatura
        |               |
        |               |-- aprobado  -> [7]
        |               |-- rechazado -> [9]
        |
        `-- rama C: RECHAZAR, o Guardrails fallido, o veredicto_contraste = CONTRADICTORIO
                 -> [9] Send Notification: "Rechazado, ver motivo"
```

## Nodos

### [1] Trigger: Formulario

| Campo | Tipo | Obligatorio |
|---|---|---|
| `foto_respaldo` | archivo (imagen) | si |
| `audio_relato` | archivo (audio) | no |
| `centro_costo` | texto | si |
| `email_solicitante` | texto | si |

Formulario publico (sin login) para simular al trabajador en terreno.

### [2] `extraer_boleta`
Prompt en `prompts/extraccion_boleta.md`. Entrada: `{{form1.output.foto_respaldo}}`.

### [3] `transcribir_y_contrastar`
Prompt en `prompts/guardrails.md`, seccion 1.
Entradas: `{{form1.output.audio_relato}}` y `{{extraer_boleta.output.structured}}`.

Si no hay audio, este nodo devuelve `veredicto_contraste = "COHERENTE"` con
`transcripcion` vacia. Configurar el manejo de error del nodo como **continuar**, no
como fallar el workflow.

### [4] Guardrails `validar_extraccion`
Verificaciones G1 a G8. En fallo: enrutar a la rama C. **No** continuar.

### [5] `decidir_veredicto`
Entradas: JSON validado, contraste, fila de `centros_costo.csv` filtrada por
`{{form1.output.centro_costo}}`, y el texto de `politica_gastos.pdf` desde la carpeta
de conocimiento (nodo `File Search` previo, o carpeta adjunta al agente).

### [6] Condition
Expresiones sugeridas:

```
Rama C: {{validar_extraccion.output.passed}} == false
     || {{decidir_veredicto.output.veredicto}} == "RECHAZAR"
     || {{transcribir_y_contrastar.output.veredicto_contraste}} == "CONTRADICTORIO"

Rama B: {{decidir_veredicto.output.veredicto}} == "ESCALAR"
     || {{extraer_boleta.output.structured.total}} > 100000

Rama A: resto
```

El orden importa. La rama C se evalua primero. Un flujo que evalua primero la
aprobacion aprueba antes de mirar la contradiccion.

### [8] Human in the Loop
Aprobador: responsable del centro de costo (columna `responsable`). Mensaje que debe
ver la jefatura: monto, categoria, regla citada, confianza de extraccion, y
transcripcion del audio. Nunca solo el veredicto: quien firma necesita ver la evidencia
que produjo el veredicto, no el veredicto.

## Publicacion

1. Probar nodo por nodo con el boton de play, empezando por [2]. Nunca el flujo
   completo primero: cuando falla, nadie sabe donde.
2. Test run con una boleta limpia. Debe recorrer el camino feliz.
3. Test run con al menos dos assets que consideres invalidos. Elige tu cuales.
4. Probar las tres ramas. El camino feliz siempre funciona: no prueba nada.
5. Publicar como **v1.0.0** (Major).

Un workflow en Draft no responde a triggers reales. La distincion draft / published es
control de cambios, y aplica igual que en cualquier pipeline de datos: lo que corre en
produccion es una version inmutable, no el editor de alguien.

## Errores tipicos observados

- Nodos llamados "Agente 1" y "Agente 2". Al tercer nodo nadie sabe cual es cual.
- El Guardrail puesto **despues** de la ramificacion. Valida lo que ya se decidio.
- `Human in the Loop` ausente porque "la confianza era 0,94". La confianza mide la
  lectura de la imagen, no la legitimidad del gasto.
- Probar solo el camino feliz. El camino feliz siempre funciona.
