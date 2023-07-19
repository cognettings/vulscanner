---
slug: blog/buenas-practicas-devsecops/
title: Buenas prácticas de DevSecOps
date: 2022-08-11
subtitle: Nuestros consejos para un desarrollo seguro en el SDLC
category: filosofía
tags: ciberseguridad, devsecops, pruebas de seguridad, compañía
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1660241560/blog/devsecops-best-practices/cover_practices.webp
alt: Foto por Leonard von Bibra en Unsplash
description: Fluid Attacks presenta nueve buenas prácticas de DevSecOps que ayudarán a tu empresa a integrar la seguridad en todo el proceso de desarrollo de *software*.
keywords: Buenas Practicas Devsecops, Automatizacion Devsecops, Sast, Dast, Romper El Build, Pruebas De Seguridad, Software Seguro, Hacking Etico, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Editor
source: https://unsplash.com/photos/L4-BDd01wmM
---

Las buenas prácticas de [DevSecOps](../../../es/blog/concepto-devsecops/)
garantizan la implementación de la seguridad
en el desarrollo de *software* y las operaciones de TI.
Las organizaciones que siguen estas prácticas permiten
a sus equipos trabajar de forma colaborativa,
crear *software* más seguro y aumentar la velocidad de desarrollo.

En este *post*
compartiremos nuestra selección de buenas prácticas
de DevSecOps que puedes empezar a implementar o reforzar ahora mismo.

## Facilitar la colaboración entre equipos

Adoptar una cultura y una mentalidad de DevSecOps
significa que las personas de los equipos de desarrollo,
operaciones y seguridad trabajan juntas
para lanzar *software* seguro con rapidez.
El objetivo de este cambio es permitir una comunicación fluida
y el trabajo en equipo,
fomentando así el sentido de propiedad y la responsabilidad.

[La implementación de DevSecOps](../../../es/blog/como-implementar-devsecops/)
implica que cada desarrollador
sea tan responsable de la seguridad del *software*
como cualquier miembro del equipo de seguridad.
Además,
cada uno puede aumentar sus conocimientos
de codificación segura corrigiendo los problemas detectados
por las pruebas de seguridad continuas.
El papel del equipo de seguridad es proporcionar entrenamiento,
así como ayuda y orientación complementaria.
Ya no lleva toda la carga de la seguridad sobre sus hombros.

## Fomentar la concientización de ciberseguridad de todos

Como ya hemos mencionado en nuestra
[serie de DevSecOps](../../../blog/tags/devsecops/),
la ciberseguridad comprende no solo la tecnología,
sino también las personas.
Los expertos en seguridad son responsables de implementar
y supervisar las pruebas de seguridad para perfilar el riesgo cibernético,
ofrecer soluciones y evaluar su eficacia.
También son responsables
de definir y cumplir las políticas de la organización.
Una mentalidad de DevSecOps
es aquella en la que todo el mundo es responsable de la seguridad.

Como la tarea permanente de gestión de riesgos
debe contemplar que todos estén de acuerdo
en su responsabilidad compartida,
las organizaciones necesitan integrar los esfuerzos
de concientización de la ciberseguridad para reducir
el riesgo de ciberataques y otros incidentes.

¿Y qué significa promover la concientización de la ciberseguridad?
Implica incitar a todo el mundo a reconocer
los problemas de ciberseguridad y a responder consecuentemente
con acciones que se hayan establecido
como adecuadas previamente de forma oficial.
A continuación se recomiendan algunas medidas para fomentar
la concientización de la seguridad para todos los miembros de la organización:

- Transmitirles las políticas de seguridad de la organización.

- Instruirles sobre el significado de los términos que se usan.

- Informarles de su rol en la protección de la información
  y en el [reporte de actividades sospechosas](../../../blog/human-security-sensor/).

- Mantenerles al día sobre los distintos vectores
  de ataque y las estrategias para mitigarlos.

Algunas de las cosas que puedes enseñar
a tu equipo son las definiciones de ciberseguridad,
el valor de la información, los mecanismos de control de acceso,
la gestión de contraseñas, la ingeniería social,
el *malware*, la informática segura
y los mecanismos de seguridad física.

