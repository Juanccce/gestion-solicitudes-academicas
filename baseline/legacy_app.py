import json
DATA = "data/solicitudes.json"
class Sistema:
    def __init__(self):
        try:
            self.solicitudes = json.load(open(DATA, encoding="utf-8"))
        except Exception:
            self.solicitudes = []
    def hacer_todo(self, accion, estudiante="", tipo="", prioridad="media", descripcion="", ident=0, responsable="", estado=""):
        if accion == "alta":
            nuevo = {"id": len(self.solicitudes)+1, "estudiante": estudiante, "tipo": tipo, "prioridad": prioridad, "descripcion": descripcion, "responsable": "", "estado": "pendiente"}
            self.solicitudes.append(nuevo)
            with open(DATA,"w",encoding="utf-8") as f: json.dump(self.solicitudes,f)
            return nuevo
        if accion in ("asignar", "estado"):
            for s in self.solicitudes:
                if s["id"] == ident:
                    s["responsable" if accion == "asignar" else "estado"] = responsable if accion == "asignar" else estado
                    with open(DATA,"w",encoding="utf-8") as f: json.dump(self.solicitudes,f)
                    return s
        if accion == "buscar":
            return [s for s in self.solicitudes if (not estado or s["estado"] == estado) and (not tipo or s["tipo"] == tipo)]
        if accion == "reporte":
            p=r=c=0
            for s in self.solicitudes:
                if s["estado"] == "pendiente": p+=1
                if s["estado"] == "en_revision": r+=1
                if s["estado"] == "resuelta": c+=1
            return {"total":len(self.solicitudes),"pendiente":p,"en_revision":r,"resuelta":c}
        return None
