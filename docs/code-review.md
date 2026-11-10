# Revisión técnica

- Separación entre CLI, servicio, modelo y persistencia.
- Validación de campos y valores permitidos.
- Errores explícitos para ID inexistente y JSON inválido.
- Ruta inyectada en el repositorio; no hay ruta global en el servicio.
- Nombres orientados a la intención y operaciones acotadas.
- Persistencia UTF-8 legible.
- Ocho pruebas unitarias con almacenamiento temporal.

Pendiente para producción: base de datos transaccional, concurrencia, autenticación, roles, auditoría, backup y flujo institucional de aprobaciones.
