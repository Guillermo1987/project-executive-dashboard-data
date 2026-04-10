# Executive Dashboard 360° — Business Intelligence

## Qué es este proyecto
Proyecto de Business Intelligence que define la estructura de datos y KPIs para un **Dashboard Ejecutivo 360°**. Integra métricas de Finanzas, Marketing y RevOps en una única fuente de verdad lista para Power BI, Tableau o Looker.

Proyecto de portafolio LinkedIn — demuestra capacidades de BI, RevOps y análisis financiero.

## Stack técnico
- **Python:** Pandas, NumPy
- **Output:** CSV listo para herramientas BI (Power BI, Tableau, Looker)
- **Visualización objetivo:** Dashboard ejecutivo con KPIs de negocio

## Archivos clave
- `generate_data.py` — genera 12 meses de datos sintéticos realistas con tendencia y estacionalidad
- `executive_dashboard_data.csv` — dataset final con todos los KPIs calculados
- `README.md` — documentación del proyecto y KPIs incluidos

## KPIs implementados

| Área | Métricas |
|------|----------|
| **Finanzas** | Revenue, Cost of Goods, Profit, Gross Margin % |
| **Marketing** | Marketing Spend, New Customers, CAC |
| **RevOps** | Churn Rate, MRR, Net Revenue Retention |

## Cómo ejecutar
```bash
pip install pandas numpy
python generate_data.py
# Genera: executive_dashboard_data.csv
```

## Extensiones posibles
- Conectar con datos reales via API (CRM, ERP, Google Analytics)
- Añadir capa de visualización con Streamlit o Dash
- Automatizar la actualización de datos con n8n
- Añadir comparativas vs período anterior y forecasting

## Relevancia para el portafolio
Demuestra: BI estratégico, RevOps, análisis financiero, preparación de datos y data storytelling.
Roles objetivo: BI Analyst, RevOps Analyst, Analytics Engineer.
