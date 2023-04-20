# flask-login-app

Miguel Perez, 15-11126
Gabriel Chaurio, 17-10126

Flask Login App

# Activar el venv con 'source ./bin/activate'

# luego 'cd ./login-app'

# Ejecutar la app con 'flask --app login --debug run'

# Si hay problemas de BDD, 'flask --app login init-db'

El punto de partida asumido por el equipo MPGC para el presente proyecto fue desde los
objetivos específicos propuestos para la aplicación y las propuestas de historias de usuario
solicitadas por el Agile Coach, para la asignatura Ingeniería de Software I en el periodo
ENE-MAR 2023.

El producto de software resultante y demás artefactos entregables derivados del proyecto
para los períodos antes mencionado realizado por el equipo MPGC bajo la supervisión del
profesor Jean Carlos Guzmán (jguzman106@gmail.com) , se rigen bajo la Licencia de Software Libre GNU (General
Public License) y se autoriza que el material pueda ser utilizado con fines académicos y
docentes de la Universidad Simón Bolívar, contemplando la posibilidad de su futura
utilización en el abordaje de proyectos de Gestion de Empresas en la USB.

El metodo de programacion utilizado es el metodo agil eXtreme programming. 
El proyecto fue completado en un total de 4 iteraciones.


# Iteracion 1:
 Como Sistema, puedo Identificar a Usuarios para Controlar el Acceso No Autorizado al Sistema(Épica).
  a. Como Sistema, puedo Autenticar Usuarios para Controlar el Acceso No Autorizado al Sistema(INVEST).
  b. Como Administrador,puedo Crearperfiles de Usuarios para Controlar de Acceso No Autorizado al Sistema(INVEST).
  c. Como Administrador,puedoIngresarRolesalosUsuariosparaControlarelAccesoNoAutorizadoalSistema(INVEST).
  Nota: -Autenticar Usuarios implica un algoritmo de encriptación.
        -Crear Perfiles implica Agregar, Buscar, Modificar, Pausar, Eliminar y Descargar datos de un proyecto en particular.
          -Los roles son Gerente de Operaciones, Supervisor del área de Mecánica General, Supervisor del área de Latonería y Pintura, Especialistas en Mecánica,        Especialistas en   Electrónica , Especialistas en Electricidad, etc.
 
# Iteracion 2:
  Como Analista de Operaciones, puedo Ingresar los datos de identificación del Vehículo que ingresa al taller para Registrar a los Vehículos de los Clientes del taller en el Sistema (Épica).
    a. Como Analista de Operaciones,puedo Ingresar los datos personales de diferentes clientes del taller para Registrar a los Vehículos de los Clientes del taller en el Sistema(INVEST).
     b. Como Analista de Operaciones, puedo Ingresar los datos de un vehículo automotor de un cliente del taller en particular para Registrar a los Vehículos de los Clientes del taller en el Sistema(INVEST).
        
Nota: -Ingresar los datos personales implica Agregar, Buscar, Modificar y Eliminar clientes.
      -Los datos personales implican Cédula, Nombres, Apellidos, Teléfono de Contacto, Dirección.
      -Ingresar los datos de un Vehículo Automotor implica Agregar, Buscar, Modificar y Eliminar vehículos.
      -Los datos de un Vehículo Automotor implican

# Iteracion 3:
  Como Usuario, puedo Generar diferentes proyectos automotrices en el Sistemapara Gestionar el Portafolio de Proyectos de un Taller Automotriz en Particular (Épica).
    a. Como Gerente, puedo Ingresar los parámetros de un Proyecto en el Sistemapara Gestionar el Portafolio de Proyectos de un Taller Automotriz en Particular (INVEST).
    b. Como Administrador, puedo Ingresar la descripción de los diferentes departamentos del taller para Configurar la estructura organizacional-operativa del taller en el Sistema(INVEST).
    c. Como Gerente de Proyectos, puedo Ingresar los datos de un proyecto automotriz de un cliente en particular para Gestionar Proyectos automotrices del taller en el Sistema(INVEST).
    
    
    Nota:
        - Ingresar la descripción de los diferentes departamentos del taller implica Agregar, Buscar, Modificar y Eliminar un departamento en particular.
        - Ingresar los datos de un proyecto Mecánico Automotriz implica Agregar, Buscar, Modificar y Eliminar proyectos concretos.
        - Los datos de un proyecto automotriz implican ID, Fecha, Vehículo (Placa, Marca, Cédula, Propietario), Departamento, Gerente de Proyectos (Cédula, Nombre, Apellidos), Problema, Solución, Monto, Observaciones.
        
        
# Iteracion 4:
  Como Gerente de Proyecto, puedo Desarrollar los Planes de Acción de un proyecto automotriz especifico en el Sistema para Gestionar el Portafolio de Proyectos de un Taller Automotriz en Particular (Épica).
    a. Como Gerente de Proyecto, puedo Definir Acciones, Actividades, Tiempo y Costos asociados a un proyecto automotriz especifico en el Sistema para Generar los Planes de Acción de un proyecto automotriz en Particular (INVEST).
    b. Como Gerente de Proyecto, puedo Especificar los Costo Detallados correspondientes al Talento Humano vinculado a un proyecto automotriz especifico en el Sistemapara Generar los Planes de Acción de un proyecto automotriz en Particular (INVEST).
    c. Como Gerente de Proyecto, puedo Establecer los Costo Detallados concernientes a los Materiales e Insumos derivados de un proyecto automotriz especifico en el Sistemapara Generar los Planes de Acción de un proyecto automotriz en Particular (INVEST).
    
 Nota:
  - Desarrollar los Planes de Acción de un proyecto automotriz especifico en el Sistema implica Agregar, Buscar, Modificar y Eliminar un Plan de Acción asociado a un proyecto automotriz en particular.
  -Los datos de los Planes de Acción implican ID, Acción, Actividad, Fecha Inicio, Fecha Cierre, Cantidad Horas, Responsable, Monto ($).
  -Especificar los Costo Detallados correspondientes al Talento Humanoimplica Agregar, Buscar, Modificar y Eliminar proyectos concretos.
  -Los datos de los Costo Detallados correspondientes al Talento Humanoimplican ID, Acción, Actividad, Tiempo, Cantidad, Costo ($), Responsable, Monto ($).
  -Establecer los Costo Detallados concernientes a los Materiales e Insumos implican Agregar, Buscar, Modificar y Eliminar costo detallados asociados a Materiales e Insumos
  -Los datos de los Costo Detallados correspondientes a los Materiales e Insumos implican ID, Acción, Actividad, Categoría, Descripción, Cantidad, Medida, Costo ($), Responsable, Monto ($)

  
