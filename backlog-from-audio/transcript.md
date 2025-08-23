¡Hola! Claro, aquí tienes la transcripción y el resumen de los requerimientos que se conversaron en los audios.

### **Resumen de Requerimientos y Puntos Clave**

Basado en la conversación, estos son los principales ajustes y nuevas funcionalidades solicitadas para la plataforma:

**Gestión de Tickets y Documentos Impresos:**
1.  **Modificación de Alta Médica:** En el documento impreso, se debe ampliar el espacio de la firma del médico para incluir un campo de **"Notas Adicionales"**. Esto permitirá al médico anotar a mano cambios en la fecha/hora de alta para que la enfermera tenga un respaldo físico para modificar el ticket en el sistema.
2.  **Privacidad en Ticket:** La razón específica de una modificación de alta (ej. "complicación médica") **no debe aparecer** en el ticket impreso para proteger la privacidad del paciente.
3.  **Tickets Anulados:** Se debe **deshabilitar la opción de imprimir** para los tickets que ya han sido anulados.

**Funcionalidades del Administrador (Admin):**
4.  **Edición Completa de Tickets:** El perfil de administrador debe tener permisos para **editar todos los campos de un ticket existente**, incluyendo revertir un ticket anulado, cambiar el RUT, nombre, fechas, etc. Todos estos cambios deben quedar registrados en la auditoría.

**Exportación a Excel y Datos:**
5.  **Campo de Comorbilidades:** En el exportable de Excel, todas las comorbilidades o criterios de ajuste de un paciente deben ir en **una sola columna, separados por comas**, en lugar de crear múltiples columnas.
6.  **Visibilidad del RUT:** El RUT del paciente debe ser **visible en la tabla principal** del listado de tickets en la interfaz.

**Búsqueda y Filtros:**
7.  **Búsqueda por RUT:** El campo de búsqueda por RUT debe ser flexible, permitiendo al usuario escribir el número **sin puntos y sin el guion/dígito verificador**, y que el sistema lo reconozca y formatee igualmente.
8.  **Claridad en Filtros de Fecha:** Los filtros de búsqueda por fecha deben especificar **a qué fecha se refieren** (ej. "Fecha de Cirugía", "Fecha de Alta Proyectada").

**Lógica de Creación y Cálculo de Tickets:**
9.  **Fecha de Inicio:** El campo "Fecha y hora de pabellón" debe ser renombrado a **"Fecha y hora de admisión"**, ya que este es el verdadero punto de partida para los cálculos de estadía.
10. **Cálculo Automático del Alta:** El "Bloque horario de alta" **debe calcularse automáticamente** y no ser un campo a seleccionar por el usuario. Se calcula sumando el tiempo de la cirugía/procedimiento seleccionado a la fecha/hora de admisión.
11. **Regla de Negocio para Altas Nocturnas:** Se debe definir e implementar una regla para las altas calculadas en horarios tardíos (ej. después de las 20:00 hrs). El sistema debería proponer automáticamente el alta para el día siguiente.
12. **Información Quirúrgica Detallada:**
    *   Añadir un campo para la **"Especialidad"** de la cirugía. La selección de una especialidad debería filtrar la lista de cirugías disponibles.
    *   La selección principal debe ser por **nombre de la cirugía**, no por código, ya que una cirugía puede tener varios códigos asociados.
    *   Añadir un campo de texto libre tipo **"Observaciones" o "Comentarios"** en la sección de información quirúrgica para cualquier dato adicional.

---

### **Transcripción Detallada**

A continuación, la transcripción de las conversaciones.

#### **Audio 1 (Duración: 04:12)**

