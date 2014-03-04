Django Backend Manager
======================

Backend para aplicaciones web para la nube con Django con la elegancia de Bootstrap de Twitter.

Con el DjangoBackend podrás gestionar de manera RÁPIDA y SEGURA a los usuarios, perfiles y permisos de usuario, recursos del sistema, módulos y planes del sistema, menús dinámicos, empresas, y mucho más...!

Ahora, cuando inicias un proyecto comenzarás directamente a atender(implementar) los requisitos de tu nuevo sistema. Ya que este módulo (Backend) se encargó de todo el trabajo inicial repetitivo de todo proyecto de software así como de los componentes o librerías que necesitas antes de comenzar a desarrollar cualquier software.

DjangoBackend es el entregable más importante de todo UN MARCO DE TRABAJO para desarrollar app WEB SEGURAS sobre django. Este marco, además, incluye la documentación del diseño del sistema, librerías se seguridad y helpers bien documentadas, métodos y técnicas de codeo, manual del desarrollador o programador, manual del usuario, ejemplos de integración, etc. 

Documentación
-------------------

`Diseño del sistema <http://djangobackend-model.appspot.com>`_


Demo
-------------------

`Demo en línea <http://dbackend.python.org.pe>`_

Usuario: admin

Pass: 12345


Manual del programador
-------------------

`Descargar en PDF <https://github.com/submitconsulting/django_backend_project/blob/master/manuales/Manual%20del%20Programador.pdf?raw=true>`_


Instalación
-------------------
Para instalar el DjangoBackend simplemente lo descargas y usas inicialmente la base de datos del archivo sdbm.db ubicado en la carpeta "/django_backend_project/django_backend/", para mayor seguridad editas el settings.py con los parámetros de conexión y vuelves a hacer `syncdb`.

Usuario: admin

Pass: 12345


Requirements:

Python 2.7.6

Django==1.6.2

PIL==1.1.7


To install Django, run the following command::

    ```
    >>> pip install django==1.6.2
    ```

Recursos del sistema
-------------------
Los recursos son las acciones o métodos que se pueden ejecutar en los controladores,  Esta data se almacena en `django.contrib.auth.models.Permission` y luego se convierte en un recurso por el decorador `@permission_resource_required`


Perfiles de usuario
-------------------
La gestión de perfiles permite administrar los direfentes roles de los usuarios que acceden al sistema. Esta data se almacena en `django.contrib.auth.models.Group`



Permisos de usuarios
-------------------
Los premisos o privilegios son los recursos que puede acceder cada perfil creado, brindando una mayor seguridad y escalabilidad al sistema. Esta data se almacena usando `django.contrib.auth.models.Group.permissions.add(django.contrib.auth.models.Permission)`


Módulos del sistema
-------------------
Los módulos asocian un conjunto de perfiles con la finalidad de ser asignado en un plan del sistema. Esta data se almacena en `apps.sad.models.Module`

Planes del sistema
-------------------
Los Planes asocian un conjunto de módulos con la finalidad de personalizar los servicios que se ofrecen a los clientes. Esta data se almacena  usando `apps.sad.models.Module.solutions.add(apps.space.models.Solution)`


Menús del sistema
-------------------
La administración de menús permite gestionar los diferentes menús para que los usuarios accedan a los recursos. Estos menún están organizados por Módulos del sistema previamente definidos. Por ahora cada menú puede tener un submenú

Asociación
-------------------
Permite la administración de los datos básicos de la asociación

Empresas
-------------------
Permite gestionar las empresas cuyas sedes están vinculadas de la asociación

Empresa
-------------------
Permite la administración de los datos básicos de la empresa

Sedes
-------------------
Permite gestionar las sucursales de la empresa y asignarla a uno o más usuarios

Auditorías
-------------------
Las acciones que realizan los usuarios en el sistema se registran para tener un control sobre los eventos generados. Se genera un archivo para cada día


Accesos (TODO)
-------------------
Permite la visualización de las entradas y salidas de los usuarios del sistema

Backups (TODO)
-------------------
Permite crear copias de seguridad y restaurar el sistema en un punto específico



Visor de sucesos (TODO)
-------------------
Si está activo, permite la visualización de los logs de las consultas generadas en la base de datos, para tener un control sobre la base de datos

Mantenimiento (TODO)
-------------------
Permite optimizar, vaciar el cache, desfragmentar y reparar (si es posible) las tablas de la base de datos

Archivos de configuración (TODO)
-------------------
Permite editar los diferentes archivos de configuración del sistema ubicados en la carpeta "config" de la aplicación



