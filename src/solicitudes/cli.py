import argparse
from pathlib import Path
from .repository import RepositorioJson
from .service import ServicioSolicitudes
def main():
    parser=argparse.ArgumentParser(description="Gestión de solicitudes académicas")
    sub=parser.add_subparsers(dest="cmd",required=True)
    add=sub.add_parser("add"); add.add_argument("--estudiante",required=True); add.add_argument("--tipo",required=True); add.add_argument("--prioridad",choices=["baja","media","alta"],default="media"); add.add_argument("--descripcion",required=True)
    ls=sub.add_parser("list"); ls.add_argument("--estado"); ls.add_argument("--tipo")
    ass=sub.add_parser("assign"); ass.add_argument("id",type=int); ass.add_argument("--responsable",required=True)
    tr=sub.add_parser("transition"); tr.add_argument("id",type=int); tr.add_argument("--estado",required=True)
    sub.add_parser("report"); args=parser.parse_args()
    ruta=Path(__file__).resolve().parents[2]/"data"/"solicitudes.json"
    svc=ServicioSolicitudes(RepositorioJson(ruta))
    try:
        if args.cmd=="add": result=svc.registrar(args.estudiante,args.tipo,args.prioridad,args.descripcion)
        elif args.cmd=="list": result=svc.buscar(args.estado,args.tipo)
        elif args.cmd=="assign": result=svc.asignar(args.id,args.responsable)
        elif args.cmd=="transition": result=svc.cambiar_estado(args.id,args.estado)
        else: result=svc.resumen()
        print(result)
    except (ValueError,LookupError) as exc: raise SystemExit(str(exc)) from exc
if __name__=="__main__": main()
