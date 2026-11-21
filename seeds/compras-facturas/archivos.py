"""Genera los archivos que la serie «Compras · Entrada de facturas» sube al buzón (datos ficticios, RNC 130555xxx).
    python3 seeds/compras-facturas/archivos.py
- facturas-plantilla.xlsx: la plantilla del buzón llena con dos facturas (video 5).
- reporte-dgii-ecf-recibidos.xlsx: el reporte «e-CF recibidos» de la Oficina Virtual de la DGII con tres comprobantes (video 6).
Las fechas se calculan desde hoy para que nunca queden en el futuro ni demasiado viejas."""
from datetime import date, datetime, timedelta
from pathlib import Path

import openpyxl

AQUI = Path(__file__).resolve().parent
HOY = date.today()
EMPRESA_RNC = "130555001"


def plantilla():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Facturas"
    ws.append(["Factura", "RNC proveedor", "Proveedor", "NCF", "Tipo NCF", "Fecha emisión (AAAA-MM-DD)",
               "Concepto", "Cantidad", "Precio unitario", "ITBIS"])
    f1 = (HOY - timedelta(days=6)).isoformat()
    f2 = (HOY - timedelta(days=4)).isoformat()
    filas = [
        ["F-1", "130555133", "Lubricantes Germiva", "E310000002201", "31", f1, "Aceite de motor 15W-40 galón", 6, 1150.00, 1242.00],
        ["F-1", "130555133", "Lubricantes Germiva", "E310000002201", "31", f1, "Filtro de aceite", 2, 475.00, 171.00],
        ["F-2", "130555141", "Climatización Germiva", "E310000088410", "31", f2, "Mantenimiento de aires acondicionados", 1, 4200.00, 756.00],
    ]
    for f in filas:
        ws.append(f)
    for col, ancho in zip("ABCDEFGHIJ", (8, 14, 28, 16, 9, 14, 36, 9, 14, 11)):
        ws.column_dimensions[col].width = ancho
    wb.save(AQUI / "facturas-plantilla.xlsx")


def reporte_dgii():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte"
    ws.append(["Encf", "Moneda", "MontoTotal", "TotalItbis", "TotalMontoItbisRetenido", "TotalMontoRetencionRenta",
               "FechaRecepcion", "Estado", "RncReceptor", "RncEmisor", "AprobacionComercial", "FechaAprobacionComercial"])
    def recibido(d, h):
        return (datetime.combine(HOY - timedelta(days=d), datetime.min.time()) + timedelta(hours=h)).strftime("%d/%m/%Y %I:%M:%S %p")
    filas = [
        ["E310000004512", "", 2124.00, 324.00, 0, 0, recibido(9, 10), "Aceptado", EMPRESA_RNC, "130555151", "", ""],
        ["E310000004530", "", 1416.00, 216.00, 0, 0, recibido(5, 15), "Aceptado", EMPRESA_RNC, "130555151", "", ""],
        ["E310000000981", "", 8260.00, 1260.00, 0, 0, recibido(3, 11), "Aceptado", EMPRESA_RNC, "130555168", "", ""],
    ]
    for f in filas:
        ws.append(f)
    for col in "ABCDEFGHIJKL":
        ws.column_dimensions[col].width = 18
    wb.save(AQUI / "reporte-dgii-ecf-recibidos.xlsx")


if __name__ == "__main__":
    plantilla()
    reporte_dgii()
    print("archivos generados en", AQUI)
