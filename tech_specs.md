
Decisiones de Diseño

La aplicación de inventario fue desarrollada utilizando Python, Django y Django ORM.
API RESTful: La aplicación sigue una arquitectura RESTful, intercambiando todos los datos mediante payloads JSON.
Base de Datos: PostgreSQL se utiliza como sistema de gestión de bases de datos relacional.
Cola de Tareas: Celery se utiliza para la gestión de tareas en segundo plano, con Redis como el broker para manejar tareas asíncronas.
La aplicación está dividida en tres aplicaciones separadas:
Users: Gestiona la funcionalidad relacionada con usuarios, incluyendo registro, autenticación y permisos.
Products: Maneja los datos de productos, creación, actualización y filtrado.
Alerts: Gestiona la lógica de alertas basada en las fechas de expiración de los productos y los disparadores definidos por el usuario.

Decisiones de Optimizacion

En lugar de almacenar el estado (activo o expirado) directamente en el modelo de alerta, este se calcula dinámicamente cada vez que se necesita. De esta manera se elimina la necesidad de tareas periódicas en segundo plano para actualizar el estado y evita posibles inconsistencias causadas por actualizaciones manuales de registros de alertas.
La fecha de ejecución de la alerta no se almacena explícitamente en el modelo. En su lugar, se calcula en función del campo days_before_expiration_to_trigger de la alerta y la expiration_date del producto. De esta manera se evita actualizar las fechas de alerta manualmente cuando se modifica una alerta.
Para todas las funciones se especifican los tipos de los parámetros y los resultados.
Varios métodos se incluyen directamente en los models y serializers. El resto en services y Selectorspara evitar importaciones circulares y mejorar la organización del código. 
Cuando es posible se utiliza select_related y prefetch_related para optimizar las consultas a la base de datos y la performance de la aplicacion.
Se agrego paginacion y posibilidad de filtrados para los endpoints que lo requieren.
