---
slug: blog/herramientas-devsecops/
title: Nuestras herramientas de DevSecOps
date: 2022-08-26
subtitle: Cómo usamos estas herramientas en Hacking Continuo
category: filosofía
tags: ciberseguridad, devsecops, pruebas de seguridad, software
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1661525496/blog/devsecops-tools/cover_tools.webp
alt: Foto por Syarafina Idris en Unsplash
description: Presentamos las herramientas de DevSecOps que utilizamos junto con las pruebas de seguridad manuales en nuestra solución Hacking Continuo.
keywords: Herramientas De Devsecops, Que Son Las Herramientas De Devsecops, Pruebas De Seguridad, Seguridad De Aplicaciones, Sca Y Sast, Desarrollo De Software, Hacking Continuo, Hacking Etico, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Editor
source: https://unsplash.com/photos/dCeWUxnIYaM
---

[DevSecOps](../../../es/blog/concepto-devsecops/)
es una cultura
que integra la seguridad en todas las fases
del desarrollo de *software*.
Como ya hemos dicho
en [nuestros consejos para la implementación de DevSecOps](../../../es/blog/como-implementar-devsecops/),
existen varias herramientas que pueden usarse
como parte de esta cultura en tu organización.
Una herramienta de DevSecOps,
que sirve como complemento al trabajo
de los expertos en pruebas de seguridad en este enfoque,
es la que permite realizar diversos métodos de evaluación
de forma automática
a lo largo del ciclo de vida de desarrollo de *software* (SDLC).
Los expertos realizan los métodos
de pruebas de seguridad manualmente
para identificar vulnerabilidades más complejas
y de mayor criticidad y, además,
revisan los reportes creados por las herramientas,
las cuales,
aunque son rápidas, tienen limitaciones en su precisión.
Esta metodología conjunta es muy valiosa para la integración completa
de la seguridad mientras se avanza a la velocidad de DevOps.

En este blog *post*,
hablaremos sobre las herramientas de DevSecOps
que utilizamos en Fluid Attacks
y cómo hemos logrado su implementación en nuestra solución
[Hacking Continuo](../../servicios/hacking-continuo/).

## ¿Qué son las herramientas de DevSecOps?

Hoy en día,
el proceso de desarrollo de *software*
se mueve a una alta velocidad.
Los desarrolladores necesitan desplegar soluciones
de *software* a producción varias veces al día
para satisfacer la demanda de los consumidores
y mantenerse al día con las tendencias.
Tradicionalmente, [DevOps](../../../blog/devops-concept/)
sitúa la seguridad en la fase de pruebas del SDLC,
buscando fallas y errores.
Pero en cuanto los equipos son conscientes
del grado en que los ciberataques pueden perjudicar
a su organización y a sus clientes,
aprenden qué tan importante es que la seguridad forme parte
del SDLC desde el principio.
Este es el núcleo de una cultura llamada DevSecOps
y se logra en parte integrando pruebas de seguridad manuales
y automatizadas en el flujo de trabajo
de DevOps para permitir comprobaciones
de seguridad en todo el SDLC.
Por supuesto,
decimos "en parte" porque hay que lograr algunas cosas
más para adoptar DevSecOps plenamente.
(Consulta "[Guía: Cómo implementar DevSecOps](../../../es/blog/como-implementar-devsecops/)"
y "[Buenas prácticas de DevSecOps](../../../es/blog/buenas-practicas-devsecops/)").

Las herramientas para DevSecOps,
que complementan el trabajo manual de los expertos en seguridad,
permiten ejecutar automáticamente algunos
métodos de pruebas de seguridad.
Estas herramientas se utilizan a lo largo de todo el SDLC
y con la orientación de expertos en seguridad.
Además de centrarse en las vulnerabilidades
que representan una mayor exposición al riesgo para un sistema,
estos expertos revisan constantemente
los reportes de resultados de las herramientas.
La colaboración entre el trabajo manual
y el automatizado permite obtener resultados más precisos y rápidos.
A continuación,
puedes ver una representación del SDLC.
Como hemos argumentado en [otro *post*](../../../es/blog/como-implementar-devsecops/),
las organizaciones que deseen implementar DevSecOps
necesitan definir cuándo se llevan a cabo las actividades de seguridad.
Por lo tanto,
algunas herramientas DevSecOps son más adecuadas
a partir de una determinada fase, pero una cosa es destacable:
la mayoría de ellas se utilizan antes de la fase de pruebas habitual.

