# Defensa del TPI: preparación y guion hablado

**Duración objetivo: 13 minutos.** La consigna permite entre 10 y 15. No apures la lectura: antes de cada comando explicá qué esperás que haga, ejecutalo, leé el resultado y contá qué significa. Es normal hacer pausas cortas para cambiar de archivo; evitá silencios largos. Todos los integrantes deben aparecer y hablar con voz propia.

## Preparación desde cero

1. Abrí la aplicación que van a usar para grabar. Si presentan en grupo remoto, inicien la videollamada y activen las cámaras. Una persona comparte la pantalla y graba.
2. Abrí PowerShell desde Inicio. Escribí y ejecutá:

    cd "$env:USERPROFILE\Downloads\TPI"
    Get-Location
    Test-Path .\docs\code-review.md

La ruta debe terminar en Downloads\TPI y Test-Path debe devolver True. Para mostrar el checklist sin abrir Notepad, ejecutá Get-Content .\docs\code-review.md. Esto evita que Notepad abra vacío si la consola estaba en otra carpeta.

3. Verificá que existan baseline\legacy_app.py, src\solicitudes y tests. Cerrá ventanas y notificaciones que no quieras compartir.
4. La solicitud de Ana con ID 1 ya está cargada en tu carpeta TPI. Para la demo se agrega una segunda solicitud, que recibe ID 2. Los tests usan almacenamiento temporal y no modifican estos registros.
5. Hagan una prueba corta de audio y grabación. Comprueben que se ven las caras del grupo y que se puede leer el texto compartido.

## Reparto sugerido

- Integrante 1: presentación, alcance y cierre.
- Integrante 2: versión inicial y diagnóstico.
- Integrante 3: diseño refactorizado y demo.
- Integrante 4: tests, Git, revisión y límites.

Con menos integrantes, repartan los bloques. Si presentan individualmente, hablá como “yo” y hacé todos los bloques.

## Guion detallado de 13 minutos

### 0:00-1:15 | Presentación

**Mostrar:** la pantalla compartida con PowerShell y la carpeta TPI. Mirá a cámara al empezar; no leas la pantalla.

**Decir:** “Hola, soy [nombre] / somos [nombres]. Este es el Trabajo Práctico Integrador de Metodología de Sistemas II. Tomamos un prototipo de gestión de solicitudes académicas y lo revisamos para mejorar la organización y el mantenimiento del código. No buscamos sumar funciones porque sí: queríamos entender qué problemas había, cambiar la estructura y comprobar que las operaciones siguieran funcionando.”

“Los nombres que aparecen en la demostración son ficticios. Es un prototipo académico con un archivo local; no es un sistema de la UTN ni sirve para tramitar solicitudes reales.”

### 1:15-2:45 | Qué hace el sistema

**Mostrar:** en PowerShell, ejecutar:

    Get-Content .\README.md

**Decir mientras aparece el texto:** “Una solicitud guarda un ID, estudiante, tipo, prioridad, descripción, responsable y estado. El programa tiene cinco operaciones visibles: dar de alta, listar o filtrar, asignar responsable, cambiar el estado y emitir un resumen.”

“Los estados del ejemplo son pendiente, en revisión y resuelta. Elegimos JSON para mantener pequeño el prototipo y no agregar dependencias externas. Esa decisión sirve para la práctica, pero tiene límites si hay varias personas escribiendo a la vez.”

### 2:45-4:45 | Versión inicial y diagnóstico

**Mostrar:** ejecutar en PowerShell:

    Get-Content .\baseline\legacy_app.py

Si se llena la pantalla, abrí baseline\legacy_app.py con un editor de texto y buscá hacer_todo con Ctrl+F.

**Decir:** “Esta es la versión inicial. La clase Sistema se encargaba de varias operaciones, y hacer_todo decidía qué hacer según una cadena. Si quería cambiar una regla o el modo de guardar, tenía que revisar varios caminos.”

“También encontramos escrituras del JSON repetidas y valores de estado escritos directamente. Otro problema importante está en la lectura inicial: se captura una excepción demasiado amplia y se ignora. Si el JSON estuviera dañado, el programa podría tratarlo como si no hubiera solicitudes. El informe registra diez problemas, su posible impacto y una prioridad para este prototipo.”

“Este diagnóstico fue manual: leímos el código y recorrimos los casos de uso. No afirmamos que una herramienta automática haya encontrado estos resultados.”

### 4:45-7:45 | Diseño refactorizado y demo

