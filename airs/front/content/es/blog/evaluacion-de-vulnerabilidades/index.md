---
slug: blog/evaluacion-de-vulnerabilidades/
title: ¡Nuevo bache hallado en tu sistema!
date: 2023-02-01
subtitle: Introducción a la evaluación de vulnerabilidades
category: filosofía
tags: ciberseguridad, pruebas de seguridad, pentesting, hacking, empresa
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1675214848/blog/vulnerability-assessment/cover_vulnerability_assessment.webp
alt: Foto por Saketh Upadhya en Unsplash
description: Conoce sobre evaluación de vulnerabilidades, por qué este proceso de TI es importante, cuáles existen y cómo se relaciona con la gestión de vulnerabilidades.
keywords: Evaluacion De Vulnerabilidad, Escaneo De Vulnerabilidad, Explorador De Vulnerabilidad, Pruebas De Penetracion, Vapt, Gestion De Vulnerabilidad, Analisis De Vulnerabilidad, Hacking Etico, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/_F21uFBVd7Q
---

No ser consciente de lo frágil que es tu aplicación,
red u otro sistema de información
hasta el momento en que es víctima de un ciberataque
es un error garrafal que no deberías cometer.
¿Aún no has puesto a prueba las posibles brechas,
debilidades o fallas de tu tecnología?
Evita que sea demasiado tarde para hacerlo.
Además,
todo el tiempo surgen nuevas vulnerabilidades de seguridad
en sistemas que evolucionan constantemente.
No basta con intentar identificar los problemas de seguridad
en una sola fase del desarrollo de aplicaciones,
o de forma esporádica.
Las **evaluaciones de vulnerabilidad**
deben ser continuas.
Conoce este proceso indispensable de ciberseguridad
con la ayuda de este artículo del blog.

## ¿Qué es la "evaluación de vulnerabilidades"?

En ciberseguridad,
como en otras áreas,
a veces nos encontramos con el uso indiscriminado
de términos y conceptos por parte de vendedores
y medios de comunicación.
El término "evaluación de vulnerabilidades",
por ejemplo,
a veces parece significar lo mismo
que "escaneo de vulnerabilidades",
"análisis de vulnerabilidades",
"pruebas de vulnerabilidades",
"investigación de vulnerabilidades"
y más.
Para fines prácticos,
en este artículo,
empezaremos considerando solo la primera asociación
y luego nos referiremos a otra.

La evaluación de vulnerabilidades
suele considerarse
como la evaluación sistemática de TI para identificar,
clasificar y reportar debilidades
o vulnerabilidades de seguridad en su código fuente,
operaciones, componentes, etc.
Dicha evaluación puede llevarse a cabo
mediante herramientas automatizadas o escáneres
(de ahí que se denomina comúnmente "escaneo de vulnerabilidades"),
que pueden detectar solo problemas de seguridad conocidos
(como los que aparecen en la lista de uso libre
[Common Vulnerabilities and Exposures](../../../pages/compliance/cve/),
o CVE.)
En otras palabras,
el alcance del análisis de un sistema por una de estas herramientas
depende de la información que tenga en su base de datos.

## ¿Por qué es importante la evaluación de vulnerabilidades?

