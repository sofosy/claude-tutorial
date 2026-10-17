"""CRM (prospectos y oportunidades) y mesa de ayuda de Caribe Fresco. Nombres ficticios."""
import json
from api import api, sql
M = "maria.santana@caribefresco.demo"; YO = 245
LEADS = [  # nombre, apellido, empresa, valor, fuente, prioridad, etapa
 ("Gabriel", "Cepeda", "Hotel Arenas Blancas SRL", 680000, "referral", "high", 89), ("Lorena", "Valdez", "Restaurante La Terraza Marina", 240000, "website", "medium", 89),
 ("Ernesto", "Lantigua", "Supermercado El Ahorro del Sur", 520000, "trade_show", "high", 88), ("Patricia", "Hernández", "Catering Gourmet Santiago", 185000, "social_media", "medium", 88),
 ("Julio", "Brito", "Cadena de Colmados Unidos", 410000, "partner", "high", 88), ("Mariela", "Ovalle", "Cafetería Universitaria Central", 96000, "phone_call", "low", 87),
 ("Andrés", "Pujols", "Resort Punta Caleta SRL", 750000, "referral", "urgent", 87), ("Glenys", "Almonte", "Comedor Industrial Zona Franca", 330000, "email_campaign", "medium", 87),
 ("Rodolfo", "Ceballos", "Frutería Don Rodo", 64000, "website", "low", 87), ("Karina", "Sosa", "Hotel Colonial Plaza", 290000, "advertising", "medium", 86),
 ("Félix", "Morel", "Restaurante Fogón Cibaeño", 120000, "referral", "medium", 86), ("Yesica", "Rojas", "Escuela Hotelera del Caribe", 150000, "trade_show", "high", 86),
 ("Domingo", "Paulino", "Minimarket Las Américas", 58000, "phone_call", "low", 86), ("Nathalie", "Guerrero", "Pastelería Dulce Tentación", 72000, "social_media", "medium", 86)]
def crm():
    if sql("SELECT COUNT(*) FROM leads WHERE company_id=15")[0][0] != "0": print("CRM ya sembrado"); return
    for i, (n, a, emp, val, src, pri, st) in enumerate(LEADS):
        api(M, "POST", "/v1/leads", {"firstName": n, "lastName": a, "companyName": emp, "phone": f"809555{1300+i:04d}", "email": f"{n.lower()}.{a.lower()}@ejemplo.com",
            "source": src, "priority": pri, "estimatedValue": val, "stageId": st, "workspace": 15, "assignedUser": YO,
            "expectedCloseDate": f"2026-{11 if st < 88 else 10}-{10 + i:02d}"})
    clientes = {nm: int(i) for i, nm in sql("SELECT id, name FROM partners WHERE company_id=15 AND partnerType='CUSTOMER' AND deleted_at IS NULL")}
    OPS = [("Supermercado La Estrella del Norte SRL", "Contrato anual de vegetales frescos", 1450000, "negotiation", 75),
           ("Hotel Brisas del Caribe SRL", "Suministro semanal de frutas para buffet", 980000, "proposal", 60),
           ("Catering Eventos del Valle SRL", "Temporada de bodas noviembre–diciembre", 420000, "qualification", 35),
           ("Supermercado Plaza Central SRL", "Nueva sucursal: abastecimiento inicial", 760000, "proposal", 55),
           ("Restaurante Mar y Tierra SRL", "Ampliación de pedido mensual", 210000, "needs_analysis", 40)]
    for cli, nom, monto, etapa, prob in OPS:
        if cli in clientes:
            api(M, "POST", "/v1/opportunities", {"name": nom, "partner": clientes[cli], "amount": monto, "stage": etapa, "probability": prob,
                "priority": "high" if monto > 700000 else "medium", "type": "new_business", "expectedCloseDate": "2026-11-15", "assignedUser": YO, "workspace": 15})
    print("CRM listo")
TICKETS = [("Pedido llegó incompleto: faltaron 3 sacos de papa", "ORDER_ISSUE", "HIGH", "PHONE", "Supermercado La Estrella del Norte SRL", "IN_PROGRESS"),
 ("Solicitan duplicado de la factura de septiembre", "BILLING_INQUIRY", "NORMAL", "EMAIL", "Hotel Brisas del Caribe SRL", "RESOLVED"),
 ("Caja de mango llegó demasiado madura", "COMPLAINT", "HIGH", "WEB_FORM", "Restaurante Sabor Criollo SRL", "OPEN"),
 ("Cambio de horario de entrega a las 6:00 a. m.", "ORDER_ISSUE", "NORMAL", "CHAT", "Hotel Costa Esmeralda SRL", "RESOLVED"),
 ("Consulta por precio de fresas para temporada", "PRODUCT_INQUIRY", "LOW", "EMAIL", "Heladería Coco Loco SRL", "OPEN"),
 ("Factura salió con el RNC equivocado", "BILLING_INQUIRY", "URGENT", "PHONE", "Comedor Doña Mercedes SRL", "IN_PROGRESS"),
 ("Solicitud de crédito a 45 días", "ACCOUNT_ISSUE", "NORMAL", "IN_PERSON", "Supermercado Mi Familia SRL", "OPEN"),
 ("Devolución de 2 cajas de lechuga", "REFUND_REQUEST", "NORMAL", "PHONE", "Restaurante Mar y Tierra SRL", "RESOLVED")]
def mesa():
    try:
        if sql("SELECT COUNT(*) FROM helpdesk_tickets WHERE company_id=15")[0][0] != "0": print("mesa ya sembrada"); return
    except Exception: pass
    clientes = {nm: int(i) for i, nm in sql("SELECT id, name FROM partners WHERE company_id=15 AND partnerType='CUSTOMER' AND deleted_at IS NULL")}
    for asunto, tipo, pri, src, cli, estado in TICKETS:
        r = api(M, "POST", "/v1/helpdesk/tickets", {"subject": asunto, "description": f"<p>{asunto}.</p>", "type": tipo, "priority": pri, "source": src,
            "customerId": clientes.get(cli), "assignedToUser": YO})
        tid = r.get("id") or (r.get("ticket") or {}).get("id")
        if estado != "OPEN" and tid:
            if estado == "RESOLVED": api(M, "PATCH", f"/v1/helpdesk/tickets/{tid}/status", {"status": "IN_PROGRESS"}, permitir=(400,))
            api(M, "PATCH", f"/v1/helpdesk/tickets/{tid}/status", {"status": estado, **({"resolution": "Atendido y confirmado con el cliente."} if estado == "RESOLVED" else {})}, permitir=(400,))
    print("mesa lista")
if __name__ == "__main__":
    crm(); mesa()
