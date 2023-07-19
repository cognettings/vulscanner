---
slug: blog/escaneo-vulnerabilidad-aplicacion-web/
title: Blinda tus aplicaciones y sitio web
date: 2023-03-02
subtitle: Escaneo de vulnerabilidades y pentesting para la web
category: filosofía
tags: ciberseguridad, pruebas de seguridad, software, pentesting, empresa
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1677776400/blog/web-app-vulnerability-scanning/cover_scanning.webp
alt: Foto por Tamas Kolossa en Unsplash
description: Aprende cómo funciona el escaneo de seguridad de aplicaciones y sitios web, su papel en la gestión de vulnerabilidades y las razones para combinarlos con el pentesting en la evaluación de vulnerabilidades.
keywords: Escaneo Sitio Web, Escaner De Seguridad Sitio Web, Escaner De Aplicaciones Web, Comprobar Vulnerabilidades En Sitio Web, Escaner De Aplicaciones Web Gratis, Escaner De Vulnerabilidades Sitio Web, Escaneo De Vulnerabilidades Vs Pruebas De Penetracion, Hacking Etico, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Editor
source: https://unsplash.com/photos/cirko7YwU_w
---

Alrededor del [64,4% de la población mundial](https://datareportal.com/global-digital-overview)
utiliza Internet,
cifra que va en aumento,
por lo cual las organizaciones tienen
un gran incentivo para digitalizarse.
Crear un sitio web o una aplicación web
es una buena manera de llegar a un mayor número de usuarios.
En consecuencia,
estas empresas se convierten en responsables
de proteger los datos de ese público.
Sus nuevos activos expuestos al público
son vectores de ataque para los ciberdelincuentes
que buscan beneficiarse de los problemas derivados
de errores cometidos en ellos.
Los desarrolladores de sitios web y aplicaciones web
recurren a [prácticas de codificación seguras](../../../blog/secure-coding-practices/)
y [evaluación de vulnerabilidades](../evaluacion-de-vulnerabilidades/)
para reducir los puntos débiles de su código fuente.
En este artículo del blog,
explicamos cómo funciona el escaneo de seguridad
de sitios web y el escaneo de seguridad de aplicaciones web,
su papel en la gestión de vulnerabilidades
y la necesidad de combinarlos con evaluaciones más complejas.

## Análisis de vulnerabilidades en apps y sitios web

Las vulnerabilidades en aplicaciones y sitios web
pueden representar más o menos riesgo en función
de la cantidad de información sensible que gestionen.
De hecho,
los sitios web completamente estáticos,
por ejemplo,
cuyo contenido es invariable
puesto que los usuarios no pueden interactuar
con las páginas para obtener respuestas como descargas,
chats o pagos,
tienen más probabilidades de ser seguras.
Las aplicaciones web,
en cambio, tienen varios elementos
(p. ej., bases de datos)
en su back-end que trabajan para generar respuestas
a las peticiones de los usuarios.
Por consiguiente,
hay más posibilidades de que se produzcan debilidades
(probablemente, las más comunes las hayas visto en
el [Top 10 de OWASP](../../../blog/owasp-top-10-2021/)).
Y por lo tanto,
hay más vías de entrada para un atacante.

Sin embargo,
muchos sitios web han integrado algún tipo de interacción.
Incluso los simples formularios de un sitio web estático
que desencadenan acciones para guardar la información
de respuesta en una plataforma diferente
pueden ser vulnerables
(p. ej., [almacenar en caché los datos](https://docs.fluidattacks.com/criteria/vulnerabilities/065/)).
Así pues,
también es necesario escanear los sitios web
para comprobar sus vulnerabilidades.
Una forma básica y automatizada de realizar un chequeo
de seguridad de un sitio web
es mediante el uso de escáneres de vulnerabilidades
de sitios web
o herramientas de escaneo de vulnerabilidades.

En un [artículo anterior](../escaneo-de-vulnerabilidades/)
hemos explicado qué es el análisis de vulnerabilidades.
Básicamente,
es el proceso por el que un dispositivo,
programa informático o herramienta de pruebas identifica
y reporta automáticamente los puntos débiles de los sistemas.
En este sentido,
es una forma de evaluación de vulnerabilidades que,
a su vez,
es una práctica necesaria dentro de un programa
de gestión de vulnerabilidades.

A la hora de decidirse por un escáner,
hay muchas alternativas para elegir,
desde escáneres gratuitos de aplicaciones web
hasta servicios pagados.
Por ejemplo,
existen opciones para comprobar la seguridad
de los sitios web en línea,
así como listados de herramientas útiles
para la evaluación de vulnerabilidades
(p. ej., la evaluación de [OWASP](https://owasp.org/www-community/Source_Code_Analysis_Tools)).

Un escaneo de sitios web
o de vulnerabilidades se realiza revisando los componentes
y configuraciones de los objetivos predefinidos
de la evaluación,
comparándolos con las características del código vulnerable.
Dichas características son definidas en los escáneres
de vulnerabilidades de seguridad por los desarrolladores
que contribuyen a su mejora.
Para una mejor comprensión de este proceso,
compartimos cómo nuestros desarrolladores
de seguridad mejoran nuestro escáner llamado
[Machine](../../../blog/casa-approved-static-scanning/).

Inicialmente,
nuestro equipo percibe la necesidad
de integrar un nuevo método que permita
a Machine encontrar una vulnerabilidad determinada.
Un candidato sería,
por ejemplo,
una nueva entrada
en el [Common Weakness Enumeration](https://cwe.mitre.org/) (CWE)
o en el [Common Vulnerabilities and Exposures](https://cve.mitre.org/) (CVE).
Podría tratarse de una funcionalidad
que no debería estar presente en producción.
Nuestros desarrolladores de seguridad empiezan
a investigarla para definir cómo la herramienta
encontrará esa funcionalidad
en los códigos fuente de nuestros clientes.
Una forma posible es utilizar una biblioteca
Python para dividir el código en fragmentos
y crear un árbol para luego encontrar los parámetros
de los que depende la funcionalidad.
Luego,
los desarrolladores pueden escribir funciones
que contengan lo aprendido
y que conduzcan a la detección
y reporte de esa funcionalidad.
Tras integrar el método a Machine,
la herramienta puede encontrar automáticamente
la vulnerabilidad en el código fuente.
La creación de métodos para mejorar la herramienta
es una actividad constante en Fluid Attacks.

Machine puede comprobar el cumplimiento
de los requisitos de seguridad más críticos
para las aplicaciones web.
Estos incluyen, entre muchos otros,
los siguientes:

- [Verificar que los componentes de terceros son seguros](https://docs.fluidattacks.com/criteria/requirements/262),
  lo que ayuda a protegerse contra el uso
  de *software* con vulnerabilidades conocidas.

- [Descartar entradas no seguras](https://docs.fluidattacks.com/criteria/requirements/173)
  e [incluir encabezados de seguridad HTTP](https://docs.fluidattacks.com/criteria/requirements/349),
  que ayudan a protegerse contra ataques de inyección
  y de secuencias de comandos en sitios cruzados (XSS).

- [Utilizar mecanismos preexistentes y actualizados](https://docs.fluidattacks.com/criteria/requirements/147)
  para implementar funciones criptográficas,
  lo que ayuda a protegerse contra fallas criptográficas.

- [Definir usuarios que tengan privilegios](https://docs.fluidattacks.com/criteria/requirements/147),
  lo que ayuda a protegerse contra las fallas en el control de acceso.

- [Exigir contraseñas](https://docs.fluidattacks.com/criteria/requirements/133/)
  y [frases de contraseña largas](https://docs.fluidattacks.com/criteria/requirements/132/),
  lo que ayuda a protegerse contra fallas de identificación y autenticación.

- [Controlar los redireccionamientos](https://docs.fluidattacks.com/criteria/requirements/324/)
  para que conduzcan a sitios de confianza,
  lo que ayuda a protegerse contra
  los falsificadores de peticiones en el servidor (SSRF).

<div>
<cta-banner
buttontxt="Más información"
link="/es/soluciones/gestion-vulnerabilidades/"
title="Empieza ya con la solución de Gestión de vulnerabilidades
de Fluid Attacks"
/>
</div>

Para validar ciertos requisitos,
la evaluación de la vulnerabilidad
de las aplicaciones web con herramientas
utiliza metodologías distintas a
las [pruebas de seguridad de aplicaciones estáticas](../../producto/sast/)
(SAST).
En algunos casos,
la protagonista es
la [prueba de seguridad de aplicaciones dinámica](../../producto/dast/) (DAST).
Busca puntos débiles en ambientes,
terminales,
servidores y configuraciones de servicios en la nube.
Esto implica la interacción con la aplicación en ejecución,
algo que también consigue Machine.

Además,
sería necesario otro método para encontrar otro tipo de problemas.
El [análisis de composición de *software*](../../producto/sca/) (SCA),
entre otras capacidades,
encuentra componentes y dependencias de código abierto vulnerables
que se utilizan en la aplicación web
para no reinventar la rueda.
Sin embargo,
cuando esta rueda está defectuosa, es hora de sustituirla.

El problema que supone utilizar *software* de código abierto
con vulnerabilidades conocidas
es tan generalizado que lo hemos situado
en primer lugar en la lista anterior,
aunque el resto sigue un orden correspondiente
a los riesgos del Top 10 de OWASP.
Nuestro [State of Attacks 2022](https://try.fluidattacks.tech/state-of-attacks-2022/)
muestra que esta era la vulnerabilidad que representa
la mayor exposición al riesgo de los sistemas de nuestros clientes.
Para encontrar estos casos de componentes vulnerables,
nos basamos en gran medida en el SCA
de nuestra herramienta automatizada.

Sin embargo,
hay que tener en cuenta que los escáneres
de vulnerabilidades de aplicaciones
y sitios web no pueden encontrar todos los problemas de seguridad.
Las [pruebas de *pentesting*](../../../blog/what-is-manual-penetration-testing/)
son necesarias para una evaluación completa de la vulnerabilidad.

## ¿Escaneo de vulnerabilidades de apps web vs *pentesting*?

Si leíste un [artículo anterior](../../../blog/account-takeover-kayak/)
sobre una vulnerabilidad
que uno de nuestros investigadores de seguridad encontró en KAYAK,
te habrás dado cuenta de que los *hackers* éticos
a menudo encuentran una vulnerabilidad
y van un poco más allá.
En su evaluación,
encuentran aún más problemas que,
vinculados a la vulnerabilidad inicial,
pueden aprovecharse para lanzar un ataque con un impacto mayor
del que se conseguiría aprovechando únicamente
la primera detección.

No se espera este tipo de comportamiento
de los escáneres de sitios y aplicaciones web.
De hecho,
las debilidades de seguridad se les escapan
a las herramientas si la detección de las primeras requiere
que un usuario externo haga cosas complejas en el sistema.
La respuesta a este problema son las pruebas de *pentesting*,
que son,
al igual que el escaneo de vulnerabilidades,
un tipo de evaluación de las mismas.

El trabajo de los *hackers* éticos,
o *pentesters*,
ayuda a encontrar problemas complejos
(a menudo de mayor gravedad que los detectados por las herramientas)
y a veces incluso vulnerabilidades desconocidas.
El *pentesting* es valioso,
ya que simula ciberataques del "mundo real"
y puede ofrecer demostraciones del impacto de la explotación
de los problemas detectados.
Además,
dado que las herramientas pueden equivocarse,
las evaluaciones manuales de seguridad que verifican
sus reportes pueden reducir las tasas
de falsos positivos en el reporte general.

La relación entre *hacking* y escaneo es de complemento.
Los *hackers* pueden sin duda utilizar
los escáneres de seguridad de sitios web
(p. ej., [Burp Scanner](https://portswigger.net/burp/documentation/scanner),
[ffuf](https://github.com/ffuf/ffuf),
[Nuclei](https://github.com/projectdiscovery/nuclei),
[Vega](https://subgraph.com/vega/))
para ganar tiempo en la búsqueda de las debilidades que mejor se ocultan.
Esta combinación,
cuando se realiza de forma continua a lo largo del desarrollo de la aplicación,
arroja conocimientos precisos
y actualizados para la gestión de vulnerabilidades.

## ¡Y no olvides priorizar y remediar!

Más allá de aprender la diferencia entre
el escaneo de vulnerabilidades y el *pentesting*,
queremos que entiendas que ambos se benefician de la identificación,
clasificación y reporte de problemas de seguridad,
lo cual es seguido por la priorización
y remediación de los mismos.
De hecho,
todos estos procesos forman parte de la gestión de vulnerabilidades.

Como [dijimos antes](../evaluacion-de-vulnerabilidades/),
es posible que prefieras abordar primero
los problemas que representen un mayor riesgo.
Además,
la remediación debería ser algo sobre lo que nunca deberías dejar de pensar.
Como las amenazas a tu organización son permanentes
y están en constante evolución,
será mejor que trabajes en la integración de la seguridad
en todo el ciclo de vida de desarrollo de *software* (SDLC),
al estilo [DevSecOps](../concepto-devsecops/).

Toma algunos pasos pequeños
y prueba el escaneo de vulnerabilidades con nuestro Machine:
nuestro escáner de vulnerabilidades en línea gratuito
y de código abierto,
no solo figura en la lista
de [herramientas de análisis de código fuente de OWASP](https://owasp.org/www-community/Source_Code_Analysis_Tools)
sino que también es una [herramienta SAST](../escaneo-estatico-aprobado-por-casa/)
[recomendada por la App Defense Alliance de Google y otros](https://appdefensealliance.dev/casa/tier-2/tooling-matrix).

Además,
te permitimos mejorar tu gestión de vulnerabilidades.
Puedes disfrutar de nuestra solución
de [Gestión de Vulnerabilidades](../../soluciones/gestion-vulnerabilidades/)
en cualquiera de nuestros
dos [planes](../../planes/).
Nuestro plan Machine de Hacking Continuo
se vale de nuestra herramienta automatizada
para encontrar vulnerabilidades
(con SAST, DAST y SCA)
y viene con acceso a nuestra [plataforma](../../plataforma/),
donde puedes conocer los resultados de las pruebas de seguridad,
asignar remediaciones a los miembros de tu equipo de desarrollo,
rastrear la exposición al riesgo y mucho más.
(**Obtén tu prueba gratuita** [**aquí**](https://app.fluidattacks.com/SignUp))
Nuestro Plan Squad de Hacking Continuo,
más completo,
añade a lo anterior: *pentesting* por parte de nuestro equipo
de *hacking* y su apoyo experto a través
de la plataforma en lo que respecta a la remediación.
