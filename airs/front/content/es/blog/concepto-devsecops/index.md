---
slug: blog/concepto-devsecops/
title: ¿Qué es DevSecOps?
date: 2020-05-14
modified: 2022-06-13
subtitle: Buenas prácticas y fundamentos
category: filosofía
tags: ciberseguridad, devsecops, software, formación, empresa
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330852/blog/devsecops-concept/cover_c4reuk.webp
alt: Foto por Sebastian Pena Lambarri en Unsplash
description: Conoce qué es DevSecOps, su importancia, en qué se diferencia de DevOps y sus ventajas en seguridad para las entregas, pruebas y despliegues continuos.
keywords: Significado Devsecops, Devops Vs Devsecops, Mover La Seguridad A La Izquierda, Mejores Practicas Devsecops, Automatizacion Devsecops, Pruebas De Seguridad, Ciclo De Vida De Desarrollo De Software, Hacking Etico, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Editor
source: https://unsplash.com/photos/YV593oyMKmo
---

A grandes rasgos,
DevSecOps es una metodología que incorpora la seguridad
a los procesos de desarrollo (Dev) y operaciones (Ops).
En términos sencillos,
esto significa que la seguridad de la tecnología se evalúa
durante su desarrollo,
pero también que la seguridad es responsabilidad de todos.

