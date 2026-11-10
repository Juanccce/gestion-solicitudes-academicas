# Registro del diagnóstico

Se revisó baseline/legacy_app.py a partir de sus flujos de alta, asignación, cambio de estado, búsqueda y reporte. El diagnóstico es manual; no se atribuyen resultados a analizadores estáticos.

| Hallazgo | Evidencia en la versión inicial | Efecto probable | Prioridad |
|---|---|---|---|
| Responsabilidades mezcladas | Sistema.hacer_todo cubre cinco operaciones y persistencia | Un cambio afecta otros flujos | Alta |
| Rutina extensa | Una acción selecciona múltiples caminos dentro de un método | Cuesta aislar errores | Alta |
| Tipos primitivos | Acción, estado y prioridad como cadenas sin validación central | Admite valores inconsistentes | Alta |
| Valores mágicos | Cadenas de estado repetidas en reporte y actualizaciones | Cambios incompletos | Media |
| Persistencia duplicada | Bloques de escritura JSON en alta y edición | Correcciones repetidas | Alta |
| Excepción ignorada | except Exception oculta JSON inválido y errores de lectura | Diagnóstico erróneo de archivo vacío | Alta |
| Ruta global | DATA fija la ubicación de almacenamiento | Dificulta pruebas aisladas | Media |
| Dominio acoplado a JSON | El caso de uso conoce diccionarios y escritura | Reemplazo de persistencia costoso | Alta |
| ID basado en longitud | len(solicitudes) + 1 puede colisionar con huecos | Identificadores duplicados | Media |
| Conteo manual | Reporte mantiene un contador por cada estado | Nuevos estados no aparecen | Media |

Los riesgos son estimaciones cualitativas adecuadas al prototipo; no equivalen a una medición de impacto en producción.