## Capacitar para mantener el proceso de desarrollo seguro

A la hora de formar a los desarrolladores,
estas son algunas acciones que debería ejecutar
el equipo más fiable de expertos en seguridad de tu compañía:

- Enseñar a los desarrolladores la importancia de actualizar
  las dependencias del *software*.

- Enseñar a los desarrolladores
  a identificar posibles vulnerabilidades en el diseño de *software*,
  fomentando la codificación segura.

- Enseñar a los desarrolladores
  a corregir las vulnerabilidades de código poco después
  de que se escriban.
  Esto implica examinar el código de alguien mediante
  [pruebas de seguridad de aplicaciones estáticas](../../producto/sast/)
  (SAST),
  [análisis de composición de *software*](../../producto/sca/)
  (SCA)
  o [pruebas de seguridad de aplicaciones dinámicas](../../producto/dast/)
  (DAST)
  y, luego,
  impartir la formación pertinente sobre qué es lo que está haciendo mal.

Los expertos en ingeniería de *software*
que te pueden ayudar a llevar a cabo este método
se conocen comúnmente como
[campeones de seguridad](../../../blog/secdevops-security-champions-spa/),
que a veces tienen el cargo de
[ingenieros DevSecOps](../../../blog/what-does-a-devsecops-engineer-do/).

## Desplazar las pruebas de seguridad hacia la izquierda

DevSecOps consiste
en integrar la seguridad en cada parte de la ingeniería de sistemas
de la información lo antes posible en
el ciclo de vida de desarrollo de *software* (SDLC).
Esto contrasta con la realización de pruebas de seguridad
solo en las fases tradicionales de prueba y producción de *software*.

Para lograr el enfoque de desplazar
la seguridad hacia la izquierda,
las organizaciones deben incorporar escaneos de seguridad
en el flujo de trabajo de los desarrolladores,
junto con las pruebas de penetración manuales continuas,
para buscar vulnerabilidades conocidas
en el código que acaban de escribir.
Al disponer de un reporte oportuno de los problemas de seguridad,
los desarrolladores pueden remediarlos poco después que surjan.

## Lanzar cambios pequeños de forma rápida y segura

Integrar la seguridad en todas las fases del desarrollo
no lo hace más lento.
Al contrario,
DevSecOps permite a los desarrolladores ejecutar
una combinación de pruebas automatizadas
y manuales en su código y solucionar cualquier problema con prontitud,
lo que minimiza los riesgos de seguridad
(es decir, se reducen los problemas que debe resolver el equipo de seguridad)
y maximiza la velocidad de lanzamiento.
Además,
los desarrolladores pueden llegar a ser
más competentes en la codificación segura,
lo que ahorra aún más su valioso tiempo.
En general,
garantizar que todos los cambios pequeños en el código
se prueben desde el principio ayuda a que
el desarrollo progrese de forma constante y,
a la larga,
más rápida.

Para saber más sobre los retos
y los impulsores de la implementación de DevSecOps,
[haz clic aquí](../../blog/como-implementar-devsecops/).

## Combinar pruebas manuales con pruebas automatizadas

La automatización de procesos
es clave en la cultura de DevSecOps.
Al automatizar las pruebas de seguridad,
tienes la ventaja de acelerarlas
para la entrega rápida de *software*;
pero confiar solo en la automatización
y no combinarla con la experiencia de los *hackers* éticos
implica tener baja precisión,
es decir, altas tasas de falsos positivos y falsos negativos.
Las herramientas automatizadas
deben ayudar a los expertos a hacer lo siguiente:

- Categorizar y monitorizar el riesgo a lo largo del SDLC.

- Crear *tickets* o *issues* cuando se encuentren vulnerabilidades.

- Registrar el historial de las vulnerabilidades.

A continuación se presentan los tres métodos de evaluación
más populares que se pueden ejecutar repetidamente
durante el desarrollo para aumentar la eficiencia y la seguridad.