**(00:02) Mujer:** Hay veces que los médicos, cuando están, cuando generan el alta del paciente o generan un cambio de horario de alta porque el paciente tuvo alguna complicación, no le avisa al tiro a la enfermera como "oye este paciente no sé qué" y tampoco evoluciona en el GIS que corresponda que el paciente tuvo o se va a quedar más tiempo, ¿cachái?
**(00:21) Mujer:** Entonces, ahí perdemos un poco la traza para que la enfermera pueda hacer la modificación del ticket. Entonces lo que me decían, que ocurre mucho en Vitacura, es que el espacio donde está la firma del médico, de lo que tenemos nosotros ahora, podríamos dejar como si existe alguna fecha que el médico lo anote ahí para que la enfermera después pueda con ese respaldo hacer la modificación del ticket y lo vuelvan a dejar como a la vista de cara a la habitación del paciente.
**(00:50) Hombre 1 (Jonathan):** Entonces aquí en esta parte dejaríamos un texto distinto porque aquí dice "Firma y..." podríamos dejar el doble o triple de grande y podríamos poner "Firma Médico Tratante y Comentarios", ¿cachái? O "Notas Adicionales".
**(01:04) Mujer:** Sí, o cambio posible alta, nuevo horario, algo así, ¿cachái? Pero lo podemos manejar. Pero sí agrandar el espacio y poner un par de...
**(01:12) Hombre 1 (Jonathan):** Y "Notas Adicionales" voy a dejar. ¿Ya? Para que él pueda escribir a puño porque nosotros si tenemos una modificación de alta hay que gestionarla como modificación y eso tiene su campo específico acá como lo vimos en el otro.
**(01:23) Mujer:** Ah, tienes razón.
**(01:24) Hombre 1 (Jonathan):** Sí, entonces... Yo creo que podemos, al final es un texto nomás, ¿cachái? Si ahí el médico quiere decir así como "oye, este es mi teléfono", igual está bueno.
**(01:32) Mujer:** Sí, pues, sí. Pero es más que nada para que la enfermera después con eso pueda hacer el cambio en el sistema.
**(01:38) Hombre 1 (Jonathan):** Ya. Ya vale, vale. Lo dejamos también eso entonces.
**(01:41) Hombre 2:** Oye, esa... perdón, solo lo último, eh... ese documento, eso que sale para imprimir en la Tótems automática, ¿qué tan grande es?
**(01:50) Hombre 1 (Jonathan):** Este mira, sale es un documento, está formateado tamaño carta, así sale.
**(01:56) Mujer:** Oye, espérame, y se me quedaba una última cosa. Cuando hagamos la... cuando se hace una modificación porque el paciente, por ejemplo, tuvo una complicación médica, eh, ese detalle no tiene que salir en el ticket. Porque está a la vista de todos.
**(02:09) Hombre 1 (Jonathan):** La razón no debe salir.
**(02:11) Mujer:** La razón no debe salir.
**(02:12) Hombre 1 (Jonathan):** Creo que en el de la Vania salía y yo por eso lo consideré. Así que lo voy a quitar, dale.
**(02:16) Mujer:** Porfa.
**(02:17) Hombre 1 (Jonathan):** Ya, bien. Oye, genial, súper buena la reu, me voy. Muchas gracias, les cuento.
**(02:21) Todos:** Gracias, lindo finde, chao.
**(02:36) Hombre 1 (Jonathan):** Hola muchachos. Hola, hola. Sorry lo tarde.
**(02:41) Hombre 3:** Cuéntanos Jonathan, justo estábamos preguntando y revisando cómo se encontraban por las clínicas.
**(02:47) Hombre 1 (Jonathan):** Bien, oye por el lado de, bueno, de ambas clínicas tengo... me pasa que en ambas clínicas están las jefas de las áreas de laboratorio, pero ambas como que han un poco delegado el estado de la plataforma en quienes son como sus segundos a bordo. En el caso de Providencia, la... Juan Sobarzo, que es quien nos ha dado los feedback y todo, me indicó que ya estaba todo al 100. ¿Cachái? Así que tendríamos ok. En el caso de Vitacura, quien está a cargo en este momento, no recuerdo el nombre pero de apellido Carmona, me dijo que todavía tenían algunos problemas con los ODBC al parecer, porque tenían algunos equipos en los que no le estaba imprimiendo. Voy a contactar ahora al equipo para confirmar si es que tienen algún problema similar, pero en impresión de etiquetas y eso no tenían problema. ¿Cachái? Así que parece que estamos ya casi listos en RCO también, pero tengo ahí algún bemol por el lado de Vitacura. Ya, así que yo voy a confirmar, no tuve oportunidad de llamar antes, los voy a llamar ahora. No sé si en lo que le han comentado a Marco tendrá alguna novedad distinta, sé que le han estado informando también a él.
**(03:46) Hombre 3:** No, no me... no he podido hablar con Marco en esto, en este rato. Le voy a preguntar.
**(03:51) Hombre 1 (Jonathan):** Sí, ese feedback, Víctor, yo creo que es súper importante porque ahí puede que tengamos ahí algunos sesgos, no alcancemos a tener el feedback completo de cosas más técnicas o de un analizador en específico, ¿cachái?
**(04:04) Hombre 3:** Sí, sí, te entiendo.
**(04:05) Hombre 1 (Jonathan):** Yo voy ahora con el equipo de soporte y les confirmo si es que seguimos con algún problema de impresión o algo así.
**(04:09) Hombre 3:** Vale, gracias.
**(04:11) Hombre 1 (Jonathan):** Vale.
**(04:12) Hombre 3:** Carlos...

