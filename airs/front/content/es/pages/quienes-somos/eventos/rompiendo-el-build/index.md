---
slug: quienes-somos/eventos/rompiendo-el-build/
title: Rompiendo el build
subtitle: Nuestros hábitos DevSecOps
category: eventos
description: En el taller Rompiendo el build presentamos los hábitos DevSecOps de Fluid Attacks. Estos van orientados a objetivos específicos, que también pueden ser aplicados en tu empresa repetibilidad, feedback preciso, y generación de valor diario.
keywords: Fluid Attacks, DevSecOps, Habitos, Romper El Build, CI-CD, Conferencia, Pentesting, Hacking Etico
eventspage: yes
banner: events-bg
---

## 1\. Objetivo

El concepto **DevSecOps**
ha ganado popularidad en los últimos años.
Sin embargo,
los webinarios que tratan este tema tienden
a centrarse solo en sus herramientas, beneficios,
o posibles escenarios de uso.
Muchos oradores demuestran
cómo realizar pruebas en un ambiente extremadamente sencillo,
totalmente ajeno a nuestras tareas cotidianas,
y, en este caso,
surgen nuevas preguntas como
**“¿esto sí funciona?”**
o
**“¿cómo puedo aplicar esto a mi empresa?”**
Estos webinarios proveen información básica,
que, aunque útil,
no responden el **cómo funciona o por dónde empezar**,
detalles, que podemos afirmar con certeza,
los asistentes también quieren saber.

Con base en lo anterior,
en esta charla buscamos responder
las preguntas planteadas compartiendo
las metodologías y prácticas de trabajo,
o **hábitos**,
que nos permiten implementar una cultura DevSecOps
en la ejecución de nuestros proyectos;
desde la gestión de la infraestructura
hasta el desarrollo de nuestra plataforma de gestión
y remediación de vulnerabilidades.

Estos hábitos nos permiten
no solo aumentar nuestra productividad
y generar valor para nuestros clientes en el día a día,
sino también aumentar la seguridad
de nuestros despliegues a producción.
Así,
conseguimos alcanzar en promedio las siguientes tasas:

<div class="avarage-rates-section">
<a href="https://gitlab.com/fluidattacks/universe/-/merge_requests?scope=all&state=merged"
target="_blank">
<div class="fl w-100 w-50-l pa2">
<div class="outline-transparent bg-button-red hv-bg-fluid-rd pointer white pv3
fw7 f3 t-all-3-eio br2 bc-fluid-red ba poppins tc">
<div>Frecuencia de despliegue a producción</div>
<div>70 al día</div>
</div>
</div>
</a>
<a href="https://gitlab.com/fluidattacks/universe/-/merge_requests?scope=all&state=merged&search=%22rever%22"
target="_blank">
<div class="fl w-100 w-50-l pa2">
<div class="outline-transparent bg-button-red hv-bg-fluid-rd pointer white pv3
fw7 f3 t-all-3-eio br2 bc-fluid-red ba poppins tc">
<div>Despliegues exitosos</div>
<div>99.99%</div>
</div>
</div>
</a>
</div>

## 2\. Contenido

Con este **seminario/taller**
buscamos que se entiendan completamente los problemas por resolver
(p. ej., el desarrollo tradicional, cascada, tecnología legada, etc.),
conversar sobre las buenas prácticas DevSecOps
que se constituyen en pruebas de seguridad continuas,
las cuales generan equipos responsabilizados y apoderados
de la seguridad de sus aplicaciones,
contribuyendo al valor diario con despliegues constantes,
y también revisar esos hábitos en una demostración real y auténtica.

Todo se realiza **en vivo** usando infraestructuras
y aplicaciones reales,
dando a la audiencia un vistazo detrás de cámaras del proceso:
Las herramientas que usamos,
los *logs* que nos permiten identificar problemas,
e incluso el código fuente que define cada paso
para el despliegue correcto de nuestras aplicaciones,
siempre enfocándonos en cómo se actualizan nuestra infraestructura
y nuestros productos en **tiempo real**.

