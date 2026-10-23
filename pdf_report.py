import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Leer datos
df = pd.read_excel("datos_hotel2.xlsx")

# Calcular KPIs
df["Ocupacion_%"] = ((df["Habitaciones_vendidas"] / df["Habitaciones_disponibles"]) * 100).round(1)
df["ADR"] = (df["Ingresos"] / df["Habitaciones_vendidas"]).round(2)
df["RevPAR"] = (df["Ingresos"] / df["Habitaciones_disponibles"]).round(2)

# Crear PDF
doc = SimpleDocTemplate("reporte_mensual.pdf", pagesize=A4)
styles = getSampleStyleSheet()
elementos = []

# Título
elementos.append(Paragraph("Monthly Hotel Performance Report", styles["Title"]))
elementos.append(Spacer(1, 20))

# Tabla de datos
encabezados = ["Month", "Revenue", "Rooms Sold", "Occupancy %", "ADR", "RevPAR"]
filas = [encabezados]

for _, row in df.iterrows():
    filas.append([
        row["Mes"],
        f"€{row['Ingresos']:,}",
        str(row["Habitaciones_vendidas"]),
        f"{row['Ocupacion_%']}%",
        f"€{row['ADR']}",
        f"€{row['RevPAR']}"
    ])

tabla = Table(filas)
tabla.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

elementos.append(tabla)
elementos.append(Spacer(1, 20))

# Resumen
elementos.append(Paragraph(f"Average Occupancy: {df['Ocupacion_%'].mean():.1f}%", styles["Normal"]))
elementos.append(Paragraph(f"Average ADR: €{df['ADR'].mean():.2f}", styles["Normal"]))
elementos.append(Paragraph(f"Average RevPAR: €{df['RevPAR'].mean():.2f}", styles["Normal"]))
elementos.append(Paragraph(f"Best month: {df.loc[df['Ocupacion_%'].idxmax(), 'Mes']}", styles["Normal"]))

doc.build(elementos)
print("PDF generado: reporte_mensual.pdf")