#### **Audio 2 (Duración: 23:37)**

**(00:18) Hombre 1 (Jonathan):** El Excel ya está funcionando como funcionaba siempre. Se los voy a mostrar mejor para que lo aprovechemos de mirar. Espérate, me voy a cambiar mejor a Providencia que tiene más datos y tenemos modificaciones.
**(00:30) Hombre 1 (Jonathan):** Denme un segundo. Vamos a entrar con el admin de Provi, el password.
**(00:39) Hombre 1 (Jonathan):** Entonces acá, listado de tickets. Exportamos a Excel. Voy a abrir el documento que se descargó.
**(00:55) Hombre 1 (Jonathan):** Y ahí lo tenemos funcionando tal como conversamos en algún momento con la... con todas las columnas.
**(01:09) Hombre 1 (Jonathan):** Todos los datos del ticket hasta acá y luego de ahí en adelante todas las modificaciones que pueda tener ese ticket en específico, principalmente indicando quién es, qué hizo la modificación, que eso también es bien positivo. Eh, fecha... creo que aquí debiésemos agregar la hora también de la modificación.
**(01:26) Mujer:** Oye, ¿y qué hay para la columna A?
**(01:30) Mujer:** Ah, sí está el RUT, no he dicho nada.
**(01:32) Hombre 1 (Jonathan):** Sí, tenemos RUT. Sí, estos son... finalmente están todos los datos que se seleccionan en el proceso de marcaje. Me queda duda con... creo que lo que no se está registrando acá es la... los... eh... los aspectos que, ¿cómo se llaman? Como la... las comorbilidades y todas esas otras cosas, paciente mayor, ¿cachái? Y estoy pensando en cómo debiésemos ingresarlas porque en la medida que eso vaya modificándose nos va a ir cambiando la base también.
**(02:02) Hombre 1 (Jonathan):** Podríamos pensar en un número máximo, tal como en las modificaciones, un número máximo de razones de que aumenten la causa origen.
**(02:12) Hombre 1 (Jonathan):** Ya bueno, ahí vamos a hacer nosotros alguna propuesta. Eso creo que es un dato relevante al menos para la información que vamos a extraer. Ya, así que funcionalidad Excel, ok.
**(02:22) Mujer:** Lo otro es que todos los campos... las comorbilidades que tenga... como el dato... no sé cómo se llama, estas, criterios de ajuste, gracias... eh, vayan todas, porque ponte tú que el paciente tenga las tres, para que no tengái que crear tantos campos, que sean dentro de un mismo campo separados por coma y ahí uno ve si lo quiere separar o no.
**(02:46) Hombre 1 (Jonathan):** Excelente idea. Eso es muy buena, Gata, muy muy buena.
**(02:49) Mujer:** Es que es lo más fácil y así agregamos 150.000...
**(02:53) Hombre 1 (Jonathan):** No, está bueno. Y sabís que me gusta porque con eso prescindimos de IDs, ¿cachái? Le digo al sistema que me pegue el texto, chao.
**(03:04) Hombre 1 (Jonathan):** Otra de las cosas que corregimos... bueno, la... o que ese número tenga una tabla aparte, no sé, pero es más fácil todo en un campo.
**(03:09) Hombre 1 (Jonathan):** No, pero eso es lo que quiero evitar, lo de las tablas aparte, ¿cachái? Porque en la medida que hagamos eso vamos a agregarle complejidad a la integridad de los datos y eso complejiza por el lado de la administración y por el lado del desarrollo. Así que prefiero que cada vez que se extraiga, lo que tú ves en pantalla salga en el texto, sin IDs ni nada de eso.
**(03:27) Hombre 1 (Jonathan):** Ya, después quitamos acá el título que había "MVP" en esta parte de acá abajito. Arreglamos el... el... ¿cómo se llama? El documento impreso. Se los voy a mostrar. Exportar PDF. Ahora muestra el rango, que nos estaba saliendo la hora.
**(03:42) Mujer:** Ah, perfecto.
**(03:43) Hombre 1 (Jonathan):** ¿Cachái? Así que ahora queda perfecto eso y si miramos uno que tenga las modificaciones como este de acá, vamos a ver también que están ahí las dos fechas con la nueva modificación y este está idéntico al original que tiene Clínica Providencia. Me fui a mirar su Excel y desde ahí lo tomé.
**(04:09) Hombre 1 (Jonathan):** Así que eso también estaría okay.
**(04:18) Hombre 1 (Jonathan):** La auditoría, no sé si se las habíamos mostrado. Tenemos incluso la... se captura la IP del equipo desde el que se está accediendo. Así que esto también es un punto positivo para el administrador. Esto igual me lo nos lo pidió con Carlos cuando estuvimos con el equipo de operaciones proyectos, que es el líder de ahí, el Javi García.
**(04:43) Hombre 1 (Jonathan):** Por el lado de ustedes, cuéntennos nomás qué cosas les faltan, qué sobra, por dónde hacemos los ajustes.
**(04:48) Mujer:** Ya, voy. A ver, eh... impresión de tickets anulados. Cuando un ticket está anulado, no debería dejar imprimir.
**(04:57) Hombre 1 (Jonathan):** Ya. Ya, está simple. Súper.
**(05:00) Mujer:** En estado... el estado anulado, ¿cachái? Porque se puede y obviamente te tira como una hora de salida pero ya no funciona ese ticket.
**(05:07) Hombre 1 (Jonathan):** Ya, perfecto. Entonces le vamos a quitar esta opción de exportar e imprimir para todos los tickets que estén en estado anulado. Súper fácil, dale.
**(05:14) Mujer:** ¿Ya? De eso mismo, eh... debería el administrador... esta quizás ya no sé si es tan fácil, pero... que las del admin, yo creo que al admin hay que ponerle más poderes, dale.
**(05:27) Mujer:** ...que pueda reversar un ticket anulado.
**(05:30) Hombre 1 (Jonathan):** Bien. O sea mira, yo creo que aquí en realidad lo que debiésemos hacer es que el admin sea capaz de editar un ticket al 100%. Que cambie nombres, que cambie RUT, que cambie fechas, que cambie todo. Lo importante es que quede en los registros de auditoría.
**(05:45) Mujer:** Ajá. Sí, porque me decían que les ha pasado que a veces se equivocan, no sé, la enfermera, ¿cachái? Y no tienen cómo después arreglarlo en este caso con esta plataforma.
**(05:58) Hombre 1 (Jonathan):** Ya, perfecto. Entonces vamos a agregar acá también una opción de edición orientada a los tickets.
**(06:30) Mujer:** Siguiente. Eh, los filtros de búsqueda.
**(06:35) Mujer:** El campo de búsqueda por RUT, que yo justo ayer... de hecho ahí estoy varias veces... eh, me buscaba por RUT pero ponte tú sin poner el... sin poner el guion ni el dígito verificador y no me dejaba buscar, ¿cachái? Me obligaba a poner 17.596. y eso es como más pajero de hacer, ¿cachái?
**(07:01) Hombre 1 (Jonathan):** Ya, ya, perfecto. Oye, no veo acá los... el dato.
**(07:04) Mujer:** Sí, eso también te iba a decir, no aparece el RUT en la tabla.
**(07:08) Hombre 1 (Jonathan):** Ya, entonces, considerar...
**(07:09) Mujer:** Porque tú buscái por RUT y igual te tira, pero en la tabla a la vista no está el RUT.
**(07:13) Hombre 1 (Jonathan):** Vale, vale, entonces súper claro. Agregar acá los RUT y segundo que sea un poco agnóstico o te vaya completando los puntos solo, como cualquier plataforma que uno usa actualmente.
**(07:23) Mujer:** Exacto. Y de hecho si tú mirái justo el Excel que sale de base, eso también debería quedar que el RUT siempre aparezca sin punto ni guion, o sea... sin puntos, por lo general.
**(07:36) Mujer:** Sí, pues, sin punto y con guion, porque lo separái en una columna después, pero con puntos se complejiza. O todos con puntos o todos sin puntos.
**(07:43) Hombre 1 (Jonathan):** Sí, eso se suele administrar con máscaras, así que lo que le vamos a decir al sistema es: tú olvídate de los puntos, pero siempre muéstrame puntos.
**(07:57) Mujer:** Ya, el cálculo de fecha de ingreso de estancia...
**(08:01) Hombre 1 (Jonathan):** ¿Creo un ticket y lo vamos mirando?
**(08:02) Mujer:** Por favor.
**(08:42) Mujer:** Ya, acá... eh... me levantaron... que sería bueno en la información quirúrgica, además de la cirugía, eh... indicar como la especialidad.
**(08:57) Hombre 1 (Jonathan):** Ya.
**(08:58) Mujer:** ¿Cachái? Que eso no lo teníamos considerado, pero sí sumar la especialidad de la cirugía: traumatología, eh... no me sé otras.
**(09:10) Hombre 1 (Jonathan):** Gastro.
**(09:10) Mujer:** Ah, Gastro, sí, pues, el de la manga. Ya, pero sumar esa especialidad porque también sumarlo a la base de datos que vamos a exportar porque también sirve para hacer análisis.
**(09:19) Hombre 1 (Jonathan):** Ya, entonces en ese sentido, Cata, la selección sería primero seleccionar especialidad, te muestra solo las cirugías relacionadas a esa especialidad y así se va acotando.
**(09:28) Mujer:** Claro. Sí, sería ideal.
**(09:29) Hombre 1 (Jonathan):** Ya, ¿y otra pregunta? ¿Código de cirugía?
**(09:41) Mujer:** Sí, me lo levantaron también.
**(09:42) Hombre 1 (Jonathan):** Ya. ¿Y ese código de cirugía...? No sé cómo es en Tracker. Mi sugerencia sería dejarlo solo con el código Fonasa.
**(10:34) Mujer:** Lo único que me queda de duda... o perdona, para cerrar. Quizás no lo normalicemos y que metan el código que quieran.
**(10:43) Mujer:** O sea, mira, yo siento que en realidad debería ser el nombre de la cirugía, porque me decían que hay algunos casos en que una cirugía tiene más de un código.
**(10:52) Hombre 1 (Jonathan):** Ya, sí, buen punto, buen punto.
**(10:54) Mujer:** ¿Cachái? Entonces, ¿cómo...? ¿Cómo lleno? ¿Cachái? ¿O qué le pongo? Entonces, para no complicar, porque la cirugía me imagino, y ahí Bastián pregunta, eh, sigue siendo la misma.
**(11:05) Hombre 1 (Jonathan):** ¿Cachái?
**(11:05) Mujer:** Que tenga dos códigos es un tema de cobro me imagino, pero tú seguís operándole la rodilla al paciente, ¿o no?
**(11:13) Hombre 2 (Bastián):** Así es.
**(11:16) Mujer:** Yo, en realidad, lo dejaría por nombre de cirugía y por la técnica, porque eso sí va a variar el horario o el tiempo que se tiene que quedar el paciente hospitalizado.
**(12:27) Hombre 1 (Jonathan):** Ya, perfecto. Entonces, lo dejamos como títulos solamente y les dejamos un campo libre, podría ser, que en el que podrían tal vez decir "se incluyó otro código" o "es esta técnica", ¿cachái? Quizás tal vez podría ser útil. Y les serviría para registrar código en el caso que quieran.
**(12:43) Mujer:** Sí, si quieren, claro. Pero que no sea como aperturado porque si no probablemente va a pasar que "oye pero es que yo la bariátrica la tengo con el 01050 no sé cuánto" y el del otro lado la va a tener con el 321 no sé. Entonces vamos a generar una complicación extra.
**(13:44) Mujer:** Mantengamos títulos nomás entonces.
**(13:45) Hombre 1 (Jonathan):** Claro.
**(13:46) Mujer:** Y ahí habría que agregar solamente el tema del tipo de especialidad, que eso sí lo encontré bueno.
**(13:50) Hombre 1 (Jonathan):** Ya, total, ya, considerado, lo vamos a agregar también entonces.
**(13:58) Hombre 2 (Bastián):** No sé si, por ejemplo, para aperturar un espacio ante cualquier elemento adicional que quieran manejar de manera local, un "otros" no obligatorio.
**(14:08) Hombre 1 (Jonathan):** Sí, un campo libre yo igual pensaría en eso, que creo que te sirve si es que querís darle igual con la cuestión del código o si querís dejar algún comentario adicional.
**(14:45) Mujer:** Ya, en el de fecha y hora de pabellón... Ya, ese debería ser... por cómo tenemos la data, que es por un día... debería ser fecha y hora de admisión.
**(15:02) Hombre 1 (Jonathan):** ¿Es de admisión? Creo que esta conversación la tuvimos igual, se definió admisión.
**(15:06) Mujer:** Sí, sí, de hecho ayer justo lo conversé con la Vania.
**(15:11) Hombre 1 (Jonathan):** Ya, y nosotros por el lado del proyecto lo revisamos también con quienes hicieron como el tema de los horarios.
**(15:25) Mujer:** Y es...
**(15:26) Hombre 1 (Jonathan):** Esas son como las pautas clínicas que le llaman, dale.
**(15:33) Mujer:** El título cambia.
**(15:36) Mujer:** Ya, y lo otro... está bueno igual el punto porque en realidad la gestión parte desde ahí. Y la asignación de cama y la reserva viene desde ahí. Totalmente de acuerdo.
**(15:48) Mujer:** Y el bloque de horario de alta, ahí tengo una pregunta, porque si yo selecciono, y que estaba pensando que quizás esto debería estar ahora al final, porque si yo selecciono la fecha y hora de término y ya sé la cirugía, el bloque de horario de alta debería calculárseme de forma inmediata. No yo proponerlo, ¿cachái?
**(16:08) Hombre 1 (Jonathan):** Mmm, tienes razón, pues. Sí, porque mira aquí abajo te lo va sumando de hecho.
**(16:16) Mujer:** Claro, y aquí está.
**(16:21) Hombre 1 (Jonathan):** Entonces lo que podríamos decirle es que me... que nos dé el bloque para esa hora y que parta como... que tome la hora de acá y le agregue dos horas, ¿cachái? Que el rango parta desde la hora sin minutos que está calculada.
**(16:48) Mujer:** Ya, pero ahí debería ser que le reste dos horas, por esto te lo digo. Porque cuando, ponte tú, voy a poner el ejemplo más fácil. Un paciente se admisiona a las 8 de la mañana y su horario máximo de estadía son 12 horas. Entonces, cuando yo pongo acá arribita, lo que le vamos a cambiar de fecha pabellón a fecha de admisión, va a ser 8 de la mañana y al yo seleccionar la cirugía, por detrás el cálculo debería decirme "el paciente se tiene que ir a las 8 de la noche".
**(17:19) Hombre 1 (Jonathan):** Ya.
**(17:20) Mujer:** Entonces, si se va a las 8 de la noche, su bloque horario de alta debería ser entre 6 de la tarde y 8 de la noche. Para yo no pasarme de hora.
**(17:28) Hombre 1 (Jonathan):** Sí, absolutamente de acuerdo. Sí, absolutamente de acuerdo, si no se va a pasar y le vamos a decir "oye, estái bien" pero en realidad se pasó.
**(17:35) Mujer:** Y por qué te digo que se tiene que calcular el bloque de horario de alta de forma inmediata, porque tú ahora pusiste, obviamente al azar, pero pusiste de 10 a 12 que se fuera, pero claro acá nos dice que el paciente se podría ir un cuarto para las dos de la mañana, ¿cachái? No te cuadra con lo que tú asignaste.
**(17:50) Hombre 1 (Jonathan):** Es que no tiene sentido, si esa es la verdad, no debiese estar esa pregunta porque lo estamos calculando abajo.
**(17:56) Hombre 1 (Jonathan):** Lo que voy a hacer acá, que lo había olvidado, es que esta información que se va calculando en la medida que vas completando nos aparezca acá arriba, cosa que el usuario vaya completando y el dato esté siempre ahí en pantalla.
**(18:25) Hombre 1 (Jonathan):** Lo que hoy está considerando es la técnica y los criterios de ajuste. Entonces no sé si dentro del mantenedor de cirugía...
**(19:11) Mujer:** Debiese ser... en la, cada cirugía... lo que ahí no sé es si dentro de las hojas maestras está considerado como la técnica, si suma o no suma horas. Quizás no suma horas, pero es un dato que se tiene que registrar.
**(19:30) Mujer:** O quizás lo otro Cata, es que siempre se habla de una cirugía y su técnica como un único concepto.
**(19:36) Mujer:** Sí, a eso voy. Justamente te iba a decir eso. O sea, finalmente lo que prima es el nombre de la cirugía, cuántas horas de hospitalizado tiene que estar, le tendríamos que sumar en el caso de que aplicara algún tipo de comorbilidad y eso que entregue un bloque de alta.
**(19:49) Hombre 1 (Jonathan):** Ya, es otro cambio cototo. Entonces lo que vamos a hacer acá es, vamos a tener, por ejemplo en los datos maestros, apendicectomía laparoscópica y apendicectomía tradicional. Y artroscópica, ¿cachái? Y las tres van a ser apendicectomía y las tres van a tener sus distintos horarios base y ahí tenemos el primer componente. Y el segundo componente y último va a ser esto de las razones de modificación que... no, el criterio... estos.
**(20:17) Mujer:** Ese. Exacto.
**(20:18) Hombre 1 (Jonathan):** Y entre esos dos se consigue la fecha estimada, el rango máximo de la fecha estimada de alta. Ya, súper.
**(20:25) Mujer:** Correcto. ¿Bastián, estás de acuerdo, cierto?
**(20:33) Hombre 2 (Bastián):** Lo que pasa es que me llamó la atención que está calculando, por ejemplo, un alta a la 1:45 de la madrugada.
**(20:42) Mujer:** Ah, también, sí, eso también tiene que corregir.
**(20:43) Hombre 2 (Bastián):** ¿Cachái? Porque se supone que el alta es hasta las 20, ¿o no?
**(20:49) Hombre 1 (Jonathan):** No, por motivo clínico no hay un horario.
**(20:53) Hombre 2 (Bastián):** Puede ser, pero no a la 1 de la mañana.
**(21:25) Mujer:** El alta planificada sí debería considerar que el paciente salga en un horario hábil o hasta X hora, ¿cachái? Estoy pensando en que, bueno, la cirugía ambulatoria no debería incluirse, pero en otra cirugía que sea 24 horas y que el paciente, no sé, voy a inventar, no sé si esto se da, pero que el paciente a las... llegó a las 11 de la noche a la admisión para operarse, no perdón, a las 11 de la mañana, entonces él debería irse... si son 12 horas, se tendría que ir a las 11 de la noche, quizás no se puede ir y eso significa que tenemos que sumarle el pernocte para que se vaya AM el día siguiente.
**(22:04) Hombre 1 (Jonathan):** Ya, perfecto. Oye, ahí entonces lo que nos va a faltar es la regla de negocio bien clarita. Para fechas estimadas de alta hasta las 9 de la noche se debe considerar el bloque del día siguiente desde entre las... ¿cachái? Como eso lo vamos a necesitar como un texto bien explícito.
**(22:19) Mujer:** Ya, ok.