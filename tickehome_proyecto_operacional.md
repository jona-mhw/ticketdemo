REDSALUD




[Nombre requerimiento]
Página 1
Proyecto Ticket Home Redsalud 2025
Versión 1





Proyecto Ticket Home Redsalud 2025






Catalina Ramirez / Carlos Díaz / Jonathan Segura 


Mayo 2025
Contenido
Ficha de Proyecto
Descripción de la Necesidad de Negocio y Requisitos Funcionales
Requerimientos (Obligatorio)
Interfaz Usuaria / Capturas de pantalla
Plan de pruebas (Obligatorio)


1. Ficha de Proyecto
Nombre
Proyecto Ticket Home Redsalud 2025
Justificación
Ticket home tiene por objetivo - Disminuir tiempos de estadía en cirugías de alto impacto en hospitalizaciones. - Generar sinergia entre equipos médicos y operacionales para uso eficiente de recursos. - Uso continuo de camas. - Optimizar la comunicación y predictibilidad del alta. 
Contar con una plataforma transversal permite contar con información unificada y homologar datos y procesos
Alcance
Implementar un sistema periférico standalone para optimizar uso y gestión de camas durante el viaje del paciente hospitalario basándose en reglas y datos maestros de cirugías, técnicas y estadías estándar. Anticipar, registrar, modificar y comunicar la fecha/hora probable de alta desde etapas tempranas (creación de orden quirúrgica/ticket). Gestionar el ciclo de vida del "Ticket Home" (creación, modificación, visualización, anulación, cierre). 

Generar datos para toma de decisiones. Aplica a todas las clínicas de la red
Business Sponsor
Gerencia Operaciones Casa Matriz Redsalud
Costo en HH (Estimación de IT)
Pendiente de definir/estimar
Business Leader
A definir (Podría ser Catalina Jesus Ramirez Lopez o un representante de la Gerencia de Operaciones)
IT Leader
Jonathan Segura
Involucrados
Catalina Jesus Ramirez Lopez, Jonathan Segura, Equipos médicos (cirujanos, tratantes), Equipos de Enfermería, Equipos operacionales y administrativos (gestión de camas), Pacientes, Familiares, Pao Riquelme,
Sistemas a Intervenir
Sin sistemas a intervenir. Es una plataforma independiente
IMPACTO
Beneficio Económico ($MM/ 5 años)
Beneficio inicial enfocado en una clínica, con potencial transversal en 9 clínicas. Ver detalle en: https://docs.google.com/spreadsheets/d/1bCNYP0BEdiQOs5ni_8-dqNNEa4j15y8o8OrkNAjYQ5c/edit?usp=sharing
Impacto no Económico
Mayor disponibilidad de camas y quirófanos; aumento de oferta para cirugías Ticket Home; mejora en visibilidad de camas disponibles (filial y casa matriz); mejora en la experiencia del paciente y familia al tener predictibilidad del alta; optimización de flujos de trabajo para equipos clínicos y administrativos.
Clasificación Impacto no Económico (Alto-Medio-Bajo)
Alto (Sugerido)
Ocurrencia Impacto no Económico (Alta-Mediana-Baja)
Alta (Sugerido, si el proyecto es exitoso)
Riesgo Implementación Exitosa (Alto-Medio-Bajo)
Medio (Por habilitación de nueva plataforma, aspectos técnicos, correcta parametrización y mantenimiento de las reglas de negocio para el cálculo de FPA y adhesión)



2. Descripción de la Necesidad de Negocio y Requisitos Funcionales

Descripción de la Necesidad de Negocio:

Estandarizar y optimizar la gestión de la Fecha Probable de Alta (FPA) del paciente quirúrgico para mejorar el flujo de camas, reducir estadías innecesarias, mejorar la comunicación con el paciente y equipos, y contar con información oportuna para la gestión operativa. Reemplazar la actual operativa en Google Sheets y otras herramientas, por una solución única y robusta.

Requisitos Funcionales (Generales):

EL SISTEMA DEBE PERMITIR:

Creación de Ticket Home: Registrar datos del paciente, cirugía, comorbilidades, FPA inicial y generar un identificador único.
Modificación de Ticket Home: Ajustar FPA con justificación y validación.
Visualización: Consultar estado e historial del ticket.
Gestión de Alta Real: Registrar alta efectiva y motivos de desviación vs FPA.
Anulación: Cancelar ticket con justificación.
Notificaciones: Informar FPA a los involucrados.
Reportes: Generar datos para análisis de gestión de camas y cumplimiento de FPA.
Seguridad: Control de acceso y auditoría de cambios.
Gestión de Datos Maestros: Administrar y utilizar tablas de referencia para cirugías, técnicas, estadías estándar, criterios de ajuste de estadía y motivos estandarizados.
[Agregar gestión de roles]