Para ayudar a entender cómo se desarrolla todo
y demostrar cómo dar el primer paso
para llegar a esta configuración,
también explicamos todos los hábitos de trabajo
que nos han permitido llegar hasta aquí
y seguir mejorando día a día.
Entre ellos se incluyen temas como:

- Hackeo continuo de los sistemas
  para garantizar la integración de la parte de seguridad en el SDLC.

- Gestión del código fuente dentro de los repositorios,
  siguiendo una estructura **monorepo**
  (decir adiós al multirepo).

- Mantener un entorno limpio
  y reducido para los desarrolladores,
  incluyendo los cambios en la rama principal,
  evitando la acumulación de código
  y llegando a **inventario cero**
  (dejando atrás Gitflow).

- Generar valor diario a los clientes
  a través de una metodología de **microcambios**
  (en lugar de cambios grandes cada 3 semanas o más).

- Migrar y gestionar toda la infraestructura
  como código fuente versionado,
  convirtiéndola en **infraestructura inmutable**
  (evitando consolas de gestión y cambios no autorizados).

- Definir entornos de integración continua como código fuente,
  *pipeline* como código,
  de una forma que pueda configurarse
  y modificarse fácilmente para todo tipo de pruebas
  (evitando limitaciones de interfaz gráfica
  para configuraciones de *pipeline*).

- Evitar servidores a toda costa,
  migrando a servicios en la nube
  y logrando una infraestructura **sin servidores**.

- Gestión segura de contraseñas al desplegar una aplicación,
  evitando la exposición de información sensible
  en el código fuente
  y **manteniendo protegidos los secretos**.

- Desplegar **entornos efímeros** que permitan probar
  todas las funcionalidades desarrolladas
  antes de pasar a producción
  (reduciendo la complejidad del proyecto
  al evitar entornos de desarrollo, pruebas, QA y otros).

- **Romper el *build*** incluso antes de hacer un *commit*
  al repositorio utilizando localmente pruebas de integración
  reproducibles  para revisar el código fuente.

- Realizar pruebas en el código fuente
  y en el despliegue que **rompan el *build***
  como resultado del más mínimo error
  (en lugar de solo notificar y permitir que
  el error persista e incluso evolucione):

    - Pruebas unitarias

    - Pruebas funcionales

    - Cobertura

    - *Linters* estrictos

    - Puertas de seguridad (SAST y DAST)

    - E2E

- Reducción extrema de los tiempos de desarrollo
  mediante el uso correcto de la **caché**.

- Aprovechar las características que presenta
  el cliente de control de versiones Git:

    - Peer review

    - Squashing

    - Rebasing

    - Rollback

    - Trigger builds

- **Telemetría** accesible para desarrolladores
  (no *logs*, solo disponible para el área de infraestructura).

Cada uno de los puntos mencionados se explica
mientras se accede a los sistemas de Fluid Attacks
para ver su implementación y funcionamiento.
Según las necesidades o el interés de los participantes,
es posible centrarse en los temas que consideren más importantes.

## 3\. Experiencia

