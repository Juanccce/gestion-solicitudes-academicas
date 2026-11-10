# Gestión de Solicitudes Académicas

Prototipo de consola para el TPI de Metodología de Sistemas II. Registra solicitudes, asigna responsables, cambia estados, filtra y emite un resumen. Usa datos sintéticos en JSON local.

## Requisitos y uso
Python 3.10+, sin dependencias externas.

    python -m src.solicitudes.cli add --estudiante Ana --tipo Inscripcion --prioridad alta --descripcion Correlativa
    python -m src.solicitudes.cli list
    python -m src.solicitudes.cli assign 1 --responsable Mesa
    python -m src.solicitudes.cli transition 1 --estado en_revision
    python -m src.solicitudes.cli report
    python -m unittest discover -s tests -v

La primera ejecución crea data/solicitudes.json. No usar datos personales reales.

La versión deliberadamente problemática está en baseline/legacy_app.py; la mejorada, en src/solicitudes/. El informe completo está en docs/informe.md.

## Historial y tags

El repositorio trae commits por etapa y los tags estado-inicial, estado-refactorizado, etapa-diagnostico, etapa-refactoring, etapa-pruebas y etapa-docs. Para publicarlo en un repositorio remoto propio:

    git remote add origin URL_DEL_REPOSITORIO
    git push -u origin main
    git push origin --tags
