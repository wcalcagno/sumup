# Nodos de validacion

## 1. Nodo `transcribir_y_contrastar`

| Parametro | Valor |
|---|---|
| Modelo | Anthropic Claude Sonnet |
| Temperatura | 0,1 |
| Entrada | audio del formulario + `{{extraer_boleta.output}}` |

### Instrucciones

Recibes un audio del trabajador y el JSON extraido de su boleta.

1. Transcribe el audio literalmente.
2. Extrae del relato: monto mencionado, fecha mencionada, categoria mencionada, centro
   de costo mencionado. Lo que no se mencione va a `null`.
3. Compara **campo a campo** contra el JSON de la boleta.

Una contradiccion existe cuando el relato afirma un valor distinto del documento en un
campo obligatorio. El silencio del relato no es contradiccion. Una diferencia de monto
menor a $1.000 atribuible a redondeo verbal tampoco lo es: registrala como
`discrepancia_menor`.

Devuelve solo este JSON:

```json
{
  "transcripcion": "string",
  "campos_del_relato": { "total": 0, "fecha": null, "categoria": null, "centro_costo": null },
  "contradicciones": [
    { "campo": "total", "en_documento": 52000, "en_relato": 38000, "severidad": "ALTA" }
  ],
  "discrepancias_menores": [],
  "veredicto_contraste": "COHERENTE | DISCREPANCIA_MENOR | CONTRADICTORIO"
}
```

Regla que no puedes relajar: **prevalece el documento**. El relato jamas corrige,
completa ni sobrescribe un campo del documento. Si el trabajador dice un monto y la
boleta dice otro, el sistema no elige el menor ni el mas probable: marca
`CONTRADICTORIO`.

---

## 2. Nodo `Guardrails` (validar_extraccion)

Valida la salida de `extraer_boleta` **antes** de cualquier ramificacion. Si alguna
condicion falla, el flujo se enruta a revision manual, nunca a aprobacion.

| # | Verificacion | Condicion de aprobacion |
|---|---|---|
| G1 | JSON parseable con las 11 claves del esquema | verdadero |
| G2 | `tipo_documento` pertenece al enumerado | verdadero |
| G3 | `confianza_0_1` es numero en [0, 1] | verdadero |
| G4 | Si `tipo_documento` es BOLETA o FACTURA, entonces `total` es entero > 0 | verdadero |
| G5 | `fecha` cumple `AAAA-MM-DD` y no es futura respecto de hoy | verdadero |
| G6 | `monto_neto + iva` difiere de `total` en a lo mas 2 pesos | verdadero |
| G7 | `rut_emisor` tiene digito verificador valido (modulo 11) | verdadero |
| G8 | `campos_ilegibles` vacio si `confianza_0_1` >= 0,90 | verdadero |

G6 y G7 son los que atrapan la alucinacion aritmetica: un modelo que "completo" el
total ilegible casi siempre produce una suma que cuadra pero un RUT que no, o al reves.

G8 atrapa la incoherencia interna: declarar alta confianza y a la vez campos ilegibles
es una contradiccion que el modelo comete cuando el prompt no fijo la escala.

---

## 3. Nodo `decidir_veredicto`

| Parametro | Valor |
|---|---|
| Modelo | Anthropic Claude Haiku |
| Temperatura | 0 |

Clasificacion de bajo costo, alto volumen. Recibe el JSON validado, el resultado del
contraste, la fila del centro de costo y el texto de la politica. Aplica la tabla de la
seccion 3 de `politica_gastos.pdf` en orden y devuelve:

```json
{
  "veredicto": "APROBAR | ESCALAR | RECHAZAR",
  "regla_aplicada": "cita textual de la politica",
  "requiere_firma_humana": true
}
```

`requiere_firma_humana` es `true` siempre que `total > 100000`, sin importar el
veredicto ni la confianza. Esa condicion no es negociable por el modelo y se verifica
tambien en el nodo `Condition`, aguas abajo. Una regla que solo vive en el prompt es
una recomendacion; una regla que ademas vive en el grafo es un control.
