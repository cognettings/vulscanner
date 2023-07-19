---
slug: blog/escaneo-de-vulnerabilidades/
title: Es(cáner)(caneo) de vulnerabilidades
date: 2023-02-17
subtitle: Definiciones, clasificaciones, ventajas y desventajas
category: filosofía
tags: ciberseguridad, pruebas de seguridad, pentesting, hacking, empresa
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1676670374/blog/vulnerability-scan/cover_vulnerability_scan.webp
alt: Foto por Alexander Ant en Unsplash
description: Aprende qué son los escáneres de vulnerabilidades y el escaneo de vulnerabilidades, cuáles son sus clasificaciones y cuáles son sus pros y contras.
keywords: Escaner De Vulnerabilidades, Escaneo De Vulnerabilidades, Evaluacion De Vulnerabilidades, Gestion De Vulnerabilidades, Pruebas De Penetracion, Deteccion De Vulnerabilidades, Hacking Etico, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Editor
source: https://unsplash.com/photos/blYwrwEGS6I
---

Hace unos días,
hablamos en este blog sobre "[evaluación de vulnerabilidades](../../../blog/vulnerability-assessment/)"
y
"[gestión de vulnerabilidades](../../../blog/what-is-vulnerability-management/)".
En esta ocasión
nos centraremos en "escáner de vulnerabilidades"
y "escaneo de vulnerabilidades".
Con la intención de vincular todos estos términos,
podemos decir de antemano que un escáner de vulnerabilidades
es una herramienta con la que se lleva a cabo el escaneo
de vulnerabilidades.
Este escaneo es una forma de evaluación de vulnerabilidades,
la cual es una de las operaciones necesarias dentro de un programa
de gestión de vulnerabilidades.
Examinemos las definiciones,
clasificaciones comunes y pros y contras de los escáneres de vulnerabilidades
y el escaneo de vulnerabilidades.

## ¿Qué es un escáner de vulnerabilidades?