<div>
<cta-banner
buttontxt="Más información"
link="/es/soluciones/devsecops/"
title="Empieza ya con la solución DevSecOps de Fluid Attacks"
/>
</div>

### Pruebas de seguridad de aplicaciones estáticas (SAST)

[SAST](../../producto/sast/)
analiza el código fuente de la aplicación.
En una fase temprana del SDLC,
estas pruebas pueden señalar la ubicación exacta de las vulnerabilidades.
Son muy útiles para detectar problemas
tales como los relacionados con la falta de validación de datos,
que abren la posibilidad a un ataque por inyección de código.

### Pruebas de seguridad de aplicaciones dinámicas (DAST)

[DAST](../../producto/dast/)
no requiere acceso al código fuente de la aplicación.
Implica la evaluación de aplicaciones en ejecución
mediante el envío de vectores de ataque a sus puntos finales.
Estas pruebas pueden detectar vulnerabilidades
en la configuración del despliegue de la aplicación,
así como problemas de autenticación y de sesión,
pero no pueden mostrarte la ubicación exacta de estos problemas
de seguridad en el código.

Las herramientas SAST y DAST no son aconsejables por sí solas,
ya que producen reportes con un alto número
de falsos positivos y falsos negativos.
Además,
ninguna de estas herramientas puede encontrar problemas
de control de acceso
(el principal riesgo para las aplicaciones web
en el [último Top 10 de OWASP](../../../blog/owasp-top-10-2021/)),
mientras que las
[pruebas de seguridad manuales](../../soluciones/pentesting/)
sí pueden hacerlo.
Sigue leyendo para saber más sobre sus ventajas.

### Análisis de la composición del *software* (SCA)

Desarrollar con rapidez significa
no perder el tiempo reinventando la rueda.
Por lo tanto,
es normal que se utilicen dependencias externas
a lo largo de la construcción de tu tecnología.
De hecho,
es posible que se utilicen hasta tal punto que probablemente
no puedas recordar cada dependencia específica.
Esto es un problema cuando ocurre algo importante,
como el frenesí de explotación de las vulnerabilidades encontradas
en la popular herramienta de registro [Log4j](../../../blog/log4shell/),
y de repente todos tienen que informarse
sobre si utilizan o no la dependencia vulnerable en sus aplicaciones.

Para mitigar los riesgos que plantean
las dependencias de código
(especialmente los ataques a las cadenas de suministro),
una buena práctica consiste en disponer de un inventario completo
y actualizado de las dependencias que componen tu *software*
y mantenerlas al día con los últimos parches.
La respuesta a esta necesidad es [SCA](../../producto/sca/).

SCA requiere acceso a tu código fuente
para revelar las dependencias externas del *software*.
Así,
este análisis puede informarte
de las licencias de los componentes,
versiones y vulnerabilidades de seguridad,
en caso de que las haya.
Al realizar SCA combinando trabajo automático y manual,
no existen limitaciones debidas al lenguaje de codificación,
ni se limita el análisis a las vulnerabilidades comúnmente conocidas.

En la cultura DevSecOps,
es una buena idea realizar auditorías
de dependencia de código de forma continua,
temprana y a lo largo de todo el SDLC
para obtener información útil de forma rápida
y continua sobre vulnerabilidades
de componentes de código abierto o de terceros.

## Realizar auditorías de seguridad continuamente

Ya que las amenazas evolucionan continuamente,
las organizaciones necesitan evaluar a fondo sus sistemas
para comprobar si cumplen las buenas prácticas,
las normas internacionales y los reglamentos nacionales.
Como es de esperar con este alcance,
la evaluación no se limita a comprobar si el *software*
en uso tiene el último parche.
Una auditoría de seguridad incluye evaluar la integridad
de los componentes físicos de los sistemas,
la seguridad de la red y el comportamiento de los empleados.

Recomendamos auditorías
de seguridad *continuas* en lugar de *periódicas*,
ya que estas últimas podrían permitir una ventana de tiempo
durante la cual se podría aprovechar la exposición al riesgo.
Si actualizas tus conocimientos sobre los puntos débiles
de seguridad de tus sistemas,
se podrá supervisar constantemente el cumplimiento de la normativa.
Remediando esos problemas,
es posible dotar a tus sistemas de una protección más adecuada
frente a los ciberataques.

