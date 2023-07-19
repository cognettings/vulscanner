---
slug: blog/escaneo-estatico-aprobado-por-casa/
title: Escaneo estático aprobado por CASA
date: 2022-12-23
subtitle: Nuestro CLI fue aprobado para asegurar apps en la nube
category: política
tags: cybersecurity, security-testing, software, cloud, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1671827428/blog/casa-approved-static-scanning/cover_casa.webp
alt: Foto por Kostiantyn Li en Unsplash
description: Nuestra herramienta automatizada es recomendada por App Defense Alliance para el escaneo estático bajo el marco Cloud Application Security Assessment (CASA).
keywords: Seguridad De Aplicaciones, Pruebas De Seguridad, Cloud Application Security Assessment, Casa, Escaneo Estatico, Machine, App Defense Alliance, Hacking Etico, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Editor
source: https://unsplash.com/photos/NDJPAIKrTEE
---

App Defense Alliance (ADA)
ha añadido la aplicación CLI de Fluid Attacks
como herramienta aprobada para las pruebas de seguridad de aplicaciones
(AST por sus siglas en inglés).
ADA es una asociación entre Google y colaboradores,
formada para garantizar que las aplicaciones de Android
sean seguras para los usuarios.
Nuestra
[herramienta de código abierto](https://docs.fluidattacks.com/machine/scanner/plans/foss)
es de uso gratuito para el análisis estático
y ha sido aceptada oficialmente para validar
los requisitos de nivel 2 bajo el marco
de Cloud Application Security Assessment (CASA) de ADA.

## El objetivo de App Defense Alliance

ADA [surgió en 2019](https://security.googleblog.com/2022/12/app-defense-alliance-expansion.html).
Sus miembros son Google,
ESET, Lookout, Zimperium y, más recientemente, McAfee y Trend Micro.
Esta alianza se compromete a garantizar
que las aplicaciones disponibles en Google Play
no estén plagadas de vulnerabilidades.

Para cumplir su propósito,
ADA exige a los desarrolladores verificar
que sus aplicaciones cumplan las normas de industria
en cuanto a seguridad de las aplicaciones.
En el caso de las aplicaciones móviles,
ADA puso en marcha
el marco [Mobile Application Security Assessment](https://appdefensealliance.dev/masa)
(MASA),
mientras que para las aplicaciones en la nube,
estableció el marco
[Cloud Application Security Assessment](https://appdefensealliance.dev/casa)
(CASA).

El marco MASA valida que
las aplicaciones cuenten con los controles de seguridad
definidos en el
[Estándar de Verificación de Seguridad de Aplicaciones Móviles](https://docs.fluidattacks.com/criteria/compliance/owaspmasvs/)
(MASVS, por sus siglas en inglés) de OWASP.
(Por cierto,
hemos listado [en otro artículo](../../../blog/what-is-mast/)
los principales riesgos para las aplicaciones móviles
y definido el papel de
las pruebas de seguridad de aplicaciones móviles (MAST),
que, si [realizas con nosotros](../../producto/mast/),
pueden comprobar si cumples con MASVS y otras guías internacionales.)

Sin embargo,
en este artículo nos centraremos en el marco CASA.
Así que vamos a explicarlo con más detalle.

## Cloud Application Security Assessment (CASA)

ADA creó CASA como una iniciativa para que
las aplicaciones Android
cumplan con los controles propuestos por el
[Estándar de Verificación de Seguridad de Aplicaciones de OWASP](https://docs.fluidattacks.com/criteria/compliance/asvs)
(ASVS, por sus siglas en inglés).
Su principal objetivo con este proyecto
es permitir integraciones seguras entre nubes
y potenciar su extensibilidad e inclusividad.

Ahora bien,
las aplicaciones varían en aspectos
como la sensibilidad de los datos a los que acceden,
la cantidad de usuarios por tipo de datos a los que se accede
y el nivel de tolerancia al riesgo de la empresa que las desarrolla.
Por eso,
el marco está diseñado para adoptar un enfoque de varios niveles basado
en los riesgos.
Dicho en términos simples,
los niveles (1, 2 y 3) indican hasta qué punto deben cumplirse
estrictamente los requisitos de seguridad.

Los usuarios del marco,
como Google,
piden a los desarrolladores que verifiquen
el cumplimiento de los estándares de CASA.
Son los primeros,
no los desarrolladores, quienes determinan el nivel.
Por supuesto que los desarrolladores
[pueden optar](https://appdefensealliance.dev/casa/casa-self-start)
por iniciar la evaluación sin haber sido contactados,
pero solo superando la evaluación del nivel 3
obtendrían una verificación válida de CASA.
Este nivel requiere que los desarrolladores elijan y paguen
a un evaluador autorizado
para que compruebe la seguridad de la aplicación.

Los equipos que necesiten evaluaciones
de nivel 1 y 2 pueden utilizar las
[herramientas de análisis recomendadas por CASA](https://appdefensealliance.dev/casa/tier-2/tooling-matrix)
para comprobar si sus aplicaciones presentan
vulnerabilidades comunes.
¡Es sobre esto que te tenemos noticias!

**Nosotros figuramos en la lista de [**procedimientos de escaneo estático**](https://appdefensealliance.dev/casa/tier-2/ast-guide/static-scan).**
Puedes utilizar nuestra aplicación CLI
de código abierto aprobada por CASA sin costo alguno para realizar
[pruebas de seguridad de aplicaciones estáticas](../../producto/sast/)
(SAST).

## Nuestra aplicación CLIpara los escaneos de seguridad

**Machine de Fluid Attacks** es nuestra aplicación CLI
que los [desarrolladores pueden configurar](https://docs.fluidattacks.com/machine/scanner/plans/foss/)
para ejecutar análisis de código fuente
y evaluar aplicaciones web y otras superficies de ataque.
Esta aplicación realiza escaneo de vulnerabilidades
y reporta los nombres de las vulnerabilidades identificadas
(de acuerdo con el
[conjunto estandarizado](https://docs.fluidattacks.com/criteria/vulnerabilities/)
de Fluid Attacks) junto con sus IDs del CWE y su ubicación en el código fuente.
Para aprender a configurar
y utilizar nuestra herramienta CLI como escáner de vulnerabilidades,
sigue [nuestra guía](https://docs.fluidattacks.com/development/skims#using-skims).

Si un usuario del marco CASA te pide pasar el nivel de seguridad 2,
asegúrate de seguir el [proceso](https://appdefensealliance.dev/casa/tier-2/tier2-overview)
descrito por ADA.
Utiliza Machine para escanear
tu aplicación tal y como muestra
su [página web](https://appdefensealliance.dev/casa/tier-2/ast-guide/static-scan).

Se te pedirá validar tu solicitud una vez al año,
pero recuerda que durante ese tiempo
la seguridad sigue siendo un tema de preocupación.
Tienes que pensar en eso siempre,
con cada cambio en tu aplicación.
Realizando pruebas de seguridad [constantemente](../../soluciones/devsecops/),
puedes ser consciente de las vulnerabilidades más comunes y solucionarlas.
Podemos ayudarte con esto.

<div>
<cta-banner
buttontxt="Más información"
link="/es/soluciones/pruebas-seguridad/"
title="Empieza ya con la solución de Pruebas de seguridad de Fluid Attacks"
/>
</div>

## Asegura tus aplicaciones con Fluid Attacks

Ofrecemos [Hacking Continuo](../../servicios/hacking-continuo/),
que consiste en realizar pruebas de seguridad de aplicaciones
a lo largo del ciclo de vida de desarrollo de tu *software* (SDLC).
Configuramos Machine para detectar
las vulnerabilidades de tu aplicación con precisión.
Puedes ver cada hallazgo y detalles diversos,
incluyendo recomendaciones para solucionar los problemas de seguridad,
en nuestra [plataforma](../../plataforma/).
Ahí también puedes contactarnos para obtener apoyo a través de chat.

Entre los beneficios del Hacking Continuo se encuentran los siguientes:

- Asegurar cada despliegue sin retrasar su salida al mercado.
- Garantizar el cumplimiento de varios
  [estándares](https://docs.fluidattacks.com/criteria/compliance/)
  (p. ej., PCI DSS, GDPR, CCPA).
- Permitir la implementación
  de [DevSecOps en la nube](../why-is-cloud-devsecops-important/).

Puedes elegir entre [dos planes pagos](../../planes/):
Plan Machine y Plan Squad.
Plan Machine ofrece continuas
[pruebas de seguridad de aplicaciones estáticas](../../producto/sast/) (SAST),
[pruebas de seguridad de aplicaciones dinámicas](../../producto/dast/) (DAST)
y [análisis de composición de *software*](../../producto/sca/) (SCA)
solo con nuestra herramienta de escaneo.
Plan Squad incluye priorización con IA y
[pruebas de penetración manuales continuas](../../pages/soluciones/pentesting/).
Nuestro equipo de *hacking* encuentra las vulnerabilidades
que representan un mayor riesgo para las aplicaciones.
Por eso te recomendamos que vayas más allá de la automatización
y apuestes por las pruebas de seguridad realizadas
a través de la perspectiva de los atacantes.

Si quieres probar nuestras soluciones,
inicia tu [prueba gratuita de 21 días](https://app.fluidattacks.com/SignUp)
con Plan Machine y pásate a Plan Squad cuando quieras.
