---
slug: blog/aws-devsecops-con-fluid-attacks/
title: Cómo potenciamos DevSecOps en AWS
date: 2022-10-24
subtitle: Pruebas manuales continuas para cumplir con AWS CAF
category: filosofía
tags: ciberseguridad, devsecops, nube, compañía
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1666640460/blog/aws-devsecops-with-fluid-attacks/cover_aws.webp
alt: Foto por Pejvak Samadani en Unsplash
description: AWS ha trazado el camino para lograr DevSecOps y ha creado su CAF, en el que aconseja realizar pentesting y red teaming, dos cosas en las que nos destacamos.
keywords: Devsecops, Aws Devsecops, Herramientas Aws Devsecops, Nube Devsecops, Devsecops En Aws, Aws Cloud Adoption Framework, Red Teaming, Hacking Etico, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Editor
source: https://unsplash.com/photos/rDQFKhNiHzs
---

[Amazon Web Services](https://aws.amazon.com/es/what-is-aws/) (AWS)
facilita y reduce el costo de desarrollar aplicaciones
con capacidad de crecimiento.
Con una lista de cientos de servicios que aumenta continuamente,
esta plataforma líder en la nube ofrece un enfoque
altamente granular de la infraestructura como servicio.
Además,
su infraestructura altamente redundante y extendida
por todo el mundo garantiza su disponibilidad y confiabilidad.
En consecuencia,
AWS presta atención a la seguridad de y en la nube.
Es con respecto a esta última que AWS permite a los usuarios
mejorar sus capacidades de DevSecOps.

Pero [DevSecOps](../concepto-devsecops/) ha sido malinterpretado
por muchos como el simple uso de herramientas automatizadas
para verificar la seguridad.
Como el propio AWS aconseja en su
[Cloud Adoption Framework](https://aws.amazon.com/es/cloud-adoption-framework/)
(CAF),
deberían aprovecharse también las técnicas manuales como el
[***pentesting***](../../../blog/what-is-manual-penetration-testing/)
y el [***red teaming***](../../../blog/what-is-red-team-in-cyber-security/)
para identificar problemas de seguridad.
Esto es fundamental,
ya que nuestros *hackers* éticos
[suelen encontrar](../../../blog/secure-infra-code/)
credenciales de AWS en el código y errores de configuración
en los servicios de AWS.
En este artículo del blog,
hablamos sobre cómo Fluid Attacks potencia tu implementación
de DevSecOps en AWS mediante el despliegue de técnicas manuales
en combinación con pruebas automatizadas.

## Seguridad en y del *pipeline*

Recordemos en primer lugar el modelo de responsabilidad compartida
(["shared responsibility model"](../../../blog/shared-responsibility-model/)
o SRM) en materia de seguridad en la nube adoptada por AWS
y varios otros gigantes.
¿Por qué?
Porque el desconocimiento o la negligencia están provocando vulnerabilidades
de las que los atacantes se aprovechan a diario.
Así pues, todos debemos ser conscientes de lo que AWS va a responsabilizarse
en materia de seguridad,
y de lo que está en nuestras manos.

Cuando AWS habla de seguridad en la nube se refiere
a aquello de lo que AWS es responsable.
Esto incluye el mantenimiento de sus zonas de disponibilidad
y la construcción de características de seguridad en sus productos
(p. ej., asegurarse de que los usuarios tienen las opciones
para restringir el acceso a los recursos del *pipeline*
a través de funciones de IAM y políticas de *bucket* de S3,
cifrar los datos en reposo y en tránsito
y almacenar datos y secretos de forma segura).

La seguridad en la nube, sin embargo,
es nuestra responsabilidad.
Los usuarios somos responsables de la seguridad
de lo que implementamos en la nube y de nuestra configuración
de los servicios de AWS.
Cuanto antes encontremos y solucionemos los problemas en esos aspectos, mejor.
En este tema es crucial la implementación
de [DevSecOps en la nube](../../../blog/why-is-cloud-devsecops-important/).

## DevSecOps en AWS con Fluid Attacks

[DevSecOps](../concepto-devsecops/) es una cultura que surge
de la integración de la seguridad en la totalidad
de los procesos de desarrollo y operaciones.
Esto significa que la seguridad se incluye en las primeras fases
del ciclo de vida de desarrollo del *software*
(incluso desde la fase de planificación).
(Consulta [aquí](../como-implementar-devsecops/)
cómo puedes implementar DevSecOps).
Cuando esto se intenta en la nube,
surgen requisitos de seguridad adicionales,
como la configuración adecuada de los servicios en la nube
y las pruebas de seguridad continuas de los archivos de infraestructura
como código (IaC) y las imágenes de contenedores.

AWS ha proporcionado pasos para respaldar DevSecOps
con servicios de AWS y herramientas de pruebas de seguridad automatizadas.
Además, ha publicado su
[CAF](https://aws.amazon.com/es/professional-services/CAF/),
que contiene una perspectiva de seguridad.
En él,
AWS expone brevemente unas buenas prácticas prescriptivas
que mejoran el estado de seguridad de los proyectos de aplicaciones en la nube.

Desde el principio,
deberías comprobar que has considerado y aplicado
las buenas prácticas de carácter directivo de AWS CFA,
que son las que tienen como objetivo mejorar las capacidades
de **gobernanza de la seguridad** y **garantía de la seguridad**.

Principalmente,
en lo que respecta a la gobernanza de la seguridad,
deberías haber identificado los riesgos específicos de tus activos
y la responsabilidad compartida en materia de seguridad
por parte de todos los miembros de tu organización.
Partiendo de este conocimiento,
puedes desarrollar, mantener y comunicar políticas, responsabilidades,
rendición de cuentas, etc.

Respecto a la garantía de la seguridad,
tendrías que revisar las precauciones que tomas
en cuanto a privacidad y configuraciones de seguridad
a través de controles
(p. ej., asegurarte de que se roten las credenciales de las cuentas,
eliminar usuarios de IAM inactivos y funciones no utilizadas, etc.).

El CAF también contempla buenas prácticas de carácter responsivo,
que mejorarían tu capacidad de **respuesta ante incidentes**.
Concretamente, afirman que el entorno AWS debe ser considerado
en tus planes de respuesta a incidentes
y que dichos planes deben ser simulados.

Pero las capacidades del CAF
que más se acercan a lo que pretendemos potenciar
en Fluid Attacks son las de carácter preventivo y de detección.
Aquí las presentamos,
junto con una versión resumida de sus buenas prácticas:

- **Gestión de identidad y acceso:**
  Disponer de controles que verifiquen la identidad de personas
  y máquinas y validar que los permisos de las cuentas
  no violen el principio de mínimo privilegio.

- **Protección de infraestructura:**
  Proteger contra el acceso no autorizado a los sistemas
  y servicios dentro de tu carga de trabajo
  (es decir, procesos y recursos que soportan tu aplicación
  y la interacción que los usuarios tienen con ella).

- **Protección de datos:**
  Cumplir con los requisitos de seguridad relativos al almacenamiento
  y codificación de datos.

- **Seguridad de aplicaciones:**
  Encontrar y corregir vulnerabilidades durante el SDLC.

- **Detección de amenazas:**
  Desplegar el monitoreo para identificar errores
  de configuración de seguridad,
  vulnerabilidades y comportamientos imprevistos.

- **Gestión de vulnerabilidades:**
  Identificar, caracterizar,
  reportar y mitigar vulnerabilidades de seguridad.

<div>
<cta-banner
buttontxt="Más información"
link="/es/soluciones/devsecops/"
title="Empieza ya con la solución DevSecOps de Fluid Attacks"
/>
</div>

Con el fin de respaldar estas capacidades,
existen herramientas de DevSecOps en AWS
(p. ej., herramientas de análisis de código
y gestión de vulnerabilidades de AWS)
que se ejecutan de forma automática y continua en el *pipeline* de CI/CD.
El *software* para DevSecOps que se ejecuta sin problemas
con el servicio AWS CodeBuild
-el cual compila código, ejecuta pruebas y produce paquetes de *software*-
puede realizar pruebas de seguridad de aplicaciones estáticas (SAST),
análisis de composición de *software* (SCA)
y pruebas de seguridad de aplicaciones dinámicas (DAST)
en etapas de desarrollo previas a la fase de pruebas tradicional.
La primera técnica analiza el código fuente
en busca de vulnerabilidades de seguridad conocidas,
la segunda encuentra *software* vulnerable de terceros
y la tercera evalúa la aplicación en ejecución desde el exterior
enviando vectores de ataque a sus puntos finales.
(Lee [aquí](../../../blog/differences-between-sast-sca-dast/)
la forma en que estas técnicas componen un enfoque integral
de las pruebas de seguridad).

Probablemente hayas oído que para lograr DevSecOps
hay que automatizar procesos y controles de seguridad.
No vamos a contradecir eso.
Evidentemente,
es importante que los procesos sean consistentes y reiterativos.
Lo que apoyamos es que evites dejarlo todo en manos de la automatización.
Estas herramientas presentan tasas
de falsos positivos y falsos negativos.
Por lo tanto, sus resultados deben revisarse manualmente,
y los *hackers* éticos deben añadirse a la estrategia de pruebas de seguridad
para completar la búsqueda de vulnerabilidades y problemas.

La combinación de automatización y trabajo manual es absolutamente necesaria.
Nuestro reporte
[State of Attacks del 2022](https://try.fluidattacks.tech/state-of-attacks-2022/)
muestra que **la totalidad** de las vulnerabilidades
de severidad crítica en los sistemas de nuestros clientes
fueron detectadas solo por nuestros *hackers* éticos.
Una de estas vulnerabilidades era tener credenciales de AWS
almacenadas en texto sin formato dentro del código fuente.
Este problema ocupó el segundo lugar entre aquellos
que más exponen a las organizaciones a riesgos.

Afortunadamente,
AWS CAF nos respalda,
pues fomenta el despliegue de métodos manuales
que simulan ciberataques del "mundo real" como una buena práctica
relacionada con la capacidad de gestión de vulnerabilidades.
Específicamente, el *pentesting* y el *red teaming*,
dos metodologías en las que destacamos.

El ***pentesting*** se refiere a simulaciones de ataques reales,
que a menudo implican la creación de *exploits* personalizados
para eludir las defensas de seguridad.
Pero el papel de los *hackers* éticos (o *pentesters*)
en este enfoque no se limita a las pruebas funcionales,
ya que también pueden realizar SAST y SCA manuales.
(Ten en cuenta que en este artículo del blog
siempre nos referimos al *pentesting* "manual".
En otro artículo, explicamos por qué pensamos que el "manual"
es el único tipo de *pentesting*).

A continuación, enumeramos las principales ventajas de nuestra
[solución de *pentesting*](../../soluciones/pentesting/):

- El conocimiento experto de los *hackers*
  permite una comprensión mucho más detallada de las vulnerabilidades.

- La combinación de automatización
  y pruebas de seguridad manuales nos permite garantizar
  la detección de vulnerabilidades críticas con tasas muy bajas
  de falsos positivos y falsos negativos.

- Se puede realizar de forma continua a medida que evoluciona
  el *software* nativo en la nube,
  en lo que se conoce como el modelo de
  [pruebas de penetración como servicio](../../../blog/what-is-ptaas/) (PTaaS),
  para que dispongas de conocimientos actualizados
  sobre el estado de tu seguridad.

- Rompemos el *build* para garantizar
  que ningún *build* vulnerable que viole las políticas
  de tu organización pase a producción.

- Una vez remediada una vulnerabilidad,
  puedes pedir a nuestros *hackers* que verifiquen que ya no está,
  todas las veces que sea necesario
  hasta que la resuelvas, sin costo adicional.

***Red teaming*** también se refiere
a simulaciones de ataques en el mundo real,
pero tiene algunas diferencias en comparación con el *pentesting*.
La primera es el enfoque holístico del *red teaming*,
ya que se propone poner a prueba la seguridad de una organización
a nivel tecnológico y humano (por ejemplo, los *hackers* éticos
pueden utilizar técnicas de
[ingeniería social](../../../blog/social-engineering/))
para determinar la eficacia de sus estrategias de prevención,
detección y respuesta a los ataques.
Lo que da pie a una explicación que también hace referencia
a una segunda diferencia entre  *red teaming* y el *pentesting*.
Específicamente,
en el *red teaming*,
la mayoría de los miembros del equipo de respuesta a incidentes
y los empleados no saben que los ataques se realizan
con el consentimiento de los directivos de la organización.
Por último, nos gustaría mencionar que *red teaming*
puede tener objetivos específicos en lugar de centrarse
en encontrar todas las vulnerabilidades.

Aparte de nuestra solución de *pentesting*,
las principales ventajas de nuestra
[solución de *red teaming*](../../soluciones/red-team/)
son las siguientes:

- Simulaciones de ataques altamente realistas
  que siguen las tácticas, técnicas y procedimientos
  de los atacantes maliciosos.

- Nuestros *hackers* éticos
  con [certificaciones](../../../certifications/) avanzadas
  (OSEE, CRTO, CRTE y CARTP) te ofrecen una amplia visión
  de la seguridad de tu organización.

Además,
en línea con las buenas prácticas de seguridad de DevOps en AWS
y una bajo la perspectiva de operaciones de CAF,
presentamos todos los hallazgos agregados en un único tablero:
la [plataforma](../../plataforma/) de Fluid Attacks.
Allí podrás obtener reportes detallados y actualizados,
conocer el riesgo asociado a cada vulnerabilidad detectada,
asignar miembros de tu equipo responsables de la remediación,
ponerte en contacto con nuestros *hackers*, entre muchas otras cosas.

Ahora que estás listo para comenzar [DevSecOps](../../soluciones/devsecops/)
de AWS con Fluid Attacks,
[contáctanos](../../contactanos-demo/).

Si todavía estás indeciso
y quieres experimentar primero con nuestras pruebas
de seguridad automatizadas,
comienza tu [prueba gratuita de 21 días](https://app.fluidattacks.com/SignUp).
Puedes cambiar de plan en cualquier momento para añadir
pruebas de seguridad manuales.