Este **taller** ha sido presentado a profesionales
en áreas de tecnología y auditoría para empresas
como:
[Accenture](https://www.accenture.com/co-es/new-applied-now),
[Arus](https://www.arus.com.co/),
[ATH](https://www.ath.com.co/wps/themes/html/ath/index.html),
[Avianca](https://www.avianca.com/co/es/),
[B89](https://www.b89.io/),
[Bancolombia](https://www.grupobancolombia.com/wps/portal/personas),
[Banitsmo](https://www.banistmo.com/),
[BIVA](https://www.biva.mx/en/web/portal-biva/home),
[Cadena](https://www.cadena.com.co/),
[Cidenet](http://cidenet.com.co/),
[Colpatria](https://www.colpatria.com/),
[Cognox](http://www.cognox.co),
[Coordiutil](https://www.vendesfacil.com/),
[Corona](https://www.corona.co/),
[EAFIT](http://www.eafit.edu.co/),
[Evendi Digital](https://evendidigital.com/),
[F2X](https://www.f2x.com.co/),
[GCO](http://www.gco.com.co/),
[Grupo AVAL](https://www.grupoaval.com/wps/portal/grupo-aval/aval/),
[Grupo Éxito](https://www.grupoexito.com.co/es/),
[Interbank](https://interbank.pe/),
[Komet Sales](https://www.kometsales.com/),
[Nutresa](https://gruponutresa.com/),
[Payválida](https://www.payvalida.com/),
[Protección](https://www.proteccion.com/wps/portal/proteccion/),
[RUNT](https://www.runt.com.co/),
[Seti](https://seti.com.co/),
[Banco Pichincha](https://www.bancopichincha.com.co/web/personas),
[Soy Yo](https://www.soyyo.co/),
[BTG Pactual](https://www.btgpactual.com.co/),
[Caja Cusco](http://www.cmac-cusco.com.pe/),
[Banco Azul](https://www.bancoazul.com/),
[Sistecrédito](https://www.sistecredito.com/),
[Banco Agromercantil](https://www.bam.com.gt/),
[Bantrab](https://www.bantrab.com.gt/),
[Telered](https://www.telered.com.pa/),
[Virtualsoft](https://virtualsoftlatam.com/),
[Linea Directa](https://www.lineadirecta.com.co/),
[OxxO](https://www.oxxo.com/),
[Chubb](https://www.chubb.com/co-es/),
[Banco Bolivariano](https://www.bolivariano.com/),
[ACH](https://www.achcolombia.com.co/home),
[Sodexo](https://www.sodexo.co/),
[Mutualser](https://www.mutualser.com/),
[Niubiz](https://www.niubiz.com.pe/),
[Nequi](https://www.nequi.com.co/),
[La Haus](https://www.lahaus.com/),
[Banco General Panamá](https://www.bgeneral.com/),
[Yappy](https://www.bgeneral.com/yappy/),
[MFTech](https://www.mftech.io/),
[Banco Industrial](https://www.corporacionbi.com/gt/bancoindustrial/)
y [Tech and Solve](http://www.techandsolve.com/).

## 4\. Lugar de encuentro

El taller se realiza en un lugar externo.
No organizamos talleres en las oficinas de las empresas participantes.

## 5\. Duración

El **taller** tiene una duración
de **6 horas** (no es posible reducir su duración).
Comprende una demostración en directo de nuestras prácticas,
una pausa por la mañana
y una pausa para el almuerzo.

## 6\. Fecha

El **taller** está diseñado
para realizarse de **9 a. m.** a **3 p. m.**,
con un descanso de **30 minutos** para almorzar.
La fecha del evento debe programarse
de mutuo acuerdo entre los participantes
y Fluid Attacks.

## 7\. Inversión

El espacio y la comida para este taller
están completamente cubiertos por Fluid Attacks.
Los asistentes deberán comprometerse con su tiempo
y cubrir sus gastos de transporte,
incluidos los gastos de parqueo de vehículos
en caso de que las instalaciones excedan su capacidad.

## 8\. Materiales

Como en todos los eventos ofrecidos por Fluid Attacks,
el material del evento se envía a los asistentes una vez completen
la [encuesta de satisfacción en línea](https://fluidattacks.formstack.com/forms/talk?Content=Breaking%20the%20build&Speaker=Juan%20Restrepo&Virtual=No).

## 9\. Audiencia

El **taller** es adecuado tanto para personal técnico como directivo,
y la tasa de satisfacción
para ambos perfiles es igualmente alta.
Sin embargo,
si quieres promover nuevos cambios
y experimentación en tu empresa,
es importante incluir a personas que puedan tomar decisiones
dentro del equipo.

El **taller** está diseñado
para un público de entre **14 y 22** personas
por parte del cliente,
más 4 participantes adicionales
por parte de Fluid Attacks.
