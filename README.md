# 📊 Optimización de Medios Publicitarios

Aplicación de programación lineal entera binaria desarrollada con Python, Streamlit y PuLP.

## Datos iniciales

| Canal | Costo | Impacto |
|---|---:|---:|
| TV | 8 | 14 |
| Radio | 3 | 5 |
| Redes sociales | 4 | 7 |
| Prensa | 2 | 3 |

Presupuesto inicial: **9**

### Solución óptima

- Radio
- Redes sociales
- Prensa

Costo total: **9**
Impacto total: **15**

## Ejecutar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud

Sube `app.py`, `requirements.txt` y `README.md` a GitHub y despliega `app.py`.

### Compatibilidad

El proyecto usa **PuLP 2.9.0** y la API clásica:

```python
pulp.LpVariable(...)
modelo.solve()
```

No utiliza `add_variable()` ni depende directamente de `PULP_CBC_CMD`, evitando problemas de compatibilidad entre versiones de PuLP.