Normalmente,
en una evaluación o exploración de vulnerabilidades de seguridad,
se espera que la herramienta reporte
cada hallazgo con detalles esenciales,
como su categoría, ubicación y gravedad,
para simplificar y priorizar su remediación
en un programa de gestión de vulnerabilidades.
(Como veremos más adelante,
[una solución de gestión de vulnerabilidades](../../soluciones/gestion-vulnerabilidades/)
tiene, entre sus partes, operaciones de evaluación de vulnerabilidades).
La remediación de vulnerabilidades es una operación fundamental
encaminada a mitigar la exposición al riesgo en el sistema evaluado y,
en consecuencia,
mejorar la seguridad de la organización
o del individuo propietario del sistema.
El riesgo, en este escenario,
está vinculado a la posibilidad de que un atacante
o ciberdelincuente explote las debilidades del sistema
en un ciberataque para acceder a información sensible,
robar recursos monetarios,
interrumpir funciones o servicios,
entre otras cosas.
Por lo tanto,
la evaluación de la vulnerabilidad actúa como
un componente esencial de
una **estrategia preventiva**.
Naturalmente,
la prevención ayuda a evitar los costos asociados
con el retraso en la remediación
y los impactos de los ciberataques.
Como beneficio adicional,
cuando se trata del campo legal,
la evaluación de la vulnerabilidad ayuda
a las empresas de diversas industrias a cumplir
con algunos requisitos de las normas internacionales de seguridad
como [PCI DSS](../../../compliance/pci/),
[HIPAA](../../../compliance/hipaa/),
[ISO 27001](https://docs.fluidattacks.com/criteria/compliance/iso27001),
[GDPR](../../../compliance/gdpr/)
y más.

## ¿Cuáles son los tipos de evaluación de vulnerabilidades?

Por lo general,
la clasificación de la evaluación de vulnerabilidades
se basa en los posibles sistemas de TI sometidos
a evaluación o escaneo.
Así,
podemos hablar de "**evaluación de la vulnerabilidad del servidor**"
cuando los objetivos de la evaluación
para la identificación de vulnerabilidades son servidores,
estaciones de trabajo u otros *hosts*,
es decir,
dispositivos conectados a una red.
Entonces, cuando el objetivo es toda una red,
ya sea pública o privada,
alámbrica o inalámbrica,
con todos sus recursos accesibles,
tenemos la "**evaluación de la vulnerabilidad de la red**".
Cuando se trata de detectar debilidades de seguridad
en bases de datos y sistemas o entornos de *big data*,
tenemos la "**evaluación de vulnerabilidad de bases de datos**".
Por último,
hablamos de "**evaluación de vulnerabilidades de aplicaciones**"
cuando el objetivo es una aplicación web o móvil
en la que se aplica el
[análisis dinámico](../../producto/dast/)
de sus operaciones
y el [análisis estático](../../producto/sast/)
de su código fuente.

A estas alturas surge la siguiente pregunta:
¿Podríamos clasificar también la evaluación
de vulnerabilidades en función de los métodos
de identificación de vulnerabilidades?
Bueno,
aquí es donde entra en juego una segunda asociación de términos.

## ¿Evaluación de vulnerabilidades frente a *pentesting*?

Aparte de lo que hemos dicho antes
sobre la relación entre la evaluación de vulnerabilidades
y el escaneo de vulnerabilidades,
también podemos hablar de la conexión entre
la evaluación de vulnerabilidades
y las [pruebas de penetración](../../soluciones/pentesting/)
(también conocidas como *pentesting*).
El *pentesting*
puede clasificarse como otra metodología
de evaluación de vulnerabilidades,
y mucha gente lo hace
(algunos hablan de VAPT: vulnerability assessment/penetration testing).
Incluso la inteligencia artificial ChatGPT,
bastante popular hoy en día,
lo hizo,
poniéndolo como el tercer tipo de evaluación
detrás de "evaluación de vulnerabilidad de redes"
y "evaluación de vulnerabilidad de aplicaciones".
Sin embargo,
el *pentesting* es una metodología;
no se refiere a un sistema específico a evaluar.
Por lo tanto,
entra más fácilmente en un contexto de comparación
con el escaneo de vulnerabilidades,
otra metodología.
Ambos son procesos diferentes para identificar
vulnerabilidades que,
de hecho,
pueden complementarse en lo que podríamos llamar
una "evaluación integral de vulnerabilidades".

El *pentesting*
es también un procedimiento de detección
y reporte de vulnerabilidades pero,
aunque se utilizan herramientas de apoyo,
es ejecutado principalmente de forma manual
por *hackers* éticos o *pentesters*.
Lo que estos profesionales buscan esencialmente
es identificar vulnerabilidades fuera del espectro
de las herramientas automatizadas.
Aquellas que son más complejas
(a menudo de mayor gravedad)
o desconocidas hasta ahora
(es decir, las vulnerabilidades de día cero).
El marco de trabajo de los *pentesters*
es pensar y actuar como atacantes.
Así,
más allá de detectar vulnerabilidades,
las explotan,
simulando ataques del "mundo real"
para probar los impactos potenciales.
Además,
el *pentesting* sirve para reducir
las tasas de falsos positivos y falsos negativos
de los escáneres de vulnerabilidades.
Los especialistas se encargan de revisar
y rectificar los reportes erróneos de acuerdo
a sus capacidades.

Para más información sobre el *pentesting*,
lee nuestra reciente serie de artículos:
"[What is Manual Penetration Testing?](../../../blog/what-is-manual-penetration-testing/),"
"[Types of Penetration Testing](../../../blog/types-of-penetration-testing/),"
"[Penetration Testing Compliance](../../../blog/penetration-testing-compliance/),"
and "[Continuous Penetration Testing](../../../blog/continuous-penetration-testing/)."

<div>
<cta-banner
buttontxt="Más información"
link="/es/soluciones/gestion-vulnerabilidades/"
title="Empieza ya con la solución de Gestión de vulnerabilidades
de Fluid Attacks"
/>
</div>

## Evaluación de vulnerabilidades dentro de la gestión de vulnerabilidades

Detectar las vulnerabilidades y,
entre otras cosas,
detallar los riesgos que representan
es fundamental para priorizarlas antes de su remediación.
Lógicamente,
aquellos problemas de seguridad
que representan el mayor peligro
(es decir, el impacto más significativo si se explotan)
son los que deben abordarse
y solucionarse con mayor urgencia.
Los recursos limitados,
como el tiempo y el esfuerzo,
deben invertirse en estos primero.
La evaluación de vulnerabilidades,
idealmente con escaneo de vulnerabilidades y *pentesting*,
puede entonces ser parte de una solución global
donde más allá de reconocerlas y detallarlas,
los problemas de seguridad son priorizados
y remediados, es decir,
la **gestión de vulnerabilidades**.

La priorización de vulnerabilidades
depende de los activos y funciones en riesgo
(debe haber claridad previa sobre cuáles son todos los activos
y su valor para la organización),
la facilidad de explotación de dichos problemas
y el daño que podrían causar,
entre otras cosas.
Por lo general,
las vulnerabilidades se califican con el sistema
Common Vulnerability Scoring System (CVSS), aunque,
en Fluid Attacks,
ya preferimos utilizar dicha métrica modificada:
"[CVSSF](../../../blog/cvssf-risk-exposure-metric)."
Por otro lado,
la remediación de vulnerabilidades puede ocurrir
a través de la implementación de controles de seguridad,
cambios en la configuración
y el desarrollo y aplicación de parches,
todos ellos sugeridos por escáneres de vulnerabilidades
y *hackers* éticos.

Como parte de [DevSecOps](../../soluciones/devsecops/),
la cultura actualmente predominante en ciberseguridad,
en la que hay una conciencia de la tecnología cambiante
(resultante de las optimizaciones de funcionalidad
y seguridad, por ejemplo)
y de las amenazas crecientes,
la evaluación de vulnerabilidades,
o mejor aún, la gestión de vulnerabilidades,
debe realizarse continuamente.
Esta solución debe tener lugar desde
las primeras fases del ciclo de vida de desarrollo de *software* (SDLC).
Las empresas pueden integrar herramientas
y procedimientos de evaluación de vulnerabilidades
con herramientas de gestión de vulnerabilidades.
Estas herramientas permiten a los usuarios disponer
de informes con vulnerabilidades detalladas y priorizadas,
y las recomendaciones necesarias
para trabajar en su remediación en un solo lugar.
Esto y más es lo que puedes encontrar en la
[plataforma](https://app.fluidattacks.com/) de Fluid Attacks.

## Evaluación y gestión de vulnerabilidades con Fluid Attacks

En Fluid Attacks,
ofrecemos servicios de evaluación de vulnerabilidades.
Con nuestra propia herramienta de evaluación de vulnerabilidades,
ejecutamos escaneos de vulnerabilidades.
Por medio de nuestros experimentados
y certificados *hackers* éticos,
realizamos pruebas de penetración.
Usando diferentes metodologías,
identificamos vulnerabilidades en tus aplicaciones
[web](../../../systems/web-apps/)
y [mobile apps](../../../systems/mobile-apps/),
[thick clients](../../../systems/thick-clients/),
[APIs and microservices](../../../systems/apis/),
[cloud infrastructure](../../../systems/cloud-infrastructure/),
[networks and hosts](../../../systems/networks-and-hosts/),
[IoT devices](../../../systems/iot/),
[SCADA and OT](.../../../systems/ot/),
[containers](../../../systems/containers/)
y [IaC](../../../systems/iac/).
Siendo nuestro cliente,
obtienes todos los reportes de problemas de seguridad
en tus sistemas en nuestra plataforma
de gestión de vulnerabilidades.
Allí,
más allá de obtener los detalles de cada hallazgo,
y las evidencias que avalan su existencia
y posible explotación,
recibes recomendaciones y consejos para su remediación,
tarea que incluso puedes asignar a miembros
de tu equipo desde la plataforma.
Desde allí,
también puede seguir el progreso de mitigación
de la exposición al riesgo de tu compañía
y comprobar si cumple con algunos de los requisitos
de [más de 60 estándares internacionales de seguridad](https://docs.fluidattacks.com/criteria/compliance/).

Todo esto forma parte de nuestro servicio característico:
[Hacking Continuo](../../servicios/hacking-continuo/).
Si aún no eres cliente nuestro,
pero quieres probar gratis durante
21 días nuestro plan con evaluación de vulnerabilidades
mediante herramientas automatizadas (Plan Machine)
[sigue este enlace](https://app.fluidattacks.com/SignUp).
[Contáctanos](../../contactanos/)
si prefieres obtener inmediatamente el plan integral
con evaluación tanto por herramientas de escaneo de vulnerabilidades
como por *hackers* éticos (Plan Squad).