<div class="imgblock">

![Pipeline DevSecOps Fluid Attacks](https://res.cloudinary.com/fluid-attacks/image/upload/v1661526215/blog/devsecops-tools/pipeline-devsecops-fluid-attacks.webp)

<div class="title">

(Imagen tomada de [aquí](https://marvel-b1-cdn.bc0a.com/f00000000236551/dt-cdn.net/images/devsecops-image-2000-6557ba1b00.png).)

</div>

</div>

## Herramientas de DevSecOps de Fluid Attacks

<br />

### Pruebas de seguridad de aplicaciones estáticas (SAST)

Las [pruebas de seguridad de aplicaciones estáticas](../../producto/sast/)
son un método que se puede utilizar continuamente
en el SDLC desde la fase de escritura de código en adelante
para buscar vulnerabilidades introducidas en el código fuente,
el código de *bytes* o los binarios de la aplicación.
Nuestro SAST automático analiza el código fuente de tu repositorio
y puede ayudarte a conocer rápidamente la criticidad
de las vulnerabilidades reportadas en él,
el nivel de exposición al riesgo
que corresponde a cada una de ellas,
dónde exactamente necesitas hacer cambios,
cuál es la corrección recomendada, etc.
Nuestros analistas de seguridad ejecutan SAST manuales
junto a nuestra herramienta para encontrar vulnerabilidades más complejas,
quizás de día cero, y reducir los falsos positivos y los falsos negativos.
A medida que los desarrolladores
de nuestras empresas clientes trabajan rápidamente
en la reparación de las vulnerabilidades que reportamos
y aprenden a no introducirlas de nuevo en el código fuente,
todos se convierten en desarrolladores de seguridad.

<div>
<cta-banner
buttontxt="Más información"
link="/es/soluciones/devsecops/"
title="Empieza ya con la solución DevSecOps de Fluid Attacks"
/>
</div>

### Análisis de composición de *software* (SCA)

El [análisis de composición de *software*](../../producto/sca/)
es un método
que puede introducirse en la fase de construcción
y utilizarse continuamente para examinar
las dependencias de código de terceros,
de las cuales tu *software* puede heredar vulnerabilidades.
Nuestro SCA automático no se limita a encontrar dependencias
de código abierto con vulnerabilidades,
sino que también identifica las licencias de todas las dependencias
de código abierto de tu base de código.
Para evitar riesgos legales,
[te aconsejamos](../../../blog/choosing-open-source/)
que elijas código abierto con una licencia compatible
con las políticas de tu organización.
Como nuestro SCA hace inventario de las dependencias
de código abierto de tu *software*,
es fácil elaborar una lista de materiales de *software*
(SBOM, por sus siglas en inglés).
En el SCA manual,
los *hackers* enriquecen los resultados de la herramienta,
verificando que se reporten todas las dependencias
de *software* con versiones vulnerables.
Como puedes adivinar fácilmente,
SCA y todos los métodos y herramientas de este blog *post*
deberían utilizarse todavía en las fases de producción.
Por ejemplo,
durante la fase de monitorización,
las compañías deben mantener actualizados los componentes de código abierto
e identificar cualquier amenaza debida a la explotación
de vulnerabilidades de día cero en estos por parte de criminales.

### Pruebas de seguridad de aplicaciones dinámicas (DAST)

Las [pruebas de seguridad de aplicaciones dinámicas](../../producto/dast/)
son un método que puede utilizarse
de forma continua a partir de la fase de prueba
para evaluar un artefacto de *software*
que puede desplegarse en ambientes de preproducción o pruebas.
¿Por qué?
Porque DAST ataca la aplicación
mientras está en ejecución y analiza su respuesta.
Nuestro DAST automático evalúa, entre otras cosas,
si la autenticación y la autorización de los usuarios
funciona bien y busca vulnerabilidades
que permitan ataques como la inyección de código.
Al combinar DAST automático y manual,
los ataques simulados son más ingeniosos,
ya que nuestros *hackers* crean sus propios *exploits*
y utilizan sus conocimientos de las técnicas empleadas
por los atacantes hoy en día.
Como DAST no tiene acceso al código fuente,
las pruebas de seguridad se complementan con SAST manual.

### Agente DevSecOps

El [agente DevSecOps](https://docs.fluidattacks.com/machine/agent)
de Fluid Attacks
es un componente que puede implementarse desde la fase
de escritura de código y utilizarse continuamente.
El agente comprueba si los cambios en el repositorio
incumplen las políticas de aceptación de vulnerabilidades
de la organización y **rompe el *build*** si es el caso.
Romper el *build* significa impedir
que una versión vulnerable del sistema se despliegue a producción.
Por lo tanto,
se encuentra entre las herramientas automatizadas
que refuerzan el desarrollo de código seguro.
Se puede deducir que su trabajo es personalizable
por cada organización para cada uno de sus proyectos.
Por ejemplo,
la organización puede definir que el agente
rompa el *build* solo para vulnerabilidades
cuya puntuación [CVSS](https://docs.fluidattacks.com/about/glossary/#cvss)
base esté entre ciertos valores.
Aunque nuestro agente DevSecOps trabaja de forma automática,
se alimenta de los resultados de SAST y DAST automatizados y manuales,
para que no haya dudas sobre su precisión.

### Plataforma

La [plataforma](../../plataforma/)
de Fluid Attacks
está preparada para funcionar
sin parar desde el inicio de tu proyecto,
en cada una de las fases de DevSecOps.
La plataforma es donde nuestras empresas clientes
mapean cada uno de sus activos digitales,
obtienen resultados de cada método de prueba de seguridad,
rastrean su exposición al riesgo a lo largo del tiempo,
reciben evidencia y orientación de nuestros *hackers* éticos,
gestionan la remediación de vulnerabilidades
y las partes interesadas, y mucho más.
El hecho de que nuestra plataforma no solo ofrezca
un inventario en tiempo real del *software* expuesto y atacable,
sino además todo lo anterior,
hace que sea más completa que las plataformas
de gestión de superficies de ataque.

## Uso de herramientas de DevSecOps en el Hacking Continuo

En Fluid Attacks
integramos las herramientas de DevSecOps
en una única solución denominada [Hacking Continuo](../../servicios/hacking-continuo/)
a lo largo de todas las etapas del ciclo DevSecOps.
En nuestro esquema de trabajo,
los desarrolladores despliegan primero los microcambios
en sus repositorios,
y luego nuestros [*hackers* éticos](../../../blog/what-is-ethical-hacking/)
buscan manualmente,
en conjunto con dichas herramientas automatizadas,
detectar **todos** los problemas de seguridad en la tecnología.
De esta forma,
probamos continuamente las últimas versiones
de los repositorios correspondientes
a los proyectos de nuestros clientes.
Es nuestro agente DevSecOps el que incorporamos
a los *pipelines* de integración continua
y despliegue continuo (CI/CD, por sus siglas en inglés)
para procurar que ninguna vulnerabilidad identificada
sea liberada a producción.
Gracias a nuestro esquema de pruebas de seguridad,
los equipos de desarrollo de *software* despliegan tecnología
a producción varias veces al día sin sacrificar
la velocidad ni la seguridad.

¿Deseas probar gratuitamente
nuestras herramientas de DevSecOps durante 21 días?
Echa un vistazo a nuestra
[prueba gratuita](https://app.fluidattacks.com/SignUp)
de Plan Machine de Hacking Continuo.
Si tienes alguna pregunta,
¡[contáctanos](../../contactanos/)\!