## Realizar evaluaciones manuales continuamente

Te recomendamos que cuentes con expertos
que evalúen tus sistemas de forma continua con técnicas como el
[*pentesting* manual](../../soluciones/pentesting/).
Estas implican el trabajo de [*hackers* éticos](../../../blog/what-is-ethical-hacking/)
que exploran el sistema para explotar vulnerabilidades
y evadir las defensas o revisar el código manualmente
(en Fluid Attacks, se ayudan de la priorización por IA),
entre otras cosas,
dependiendo de la fase del SDLC en la que se realicen las pruebas.
Estos expertos están al día en las tácticas utilizadas
por los atacantes y tienen la capacidad
de comprobar el nivel de seguridad de tu tecnología
frente a ataques especialmente diseñados para ella.

Dado que los reportes de seguridad basados
en escaneos realizados con herramientas automatizadas
tienen altas tasas de falsos positivos y falsos negativos,
valoramos inmensamente el trabajo manual realizado por los expertos.
Para que te hagas una idea,
[nuestros análisis](https://try.fluidattacks.tech/state-of-attacks-2022/)
de las pruebas de seguridad realizadas
el año pasado en los sistemas de nuestros clientes muestran que el
**67,4% de la exposición al riesgo se reportó solo con métodos manuales**.
Por ello,
sostenemos que las pruebas de penetración
son un componente valioso en favor
de la precisión y la profundidad.

En pocas palabras,
aconsejamos pruebas de penetración *continuas*
para validar la seguridad de tu tecnología
y probar contra nuevas técnicas utilizadas por los atacantes.
Esto contrasta con el consejo común de realizar
solo pruebas de penetración *periódicas*
con el fin de cumplir las regulaciones, entre otros motivos.
Las evaluaciones continuas apoyan una sólida cultura de remediación,
que va más allá de las obligaciones periódicas.

## Romper el *build*

Es recomendable impedir el despliegue
de un sistema si se detecta una vulnerabilidad en él.
En nuestro informe
[State of Attacks 2022](https://try.fluidattacks.tech/state-of-attacks-2022/),
reportamos que a los clientes
que activaron nuestra función para romper
el *build* **les llevó casi 30% menos de tiempo**
remediar las vulnerabilidades de sus sistemas que a los que no la activaron.
Esto es automático y responde a las políticas
de la organización que establecen qué tan severa
debe ser una vulnerabilidad para que rompa el *build*,
el periodo de gracia antes
de que una nueva vulnerabilidad reportada rompa el *build*, etc.
Con este ejemplo,
puedes ver que vale la pena automatizar herramientas y procesos.

## Prueba DevSecOps con Fluid Attacks

En Fluid Attacks
somos especialistas en pruebas de seguridad
[a lo largo de todo el SDLC](../../soluciones/devsecops/),
combinando herramientas automatizadas y pruebas de seguridad manuales.
Nuestro Plan Machine de
[Hacking Continuo](../../servicios/hacking-continuo/)
te permite encontrar vulnerabilidades de *software*
a través de SAST, DAST y SCA
con gran precisión mientras desarrollas.
Si te cambias a [Plan Squad](../../planes/),
puedes contar con nuestros *hackers* éticos
para encontrar vulnerabilidades complejas
y más severas con técnicas manuales y aconsejarte sobre cómo remediarlas.

Utilizando Hacking Continuo,
puedes hacer uso de nuestro agente DevSecOps,
el componente que romperá el *build*
de acuerdo con las políticas de tu organización.
Así te damos los medios para comprometerte plenamente
con el desarrollo de *software* seguro con rapidez.

¿Quieres probar Plan Machine de Hacking Continuo?
[Pulsa aquí](https://app.fluidattacks.com/SignUp)
para disfrutar de una **prueba gratuita de 21 días**.
[Contáctanos](../../contactanos/)
si deseas más información.
Estaremos encantados de responder a todas tus preguntas sobre DevSecOps.