**Mostrar:** primero la estructura de src\solicitudes. Luego ejecutá:

    Get-Content .\src\solicitudes\service.py
    Get-Content .\src\solicitudes\repository.py

**Decir:** “En la versión mejorada separamos las tareas. El modelo representa la solicitud; el servicio valida y aplica las reglas; el repositorio lee y guarda JSON; y cli.py conecta los comandos de consola con el servicio. Así podemos probar reglas sin depender de la pantalla ni de un archivo real.”

“Voy a cargar otra solicitud ficticia. Antes de ejecutarlo, los argumentos identifican estudiante, tipo, prioridad y descripción.”

Ejecutar:

    python -m src.solicitudes.cli add --estudiante Luis --tipo Examen --prioridad media --descripcion "Consulta de fecha"

**Decir después de leer la salida:** “El sistema creó la solicitud con ID 2 y estado pendiente. La solicitud de Ana que ya estaba en los datos conserva el ID 1.”

Antes de cada comando siguiente, explicar qué cambia:

    python -m src.solicitudes.cli list

“List muestra las solicitudes guardadas. Así puedo comprobar que el alta persistió y que ahora hay dos registros.”

    python -m src.solicitudes.cli assign 2 --responsable Mesa

“Assign modifica la persona responsable de la solicitud 2. No cambia el estudiante ni la descripción.”

    python -m src.solicitudes.cli transition 2 --estado en_revision

“Transition actualiza el estado. El servicio primero comprueba que en_revision sea uno de los estados permitidos.”

    python -m src.solicitudes.cli report

“Report cuenta cuántas solicitudes hay por estado. El total ahora es dos, porque usamos registros de ejemplo.”

### 7:45-9:45 | Tests

**Decir antes de escribir:** “Ahora voy a ejecutar las ocho pruebas. Cubren alta y persistencia, asignación, transición, filtros, resumen y entradas inválidas. Corren en almacenamiento temporal para no modificar las solicitudes de la demo.”

Ejecutar:

    python -m unittest discover -s tests -v

Mientras corre, esperá un segundo; cuando aparezcan los resultados, decí: “Cada línea con ok indica que ese caso pasó. Al final vemos Ran 8 tests y OK. Eso nos da una comprobación repetible de estos comportamientos; no significa que el prototipo esté probado para todos los usos posibles.”

### 9:45-11:00 | Historial y tags

**Decir antes de ejecutar:** “También dejamos trazabilidad para distinguir el punto de partida de cada etapa del trabajo.”

Ejecutar:

    git log --oneline --decorate --all -10
    git tag --list

“En el historial se ven commits para el estado inicial, diagnóstico, refactoring, pruebas y documentación. Los tags estado-inicial y estado-refactorizado marcan los extremos; los tags etapa-diagnostico, etapa-refactoring, etapa-pruebas y etapa-docs ubican los hitos.”

### 11:00-12:15 | Code review y límites

**Decir:** “El checklist revisa separación de responsabilidades, validaciones, errores, persistencia y testabilidad. No agregamos autenticación ni permisos porque el alcance es una demo de consola.”

Mostrar el checklist directamente en PowerShell:

    Get-Content .\docs\code-review.md

“Para una versión institucional habría que definir roles, auditoría de cambios y copias de seguridad; también pasar a una base de datos transaccional si hubiera concurrencia. Son límites de esta solución, no funciones ya implementadas.”

### 12:15-13:00 | Cierre

**Decir:** “La mejora principal fue separar responsabilidades, hacer visibles los errores y sumar pruebas para los flujos importantes. El ejemplo queda más fácil de revisar y modificar, aunque sigue siendo un prototipo. Usamos ChatGPT como apoyo para ordenar el informe y revisar la redacción; el equipo revisó las decisiones y debe poder explicarlas. Gracias.”

## Consejos para no quedarse en silencio mientras escribís

- Antes de cada comando, contá qué dato va a leer o modificar.
- Después de ejecutarlo, leé solo la parte importante de la salida y explicá qué confirma.
- No describas cada tecla ni leas líneas irrelevantes. Una explicación breve por comando es suficiente.
- Si un comando tarda, esperá en silencio un instante; no rellenes con frases repetidas.
- Si aparece un error, no tapes el resultado ni inventes otro: frená, explicá qué pasó y corregilo antes de seguir.

## Revisión final

El video debe durar entre 10 y 15 minutos; todos deben aparecer y hablar con voz propia. Comprueben que se vean las cámaras, que el código sea legible y que el audio esté claro. Reproduzcan el archivo completo antes de entregarlo.