Consideremos cada una de las palabras
que componen este término y veamos sus significados
generales para ilustrarnos antes de entrar en el terreno de la ciberseguridad.
Según el diccionario,
"vulnerabilidad"
es [el hecho de ser débil](https://www.oxfordlearnersdictionaries.com/us/definition/english/vulnerability?q=vulnerability)
y de herirse fácilmente física o emocionalmente.
Por otro lado,
un "escáner" es un dispositivo para examinar y registrar algo.
Incluso podemos encontrar útil la definición de esta palabra
dentro del ámbito de la salud:
"[máquina utilizada por los médicos](https://www.oxfordlearnersdictionaries.com/us/definition/english/scanner?q=scanner)
para obtener una imagen del interior del cuerpo
de una persona en una pantalla.

Ahora bien,
en el contexto de la ciberseguridad,
una vulnerabilidad puede verse como una debilidad dentro
de un sistema informático.
Una vulnerabilidad suele ser el resultado
de problemas de diseño o configuración y,
si es explotada por atacantes,
puede permitir a estos un acceso no autorizado
y privilegiado al sistema y comprometer sus operaciones o activos.
Un escáner de vulnerabilidades es entonces un dispositivo
o programa informático o herramienta de pruebas que identifica
y reporta automáticamente tales debilidades presentes en los sistemas
(p. ej., aplicaciones web y móviles,
redes, infraestructuras y dispositivos de IoT).

## ¿Qué es el escaneo de vulnerabilidades?

El escaneo de vulnerabilidades
es precisamente el procedimiento mencionado en el párrafo anterior.
No es más que otra forma de evaluación de vulnerabilidades que,
gracias a la automatización,
permite a las empresas descubrir rápidamente muchos de sus puntos débiles.
Normalmente,
los escaneos de vulnerabilidades se centran en identificar,
describir y reportar vulnerabilidades previamente conocidas
que están registradas en las bases de datos de los escáneres.
Estas máquinas suelen revisar los componentes
y configuraciones de sus objetivos de evaluación predeterminados
y los comparan o relacionan con la información que tienen
en sus bases de datos para identificar problemas de seguridad.

Las vulnerabilidades detectadas por un escáner pueden ser,
por ejemplo,
versiones de *software* obsoletas,
configuraciones erróneas e incumplimiento de requisitos de seguridad.
A veces,
estas herramientas automatizadas también trabajan
basándose en patrones de ataque específicos predefinidos
que envían al objetivo para comparar sus respuestas
con las que se supone se producen en presencia
de vulnerabilidades conocidas.

## ¿Cómo se clasifican los escáneres y el escaneo de vulnerabilidades?

Las clasificaciones que normalmente se encuentran
para estos términos no suelen ser muy claras ni convincentes.
Al no hallar categorías estrictas,
decidimos presentar tipos de escáneres según los objetivos
que evalúan y tipos de escaneo según los modos de funcionamiento:

### Tipos de escáneres de vulnerabilidades

- **Escáneres de vulnerabilidades de red o escáneres de seguridad de red:**
  Estas herramientas buscan vulnerabilidades
  en toda la red de una organización
  (es decir, escaneo de vulnerabilidades de red).
  Inicialmente identifican los puertos abiertos,
  los servicios que se ejecutan en esos puertos
  y el sistema operativo de los dispositivos de la red.
  Siguiendo sus bases de datos de vulnerabilidades conocidas,
  estos escáneres detectan problemas de seguridad
  en dispositivos como enrutadores,
  conmutadores, *firewalls* y servidores.
  Además de estos escáneres de vulnerabilidades centrados en redes,
  cabe mencionar los escáneres de vulnerabilidades basados en *hosts*,
  los cuales se centran específicamente en *hosts* de red individuales,
  como servidores o estaciones de trabajo,
  para identificar vulnerabilidades en sus sistemas operativos,
  aplicaciones y servicios.

- **Escáneres de sitios web
    o escáneres de vulnerabilidades de aplicaciones web:**
  Estas herramientas escanean sitios web
  y aplicaciones web para detectar problemas de seguridad,
  concretamente en su código y en sus configuraciones.
  Estos escáneres de vulnerabilidades web pueden utilizar
  tanto las bases de datos de vulnerabilidades
  conocidas como los patrones de ataque comunes mencionados
  anteriormente para identificar problemas
  o riesgos como los que podemos ver
  en el [Top 10 de OWASP](../../../blog/owasp-top-10-2021/)
  (p. ej., *Broken access control*, *Cryptographic failures* e *Injection*).
  Podemos incluir aquí escáneres
  como aquellos para hacer pruebas de seguridad
  de aplicaciones estáticas (SAST)
  y pruebas de seguridad de aplicaciones dinámicas (DAST).

- **Escáneres de vulnerabilidades de componentes de código abierto:**
  Estas herramientas se centran en identificar
  y analizar todos los componentes de *software*
  de código abierto de terceros
  y sus dependencias en búsqueda de vulnerabilidades
  (es decir, análisis de composición de *software* o SCA).
  El uso de componentes obsoletos con vulnerabilidades
  conocidas también figura en el Top 10 de OWASP y,
  como vimos en el [State of Attacks, 2022](https://try.fluidattacks.tech/state-of-attacks-2022/),
  fue el problema de seguridad que más contribuyó
  a la exposición al riesgo de las empresas que evaluamos
  desde Fluid Attacks en un año.

<div>
<cta-banner
buttontxt="Más información"
link="/es/soluciones/gestion-vulnerabilidades/"
title="Empieza ya con la solución Gestión de vulnerabilidades de Fluid Attacks"
/>
</div>

### Tipos de escaneo de vulnerabilidades

- **Escaneos integral y específico de vulnerabilidades:**
  En relación con lo que hemos mencionado
  sobre los escáneres basados en redes y en *hosts*,
  los escaneos de vulnerabilidades pueden variar
  en términos de exhaustividad.
  El **escaneo integral de vulnerabilidades**
  se enfoca en la evaluación de todos los sistemas que constituyen una red.
  Este puede detectar más vulnerabilidades que
  el **escaneo específico de vulnerabilidades**,
  el cual se centra en sistemas concretos,
  pero requiere más tiempo de análisis.

- **Escaneos externo e interno de vulnerabilidades:**
  **El escaneo externo de vulnerabilidades**
  se realiza desde fuera del perímetro de la red de una organización.
  Estas evaluaciones sirven para detectar vulnerabilidades
  que los atacantes podrían explotar desde fuera de la red
  para poder moverse "verticalmente" o dentro de ella.
  Allí,
  las herramientas se ocupan de los dispositivos de seguridad
  que bloquean el tráfico.
  Estos escaneos de seguridad identifican puertos abiertos
  y servicios y vulnerabilidades en dispositivos orientados a la internet,
  como servidores web y de correo y *firewalls*.
  El escaneo externo es esencial para la,
  ahora tan común, infraestructura en la nube,
  donde los escáneres deben analizar todos
  los activos alojados allí por una organización.

  **El escaneo interno de vulnerabilidades**
  se lleva a cabo desde el interior del perímetro
  de la red de una organización.
  Estas evaluaciones se utilizan para detectar vulnerabilidades
  que podrían ser explotadas por atacantes
  que han obtenido acceso a la red para desplazarse "lateralmente"
  a diversos sistemas de la misma.
  Estos escaneos identifican vulnerabilidades en servidores internos,
  estaciones de trabajo y otros dispositivos
  que no son visibles desde la internet.
  Estándares como el de PCI DSS suelen exigir a las empresas
  que realicen escaneos internos y externos con regularidad y,
  por ejemplo,
  cuando se modifica la red mediante actualizaciones
  o instalación de componentes.

- **Escaneos autenticado y no autenticado de vulnerabilidades:**
  También podemos referirnos a ellos
  como escaneos sin credenciales y con credenciales de vulnerabilidades.
  El **escaneo no autenticado de vulnerabilidades**
  no requiere el uso de credenciales de inicio de sesión.
  Estos escaneos se limitan a identificar vulnerabilidades
  que son visibles desde el exterior.
  Lo que se hace en estos escaneos es detectar servicios
  y puertos abiertos.
  Posteriormente,
  el escáner envía paquetes a los mismos para extraer
  la información disponible,
  como las versiones del *software* o del sistema operativo y,
  utilizando su base de datos,
  reporta las vulnerabilidades conocidas que puedan estar presentes.

  **El escaneo autenticado de vulnerabilidades**
  requiere el uso de credenciales de inicio de sesión.
  Estas evaluaciones son más precisas y exhaustivas que las anteriores.
  Consiguen recopilar datos más detallados
  o de nivel básico del sistema operativo y de aplicaciones
  y servicios específicos,
  así como detalles de configuración de los sistemas evaluados.
  En este caso,
  los escáneres detectan vulnerabilidades que solo son visibles
  tras iniciar sesión en el sistema.

## Pros y contras de los escáneres y escaneo de vulnerabilidades

Hoy en día existen montones de herramientas automatizadas
para el escaneo de vulnerabilidades,
incluyendo los escáneres de vulnerabilidades
comerciales y gratuitos.
Es habitual que las organizaciones interesadas en su ciberseguridad
utilicen varias de estas herramientas simultáneamente
para lograr una "cobertura total" con ayuda de sus diferentes características.
Aunque los escáneres de vulnerabilidades garantizan velocidad
de evaluación y permiten que las personas ahorren tiempo y esfuerzo,
su alcance es restringido.
Este alcance depende de las bases de datos
que los escáneres utilizan como referencia.
Estas bases de datos se componen de listas públicas
como la CVE ([Common Vulnerabilities and Exposures](../../../compliance/cve/))
y las propias listas de los proveedores
(generadas, mantenidas y actualizadas por sus grupos de investigación).
Todo lo que está fuera de estas listas no es detectado por los escáneres y
por tanto,
queda como un falso negativo
(es decir,
el escáner reporta la no presencia de una vulnerabilidad
cuando en realidad esta sí existe).

Además,
es cierto que los escáneres de vulnerabilidades pueden proporcionar
información detallada sobre sus hallazgos, como la ubicación,
la severidad o la exposición al riesgo,
la fecha de identificación,
el estado e incluso recomendaciones para remediar
o mitigar las vulnerabilidades.
Sin embargo,
muchos de estos reportes se refieren a falsos positivos
(es decir, los escáneres reportan la presencia de vulnerabilidades
donde en realidad no hay ninguna).
Algo que también puede resultar problemático
es confiar en los valores de severidad o riesgo asignados,
que suelen depender de métricas como el CVSS
(Common Vulnerability Scoring System).
Esto se debe a que los niveles de riesgo también pueden depender
de la relación que establezcan determinadas vulnerabilidades
en patrones de ataque específicos.
Aun así,
los escáneres las evalúan más bien de forma aislada
(las máquinas se centran en las "vulnerabilidades superficiales",
aquellas independientes de otras).
Además,
los escáneres suelen ser incapaces de identificar
aquellas vulnerabilidades que surgen
como resultado de combinaciones.

Dadas las dificultades mencionadas,
es necesario otro tipo de evaluación de vulnerabilidades:
las pruebas de penetración o
[*pentesting*](../../../blog/what-is-manual-penetration-testing/).
La cobertura total
no se consigue únicamente con herramientas automatizadas,
incluso aunque se implementen muchas.
La identificación de vulnerabilidades complejas
—a veces de mayor severidad—
y previamente desconocidas depende de la experiencia
y la astucia humanas, depende de los *pentesters*.
Estos pueden correlacionar vulnerabilidades
y detectar unas nuevas que surgen en determinados patrones de ataque.
Los *pentesters*
[simulan ataques del "mundo real"](../../../blog/what-is-breach-attack-simulation/)
e incluso explotan vulnerabilidades
para evaluar sus impactos.
Asimismo,
interpretan y validan los resultados de los escaneos
tanto para reducir las tasas de falsos positivos
como para entregar reportes que,
con puntuaciones más apropiadas,
permitan realmente priorizar la exposición al riesgo
de la empresa evaluada para pasar a acciones de remediación.
En definitiva,
podríamos decir que el escaneo de vulnerabilidades
puede considerarse un primer paso antes de,
o un apoyo inicial para,
las pruebas de penetración.

## Escaneo de vulnerabilidades con Fluid Attacks

En Fluid Attacks
disponemos de un escáner de vulnerabilidades de código abierto
que hemos ido desarrollando y que actualizamos
y mejoramos continuamente con la ayuda de nuestro *red team*.
Esta herramienta es capaz de aplicar [SAST](../../producto/sast/),
[DAST](../../producto/dast/)
y [SCA](../../producto/sca/).
En el 2021,
obtuvo un [resultado perfecto en el OWASP Benchmark](../../../blog/owasp-benchmark-fluid-attacks/)
versión 1.2 con SAST.
(De hecho,
aparece en la
[lista de herramientas de análisis de código fuente de OWASP](https://owasp.org/www-community/Source_Code_Analysis_Tools).)
Además,
en 2022,
[fue aprobada para pruebas de seguridad de aplicaciones en la nube](../../../blog/casa-approved-static-scanning/)
por la App Defense Alliance,
la cual busca garantizar que las aplicaciones
en Google Play no contengan vulnerabilidades de seguridad.

En [nuestro Plan Machine](../../planes/)
(que puedes probar ahora mismo de
[forma gratuita durante 21 días](https://app.fluidattacks.com/SignUp)),
puedes integrar nuestro escáner
en tu ciclo de vida de desarrollo de *software*
para hacer un escaneo continuo de vulnerabilidades.
(La continuidad en las pruebas de seguridad está recomendada
incluso por
el [centro para la seguridad en internet](https://www.cisecurity.org/controls/continuous-vulnerability-management)
o CIS.)
En nuestro Plan Squad,
cuentas con nuestro escaneo de vulnerabilidades
junto con las pruebas de penetración manuales por parte
de nuestros *hackers* éticos o *pentesters* altamente certificados.

En ambos planes
de nuestro [servicio Hacking Continuo](..//../servicios/hacking-continuo/),
sabemos que no interesa mucho quedarse
en la detección de problemas de seguridad
que los criminales puedan explotar en ciberataques.
Por ello,
Machine y Squad te ofrecen
nuestra [solución de Gestión de vulnerabilidades](../../soluciones/gestion-vulnerabilidades/),
la cual está apoyada
en nuestra única [plataforma](https://www.youtube.com/watch?v=I8bXM3Lv5DQ).
En esta,
nuestros clientes reciben reportes detallados
de sus vulnerabilidades,
asignan procedimientos de remediación,
solicitan reataques para verificar sus soluciones,
resuelven dudas con nuestros expertos,
llevan un control de sus avances en ciberseguridad,
y mucho más.

¡No dudes en [contactarnos](../../contactanos/)
si quieres ser uno de nuestros clientes!