Posiblemente te has dado cuenta
que la metodología [DevSecOps](../../soluciones/devsecops/)
se está adoptando cada vez más.
En 2021,
por ejemplo,
en un [estudio sobre DevSecOps](https://learn.gitlab.com/c/2021-devsecops-report?x=u5RjB_)
a nivel mundial
realizado por GitLab,
cerca del 36% de los encuestados afirmó que sus equipos desarrollan *software*
utilizando DevOps o DevSecOps.
Por tanto,
seguramente querrás saber qué significa este término.
En este blog *post*,
te daremos todos los conceptos básicos sobre esta metodología.
Después de leerlo,
puedes incluso visitar nuestra serie completa de *posts* sobre
[el tema](../../../blog/tags/devsecops/).

## DevOps vs. DevSecOps

DevSecOps
[ha sido referido como](https://www.infoq.com/articles/evolve-devops-devsecops/)
la extensión natural de DevOps.
Por lo tanto,
debemos comenzar explicando
cuál es la diferencia entre DevOps y DevSecOps.

### DevOps

[DevOps](../../../blog/devops-concept/),
quizá un concepto tan conocido como DevSecOps,
se define como una metodología de desarrollo de *software*
que busca reducir la brecha entre el desarrollo y las operaciones.
Para ello,
hace énfasis en la comunicación entre desarrolladores y operadores
y en la responsabilidad compartida de garantizar calidad en los productos.

Una de las principales características de DevOps es la velocidad.
De hecho,
aquí es donde destacan dos procesos,
ya que casi nunca están ausentes cuando se habla de DevOps.
Uno de ellos es la integración continua
(CI, por su nombre en inglés).
Este es un proceso
en el que los desarrolladores integran el código en el que trabajan
en un repositorio compartido
varias veces al día,
todos los días.
Junto con la CI está el despliegue continuo
(CD, por su nombre en inglés),
que significa trasladar el *software* al ambiente de producción,
proporcionando una respuesta rápida a las modificaciones
y una retroalimentación constante.
He aquí un resultado positivo:
En la
[encuesta de 2021](https://learn.gitlab.com/c/2021-devsecops-report?x=u5RjB_),
de GitLab antes mencionada,
casi el 60% de los desarrolladores afirmaron
que liberaban código el doble de rápido
gracias a DevOps.

### DevSecOps

Aunque DevOps suene muy bien,
no tiene sentido que un lanzamiento sea rápido
si el producto está plagado de errores.
Los equipos intentan evitar esto
[implementando DevSecOps](../como-implementar-devsecops/),
lo que significa que adoptan una cultura
en la que todos son responsables de la seguridad
y cada desarrollador evalúa su propio código,
ya sea con herramientas automatizadas
o técnicas manuales de pruebas de seguridad.
Algo que hacen durante todo
el ciclo de vida de desarrollo de *software* (SDLC),
es decir,
desde el principio hasta el final.

## Significado de DevSecOps

Hace un tiempo publicamos [un *post* sobre DevOps](../../../blog/devops-concept/).
Al final del mismo,
nos preguntábamos sobre la inclusión de la seguridad
en esta metodología de integración y despliegue continuos.
A raíz de ello,
hacíamos referencia al surgimiento del concepto
[**DevSecOps**](../../soluciones/devsecops/).
Si buscamos en la Internet una definición breve,
encontramos lo que se dice en el [glosario de Gartner](https://www.gartner.com/en/information-technology/glossary/devsecops):

<quote-box>

DevSecOps es la integración de la seguridad
en el desarrollo informático ágil emergente y DevOps
de la forma más transparente y fluida posible.
Idealmente,
esto se hace sin reducir la agilidad o la velocidad de los desarrolladores
ni exigirles que abandonen su entorno
de cadena de herramientas de desarrollo.

</quote-box>

Ok, esta información puede ser suficiente.
¡Nos vemos en el próximo *post*\!

<div class="imgblock">

![What is DevSecOps](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330850/blog/devsecops-concept/ah_jnw9fa.webp)

<div class="title">

Imagen tomada de [i.imgur.com](https://i.imgur.com/YezxAlA.png).

</div>

</div>

¡Es broma\! Hablemos al respecto.

Entonces,
¿qué significa DevSecOps?
Como dijimos en el *post* sobre DevOps,
el elemento **Sec**,
en referencia a la seguridad,
se añade a **DevOps**.
Pero para que quede claro,
no lo añadimos en cualquier parte,
lo añadimos en el medio: **DevSecOps**.
Se espera entonces que la seguridad desempeñe un papel importante
junto a los procesos de desarrollo (**Dev**) y operaciones (**Ops**).
DevSecOps es una evolución de DevOps
en la que la seguridad es entendida e implementada.
Ahora bien,
¿por qué se incluye la seguridad en esta metodología?
¿Por qué es importante DevSecOps?

## ¿Por qué necesitamos DevSecOps?

Muchos siguen ignorando la seguridad en la ingeniería de *software*.
Otros siguen viéndola como un obstáculo
que retrasa el proceso de producción.
Pero muchos otros han llegado a ver la seguridad
como una *necesidad* en un espacio virtual ampliamente compartido,
donde las intenciones de ciertos individuos resultan no ser las mejores.
Los más atentos a esta cuestión
han sido aquellos que desean mantener el prestigio de sus empresas,
las cuales pueden estar manejando datos personales
de enormes cantidades de usuarios.

Debemos ser conscientes
que los datos de los usuarios
y la funcionalidad de las aplicaciones
pueden ponerse en riesgo por la presencia de vulnerabilidades.
Así que,
para evitar debilidades y posteriores ataques a los productos,
hay que implementar medidas de seguridad
desde las primeras fases del SDLC.
Por lo general,
las pruebas de seguridad se han llevado a cabo
*justo antes* del despliegue de las aplicaciones
en el ambiente de producción.
Pero para muchos,
este método de evaluación ha sido engorroso.
¿Qué ocurre con aquellos que,
dentro de la cultura DevOps,
están continuamente creando funcionalidades en sus aplicaciones?
¿Están invirtiendo tiempo y esfuerzo
en encontrar o detectar deficiencias en su código
*justo antes* de cada despliegue?

Si ya están dentro de la metodología DevSecOps,
la respuesta es *no*.
Cuando hablamos de implementación en las etapas iniciales,
como se muestra en la figura siguiente,
el elemento de seguridad tiene que cubrir
el ciclo desde el inicio hasta su fin.

<div class="imgblock">

![Security in DevSecOps](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330850/blog/devsecops-concept/devsecops_vkkb14.webp)

<div class="title">

DevSecOps abarca el desarrollo y las operaciones.
Figura tomada de [images.idgesg.net](https://images.idgesg.net/images/article/2018/01/devsecops-gartner-image-100745815-orig.jpg).

</div>

</div>

## ¿Cómo funciona DevSecOps?

En este modelo,
las compañías tienen que establecer requisitos de seguridad
que deben cumplir durante el SDLC.
Estos requisitos
pueden basarse en evaluaciones de la infraestructura del sistema.
Dichas evaluaciones,
realizadas manualmente y desde el punto de vista del atacante,
detectan posibles problemas de seguridad.
En otras palabras,
estas evaluaciones pretenden responder a preguntas como:
¿Dónde pueden atacarnos los *hackers* maliciosos?
¿Cuáles son las áreas y la información que más debemos proteger?
¿Cuáles son las brechas que no debemos permitir en nuestras aplicaciones?
¿Cuál serán las contramedidas y soluciones que debemos establecer?

Siguiendo los requisitos de seguridad,
se realizan continuamente pruebas para encontrar vulnerabilidades.
Estas pruebas se llevan a cabo mediante herramientas automáticas
combinadas con [equipos de expertos en seguridad](../../soluciones/hacking-etico/)
que utilizan sus conocimientos para detectar deficiencias,
manteniendo el ritmo de DevOps.
El uso de estas herramientas
y de capacidades humanas
integradas en los *pipelines*,
empleando [pruebas de seguridad de aplicaciones estáticas](../../producto/sast/)
y [pruebas de seguridad de aplicaciones dinámicas](../../producto/dast/)
permite minimizar el número de vulnerabilidades.
Estos puntos débiles pueden detectarse de forma temprana,
mientras el código está en construcción,
y su remediación puede hacerse con prontitud.
La actuación oportuna de los expertos y las herramientas DevSecOps,
que deberían generar un registro continuo de información
y una retroalimentación inmediata,
permite a las empresas ir un paso por delante de los atacantes
y mantener los controles de seguridad.
Por eso son importantes las prácticas DevSecOps.

<caution-box>

**Precaución:**
(a) **Depender excesivamente de las herramientas y de su trabajo automático
puede dar lugar a altas tasas de falsos positivos y falso negativos.**
Por esta razón,
el papel de los expertos es fundamental
para lograr precisión
y evitar que los desarrolladores pierdan tiempo
confirmando si las vulnerabilidades son reales.
El principal riesgo es la existencia de falsos negativos o escapes.
Las organizaciones pueden desconocer ciertas vulnerabilidades de seguridad
que la tecnología actual no logra identificar.
(b) **Realiza las verificaciones de seguridad de forma gradual**,
empezando [por las áreas de mayor prioridad](https://medium.com/hackernoon/the-future-of-security-is-devsecops-9166db1d8a03),
intentando no sobrecargar de trabajo a los desarrolladores,
que suelen ser los responsables de subsanar las deficiencias.

</caution-box>

## Beneficios de DevSecOps

El informe de Forrester de 2021
sobre el estado de la seguridad de las aplicaciones
[mostró](https://securityboulevard.com/2021/04/forresters-state-of-application-security-report-2021-key-takeaways/)
que el 30% de los encargados de tomar decisiones
relacionadas con seguridad,
encuestados en 2020,
cuyas empresas sufrieron una brecha,
dijeron que el ataque había sido posible
debido a vulnerabilidades en su *software*.
DevSecOps tiene como objetivo evitar esto.
Como los cambios en el código se revisan para detectar vulnerabilidades,
es posible descubrir estas antes de que el usuario final
reciba un *software* defectuoso.

Otra [tendencia preocupante](../../../blog/cybersecurity-trends-2021/)
es la de los ataques a las cadenas de suministro.
Los equipos suelen utilizar componentes de terceros
para desarrollar su *software*.
Además,
si ellos mismos construyeron los componentes,
es probable que otros equipos los utilicen.
Si los atacantes encuentran una vulnerabilidad
que les permita alterar el código,
los componentes, los servicios en la nube, etc.,
comunes a varios proyectos de *software*,
terminan comprometiendo toda la cadena de suministro.
Las prácticas DevSecOps pretenden proteger el *software*
de los riesgos heredados de la cadena y evitar
que los equipos generen riesgos heredables a la cadena.

Y,
como mencionamos más adelante,
DevSecOps también puede permitir que tu equipo ahorre en costos de remediación.

## Cómo pasar de DevOps a DevSecOps

"¡Me apunto!
¿Cómo puedo arrancar?"
¡Qué bien que lo preguntes!
Afortunadamente,
tenemos un *post* donde ofrecemos una guía completa
sobre [cómo implementar DevSecOps](../como-implementar-devsecops/).
Aquí,
te daremos unos consejos sencillos
sobre cómo pasar de DevOps a DevSecOps.

Puedes empezar por **ampliar la responsabilidad compartida
y el sentido de pertenencia** del *software*
para también incluir su seguridad.
En su mayor parte,
esto se consigue creando la posibilidad de colaboración
entre los equipos de desarrollo,
operaciones y seguridad.
Lo que pretendemos aquí es que la gente adopte
una cultura y una mentalidad DevSecOps.

También puedes **especificar las verificaciones de seguridad**
que necesitan ser implementadas en tus procesos DevOps.
Lo ideal sería automatizar la mayoría de ellas.
Sin embargo,
es necesario hacer un esfuerzo
para formar a los desarrolladores en codificación segura,
revisando el código en busca de vulnerabilidades
tan pronto como se realice un cambio.
Además,
no importa si no son desarrolladores,
ingenieros o lo que sea;
cada uno de los empleados de tu compañía debe ser consciente
de los nuevos requisitos de seguridad establecidos
y saber cómo aplicarlos en su trabajo diario.

En este proceso,
deben surgir algunos roles y responsabilidades DevSecOps.
Hay una persona cuyo trabajo consiste en definir acciones,
dirigir los controles de seguridad
(por ejemplo,
realizar evaluaciones de riesgos y modelos de amenazas)
y supervisar las prácticas en el proceso DevSecOps.
Hablamos del ingeniero DevSecOps.
Ya en este blog hemos dedicado
un *post* a este rol,
en el que incluso mencionamos cómo convertirse en un ingeniero DevSecOps.
Te invitamos a [visitarlo](../../../blog/what-does-a-devsecops-engineer-do/).

<div>
<cta-banner
buttontxt="Más información"
link="/es/soluciones/devsecops/"
title="Empieza ya con la solución DevSecOps de Fluid Attacks"
/>
</div>

## Las mejores prácticas de DevSecOps

Es fundamental mostrar un compromiso con la seguridad
y mejorar las capacidades de DevSecOps.
Ya hemos identificado un conjunto de las mejores prácticas,
de las cuales hablamos ampliamente en [otro *post*](../buenas-practicas-devsecops/).
Aquí te ofrecemos un breve resumen:

- **Colaboración:**
  Fomentar una comunicación rápida
  y hacer posible que
  todo el equipo del proyecto
  conozca dónde están las vulnerabilidades en el código,
  quiénes las introdujeron,
  qué se ha hecho al respecto
  y cuáles son sus estados de remediación.

- **Sensibilización sobre ciberseguridad:**
  Informar regularmente a los empleados
  sobre las políticas de seguridad de toda la empresa
  (vital para mantener una conciencia activa en ciberseguridad),
  educarlos para que incorporen prácticas de seguridad
  en su trabajo diario
  (por ejemplo, pruebas y revisión del código),
  y hacerles responsables de evaluar y mantener la seguridad de su trabajo.

- **Velocidad:**
  Lanzar pequeños cambios de código de forma rápida y segura.

- **Pruebas a la izquierda:**
  Disponer de escaneos de seguridad integrados
  en el flujo de trabajo de los desarrolladores
  en las primeras fases del SDLC
  para buscar vulnerabilidades conocidas
  que ellos pudieron haber acabado de generar en el código;
  de esta forma pueden corregirlas
  antes de que el equipo de seguridad revise los resultados del análisis.

- **Automatización combinada con *pentesting* manual:**
  Integrar con éxito la seguridad en el SDLC,
  de modo que cada cambio en el código sea escaneado automáticamente,
  hacer un inventario continuo de las dependencias y manterlas actualizadas,
  y crear automáticamente *issues*/*tickets*
  o romper el *build*
  (según la política de la organización)
  en caso de encontrar una vulnerabilidad.
  Además,
  hacer esto continuamente
  y en conjunto con las pruebas de seguridad manuales.

- **Estándares de seguridad:**
  Automatizar el uso de estándares de seguridad,
  evaluados y establecidos por el equipo de seguridad,
  y evaluar continuamente el cumplimiento
  y la integridad de los componentes físicos de los sistemas,
  la seguridad de la red
  y el comportamiento de los empleados.

- **Auditorías de seguridad *continuas* en lugar de *periódicas*:**
  Identificar toda la superficie de ataque,
  y los posibles vectores de ataque
  para los sistemas de información,
  lo que suele ser parte de las evaluaciones
  de riesgos y la modelización de amenazas.

- **Pruebas de penetración continuas:**
  Disponer de *hackers* éticos
  que evalúen la seguridad de tus sistemas
  a lo largo de todo el SDLC,
  en lugar de realizar únicamente pruebas
  de penetración esporádicas que dejarían márgenes
  de tiempo durante los cuales los atacantes podrían invadir los sistemas.

- **Romper el *build*:**
  Impedir que el código vulnerable llegue a producción
  y repararlo rápidamente,
  reduciendo así el tiempo de remediación
  [hasta en un 30%](https://try.fluidattacks.tech/state-of-attacks-2022/).

¿Y cuáles son las fases de la implementación de DevSecOps?
Idealmente,
las prácticas anteriores deberías iniciarlas de forma gradual.
Algunas de ellas,
como la automatización,
pueden volverse más sofisticadas
a medida que adquieres experiencia en DevSecOps.
Para una guía detallada de DevSecOps,
consulta el [blog *post*](../como-implementar-devsecops/)
correspondiente.

## Seguridad a la izquierda

La importancia de iniciar las pruebas de seguridad
desde el principio del desarrollo de *software*
es fundamental.
Visualiza el SDLC en una línea recta horizontal,
con la planificación del proyecto situada en el punto más a la izquierda
y el despliegue a producción en el punto más a la derecha:
Lo que te pedimos es que desplaces las pruebas de seguridad
siempre hacia la izquierda.

La idea en torno a las pruebas llevadas a la izquierda
es identificar y abordar los problemas de seguridad en el *software*
desde las primeras fases del desarrollo.
Es decir,
no hasta bien iniciada la fase tradicional de pruebas del SDLC,
sino mucho antes,
incluso cuando se están definiendo sus requisitos
(por ejemplo, lo que debe hacer y los recursos necesarios).

Desplazar las pruebas hacia la izquierda
puede ayudarte a producir *software* más seguro
y ahorrar dinero.
Se ha argumentado que la remediación en las primeras fases del desarrollo
[es menos costosa](https://landing.fluidattacks.com/us/ebook/)
que en la fase de despliegue a producción.

## Automatización de DevSecOps acompañada de técnicas manuales

Como hemos mencionado antes,
lo ideal es tener controles de seguridad automatizados.
Esto incluye aspectos esenciales como
tener herramientas de pruebas de seguridad automatizadas
(por ejemplo, [SAST](../../producto/sast/),
[DAST](../../producto/dast/) y [SCA](../../producto/sca/))
en ejecución en tu SDLC.
Sin embargo,
estas herramientas pueden generar falsos positivos
y falsos negativos,
por lo que una estrategia aún mejor es tener personas
expertas que utilicen técnicas manuales
para encontrar vulnerabilidades en tu *software*.
De hecho,
en este punto podemos rescatar que,
por ejemplo,
nuestros *hackers* éticos,
en comparación con las herramientas que usamos,
[detectaron alrededor del 81%](https://try.fluidattacks.tech/report/state-of-attacks-2021/)
de las vulnerabilidades de severidades alta y crítica reportadas en sistemas
durante un periodo de análisis de varios meses en 2020.
En resumen,
la automatización de procesos te ahorra tiempo,
pero es necesaria la intervención manual
para lograr alta precisión.

## DevSecOps como servicio

Algunas organizaciones pueden considerar necesario
contratar servicios externos de DevSecOps.
Cuando lo hacen,
esperan que se les proporcione una solución
que aproveche los conocimientos y la experiencia práctica
de profesionales certificados en DevSecOps.
El proveedor de DevSecOps como servicio
es responsable de integrar metodologías y herramientas de seguridad
(como las herramientas para ejecutar comprobaciones de seguridad
en los *pipelines* CI/CD)
en todo el SDLC.
Además,
debe evaluar las vulnerabilidades actuales y potenciales del sistema
y ayudar a aplicar las mejores prácticas de ciberseguridad
más allá de la codificación segura.

En Fluid Attacks ofrecemos la implementación de [DevSecOps](../../soluciones/devsecops/)
como parte de nuestra solución [Hacking Continuo](../../servicios/hacking-continuo/)
Como se mencionó anteriormente,
entendemos que el uso de técnicas manuales
para las pruebas de seguridad
tiene beneficios evidentes
sobre las herramientas de pruebas de seguridad automatizadas.
Así que,
nosotros ayudamos a las organizaciones a implementar DevSecOps
ofreciendo las habilidades de nuestros *hackers* éticos
(además de las herramientas automatizadas)
para encontrar vulnerabilidades en todo el SDLC.
Mediante la realización de
[pruebas de *pentesting*](../../soluciones/pentesting/) continuas,
las organizaciones pueden validar la seguridad de su tecnología
y probarla frente a nuevas técnicas utilizadas por los atacantes
y, por lo tanto, no incluidas en el alcance de las herramientas automatizadas.

## ¿Cómo se relaciona DevSecOps con los *red teams*?

Puede que entonces quieras que tu sistema sea evaluado
para detectar vulnerabilidades
de la forma más realista posible.
Es decir,
que *hackers* éticos realicen ataques reales.
[Red teaming](../../soluciones/red-team/) puede hacerlo por ti.
Su relación con DevSecOps es que
puedes conseguir un mejor entendimiento de la seguridad de tu sistema
si los *hackers* éticos prueban continuamente las versiones del mismo
tal y como lo harían los atacantes maliciosos.
Esto implica que [solo algunas personas](../../../blog/tiber-eu-framework/)
de tu organización
deben conocer el acuerdo contractual con el *red team*;
el resto del equipo debe responder a los ataques
que se llevarían a cabo [sin previo aviso](../../../blog/attacking-without-announcing/).
La seguridad debería consistir en estar preparados
para ataques reales en cualquier momento,
y así es como DevSecOps se relaciona con los *red teams*.

Adicionalmente,
el *red teaming* [puede mejorar](https://www.devsecops.org/blog/tag/Red+Team)
tu implementación de DevSecOps
desafiando una típica mentalidad perniciosa:
Asumir que las vulnerabilidades pueden ser aceptadas
(no trabajar en su remediación),
ya que hay pocas posibilidades de que sean explotadas.
Así,
cuando tienes pruebas reales
de que los *hackers* han explotado una vulnerabilidad en tu *software*,
no te queda más remedio que priorizar su remediación
en lugar de centrarte en desplegar nuevas funcionalidades.

## DevSecOps con Fluid Attacks

Ahora,
para tener una idea más clara del rol de la seguridad en DevOps,
vamos a resumir brevemente lo que Óscar Prado,
analista de ciberseguridad,
compartió con nosotros sobre lo que Fluid Attacks hace por sus clientes.
Nuestra empresa ofrece servicios de *hacking* continuo,
una búsqueda constante de vulnerabilidades en sistemas informáticos.
Pero aunque se utilizan algunas herramientas en este proceso,
en Fluid Attacks confiamos en las herramientas
solo como apoyo a las operaciones de nuestros *hackers*,
contrario a lo que hacen otras compañías.
Aquí damos más valor a los conocimientos
y habilidades de los *hackers* éticos
para garantizar una mayor precisión en las pruebas.
El trabajo de estos puede iniciar
"desde el momento en que los desarrolladores suben el primer *commit*",
revisando cada nuevo cambio,
y puede continuar después
de que la aplicación se haya desplegado a producción.

Cuando se detecta una vulnerabilidad en el código del cliente,
un miembro de nuestro equipo puede desarrollar un *script* personalizado,
llamado *exploit*,
asociado al hallazgo.
Ese *exploit* "comprueba automáticamente
si el hallazgo del analista persiste".
Por lo tanto,
"si el cliente quiere hacer nuevos cambios en su producto,
debe arreglar primero el hallazgo",
porque si no lo hace,
el *exploit* seguirá reportando la presencia de la vulnerabilidad.
Entonces,
según unos requisitos definidos por el equipo del cliente,
el agente DevSecOps de Fluid Attacks romperá el *build*,
y el proceso de despliegue se detendrá automáticamente.
"De esta forma,
se prioriza la seguridad,
y nuestras pruebas de detección de vulnerabilidades se integran
en el SDLC del cliente",
concluye Óscar.

<div class="imgblock">

![Break the build](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330851/blog/devsecops-concept/build_wmkfpb.webp)

<div class="title">

Romper el *build* significa detener el proceso de despliegue de *software*.
Imagen tomada de [citymetric.com](https://www.citymetric.com/sites/default/files/article_2015/01/149818154.jpg).

</div>

</div>

**Bonus:**
Fluid Attacks está convencido de que la velocidad sin precisión es inútil.
Por eso,
hemos combinado lo mejor de cada uno:
Tecnología y conocimiento producen un buen equilibrio.
Muchas empresas de ciberseguridad ofrecen herramientas rápidas y automatizadas
que son muy propensas a falsos positivos y falsos negativos
en la búsqueda de vulnerabilidades.
Fluid Attacks ha reconocido que debe haber trabajo humano en estos procesos
para garantizar la precisión y la eficiencia.
Fluid Attacks no ha olvidado el valor de la rapidez,
sino que siempre la ha mantenido en paralelo
con pruebas de alta calidad y excelentes resultados.
Por ello,
invitamos a las organizaciones a automatizar las herramientas y los procesos
cuando sea posible
y a confiar en *hackers* éticos
para realizar pruebas de seguridad sofisticadas.
De esta forma podrán alcanzar sus objetivos de DevSecOps.

## ¿SecDevOps?

Curiosamente,
cuando hablamos con Óscar,
él no utilizó el nombre DevSecOps,
sino **SecDevOps**.
Trasladó la seguridad a la izquierda.
Con SecDevOps,
quizás se pone más énfasis
en establecer inicialmente unos requisitos de seguridad a seguir
a través de los procesos de pruebas llevados a cabo continuamente
en el SDLC.

Independientemente del nombre que demos a la inclusión de la seguridad
en la metodología DevOps,
dentro de esta nueva cultura empresarial
se espera que la seguridad juegue un papel esencial
en la producción y mantenimiento de *software* desde el principio.
Se pretende que todos los implicados en los proyectos conozcan
y apliquen la seguridad;
por eso necesitan formación.
Hay que tener en cuenta que,
al igual que en DevOps,
no debería haber equipos separados por funciones,
sino por productos.
Al final,
todos deben ser responsables de la seguridad.

Las empresas que decidan implementar el enfoque [DevSecOps](../../soluciones/devsecops/)
(o, quizás mejor dicho, SecDevOps)
conseguirán importantes beneficios,
especialmente en la calidad y seguridad de sus procesos y productos.
¿Quieres recibir asesoría sobre cómo hacerlo?

En Fluid Attacks te ayudamos a aplicar las prácticas DevSecOps:
Puedes incorporar a tus *pipelines* nuestro
[agente DevSecOps](https://docs.fluidattacks.com/machine/agent)
y configurarlo para que
[rompa el *build*](../../soluciones/devsecops/)
si nuestras herramientas SAST o DAST
encuentran una vulnerabilidad abierta en tu *software*.
Además,
puedes preguntarnos por nuestro [Plan Squad](../../planes/),
que incluye [*hackers* éticos](../../soluciones/hacking-etico/)
que evalúan la seguridad de tu tecnología.
Para obtener más información
y resolver todas tus dudas sobre DevSecOps,
¡[contáctanos](../../contactanos)\!
