# 📊 Optimización de Medios Publicitarios

Aplicación desarrollada con **Python, Streamlit y PuLP** para resolver un problema de optimización de un plan de medios con presupuesto limitado.

## Problema

Se deben seleccionar canales publicitarios para maximizar el impacto sin superar el presupuesto.

Datos iniciales:

| Canal | Costo | Impacto |
|---|---:|---:|
| TV | 8 | 14 |
| Radio | 3 | 5 |
| Redes sociales | 4 | 7 |
| Prensa | 2 | 3 |

Presupuesto inicial: **9**

La solución óptima inicial es:

- Radio
- Redes sociales
- Prensa

Costo total: **9**

Impacto total: **15**

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Desplegar en Streamlit Community Cloud

1. Sube `app.py` y `requirements.txt` a un repositorio de GitHub.
2. Entra a Streamlit Community Cloud.
3. Conecta tu cuenta de GitHub.
4. Selecciona el repositorio.
5. Selecciona `app.py` como archivo principal.
6. Pulsa Deploy.

La aplicación permite modificar el presupuesto, los costos y los impactos desde la interfaz.
