---
slug: blog/diferencias-entre-sast-sca-dast/
title: ¿Cómo difieren SAST, SCA y DAST?
date: 2022-08-24
subtitle: Lo que ofrecen solos, combinados y de forma manual
category: filosofía
tags: ciberseguridad, pruebas de seguridad, software
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1661360632/blog/differences-between-sast-sca-dast/cover_differences.webp
alt: Foto por Ravi Kumar en Unsplash
description: Conoce la diferencia entre SAST, SCA y DAST y cuándo utilizar cada uno. Combínalos para realizar pruebas de seguridad exhaustivas y crear aplicaciones seguras.
keywords: Sast Vs Sca, Pruebas De Seguridad, Seguridad De Aplicaciones, Sca Y Sast, Dast Sast Sca, Codigo Fuente, Hacking Continuo, Hacking Etico, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Editor
source: https://unsplash.com/photos/sKZYPerA5s0
---

Las aplicaciones hacen girar al mundo.
¿O no es ese el dicho?
De cualquier modo,
difícilmente pasa un día sin que utilicemos
algún tipo de aplicación de *software*.
Por eso la seguridad del *software* es esencial.
Cuando se demuestra que una aplicación es insegura,
se desata el caos.

Existen diferentes tipos de pruebas de seguridad en el mercado.
Esto se debe al hecho de que lo que ve el usuario final
es sólo una parte de la aplicación,
la cual puede analizarse desde diferentes puntos de vista.

En este artículo del blog,
definiremos los tres métodos más populares utilizados
en las pruebas de seguridad de *software*:
pruebas de seguridad de aplicaciones estáticas([SAST](../../producto/sast/)),
análisis de composición de *software* ([SCA](../../producto/sca/))
y pruebas de seguridad de aplicaciones
dinámicas ([DAST](../../producto/dast/)).
Veremos sus diferencias
y hablaremos de cómo se complementan.
Asimismo,
argumentamos que alcanzan su máximo potencial
cuando se realizan mediante herramientas de pruebas de seguridad
automatizadas **y** de forma manual por parte
de personas expertas.

## ¿Cuál es la diferencia entre SAST, SCA y DAST?

SAST y SCA aparecen asociados en búsquedas,
posiblemente porque ambos se realizan mirando
el contenido interno de la aplicación estática
y no desde el exterior mientras la aplicación se está ejecutando.
Además, DAST y SAST a menudo se enfrentan entre sí.
La diferencia de nombres
(es decir, "dinámico", "estático")
suele inspirar la pregunta "¿Cuál es mejor?".
Sin embargo,
como intentaremos transmitir a lo largo de este post,
estos métodos se realizan con intenciones diferentes.
Por lo tanto,
cualquiera de ellos no es necesariamente mejor que los otros dos.
Echemos un vistazo a cada uno de ellos
por separado para que se entiendan mejor.

### ¿Qué es SAST?

Las pruebas de seguridad de aplicaciones
estáticas ([SAST](../../producto/sast/))
son un tipo de pruebas caja blanca.
Esto significa que los analistas de seguridad
y las herramientas que realizan
este método tienen acceso al código fuente,
al código de bytes o a los binarios de la aplicación.
Cuando se habla de una herramienta SAST,
se hace referencia a un programa
que encuentra automáticamente errores en el código utilizando
funciones sofisticadas
(p. ej., análisis de flujo de datos,
análisis de flujo de control,
reconocimiento de patrones).
Los encuentra porque coinciden con errores conocidos
que tiene almacenados en una base de datos.

No es un secreto
que las herramientas comerciales de
pruebas de seguridad de aplicaciones estáticas generan reportes
que contienen altas tasas de falsos positivos.
Por eso siempre es necesaria la verificación humana.
Los expertos se encargan de revisar los resultados
para determinar si se trata de problemas reales.
Así pues,
el despliegue de herramientas SAST debe realizarse
junto con el trabajo manual.
El SAST manual lo llevan a cabo evaluadores
de seguridad que comprenden el contexto
de la aplicación y encuentran problemas
de seguridad en el código fuente que la herramienta
no ha podido detectar
(es decir, falsos negativos).
En un [artículo anterior del blog](../../../blog/sastisfying-app-security/)
se explica más detalladamente
por cuáles etapas pasa.
Los expertos están al día en materia de vulnerabilidades
gracias a su trabajo diario
y al contacto con recursos
como el Open Web Application Security Project
(OWASP) y el Common Weakness Ennumeration (CWE).
La combinación de pruebas de seguridad automáticas
y manuales continuas genera resultados más precisos.

### ¿Por qué es importante SAST?

Es muy importante examinar el código fuente
realizando SAST manualmente
junto con herramientas de pruebas de seguridad automatizadas.
Para que te hagas una mejor idea,
nuestro [State of Attacks 2022](https://try.fluidattacks.tech/state-of-attacks-2022/)
muestra que
"[la información confidencial no cifrada](https://docs.fluidattacks.com/criteria/vulnerabilities/247/)"
y "[la información sensible en el código fuente](https://docs.fluidattacks.com/criteria/vulnerabilities/009/)"
se encuentran entre los cinco tipos de vulnerabilidades
que más riesgo suponen para los sistemas
que Fluid Attacks evaluó en 2021.

### ¿Cuáles son los beneficios de SAST?

Las siguientes son algunas de las ventajas más notables
de las pruebas de seguridad estáticas de las aplicaciones:

- Puede realizarse de forma continua,
  temprana y a lo largo de todo
  el ciclo de vida de desarrollo de *software* (SDLC).

- Te permite conocer la ubicación exacta de una vulnerabilidad,
  como el nombre del archivo y el número de línea.

- Como este método te informa de las vulnerabilidades
  poco después de que se hayan escrito,
  la corrección puede llevarse a cabo con la misma rapidez.

- Cuanto antes se remedie, más te ahorras.

- Cuando se realiza manualmente en combinación con herramientas SAST,
  arroja resultados con bajas tasas de falsos positivos
  y falsos negativos.

### ¿Qué es SCA?

El análisis de la composición de *software* ([SCA](../../producto/sca/))
te permite inventariar tus componentes de código abierto.
Al conocer sus versiones,
puedes comprobar cuáles están actualizados.
Y al conocer las licencias de los componentes,
puedes cambiar a otros componentes
que hagan cosas similares pero que tengan
licencias compatibles con las políticas
de tu organización para evitar riesgos legales.
Además,
tanto manualmente como con la ayuda de herramientas de SCA,
este método apunta a aquellos componentes
que tienen vulnerabilidades que aparecen en bases de datos públicas
o que han sido reveladas por evaluadores de seguridad,
investigadores o los propios vendedores.

### ¿Por qué es importante la SCA?

Identificar el riesgo relacionado
con las dependencias vulnerables de *software*
de código abierto es una prioridad absoluta.
Has oído hablar de [Log4Shell](../../../blog/log4shell/).
¿Cómo no?
A día de hoy sigue siendo un gran lío.
Los atacantes siguen explotando vulnerabilidades
en Log4j porque una multitud
(tal vez millones, pero ¿quién sabe?)
de aplicaciones lo utilizan para el registro.
Sigue siendo noticia porque la gente no reconoce
que lo utiliza en su *software* y,
por tanto,
está expuesta a ataques de ejecución remota de código y de malware,
entre otros.

Log4j es sólo uno de nuestros problemas.
Nuestro [State of Attacks de 2022](https://try.fluidattacks.tech/state-of-attacks-2022/)
muestra que
el "[Uso de *software* con vulnerabilidades conocidas](https://docs.fluidattacks.com/criteria/vulnerabilities/011/)"
es el tipo de vulnerabilidad que generó
la mayor exposición al riesgo y también estuvo presente
en la mayoría de los sistemas
Fluid Attacks evaluados durante 2021.

Pero no nos malinterpretes.
No creemos que el código abierto sea malo.
De hecho,
recomendamos compartir abiertamente tu código fuente,
siempre y cuando te asegures de probarlo constantemente
contra vulnerabilidades.
La importancia de la seguridad del código abierto se debe,
al menos en parte,
a que facilita el desarrollo de *software*.
[Alrededor de 80%](../../../blog/stand-shoulders-giants/)
del código de las aplicaciones
procede de dependencias de código abierto
y el resto es código propietario.
La forma en que se utilizan estas bibliotecas
para poder crear algo nuevo se ajusta al curso estándar
de la evolución de la cultura humana.
Ya lo hemos dicho antes:
estamos de pie sobre hombros de gigantes.

### ¿Cuáles son las ventajas de SCA?

Entre las ventajas más destacables del análisis de composición de *software*
se encuentran las siguientes:

- Puede realizarse de forma continua,
  al principio y a lo largo de todo el SDLC.

- Permite elaborar una lista de materiales de *software* (SBOM;
  es decir,
  un documento que indica qué dependencias de *software*
  se están utilizando).

- Ayuda a identificar el riesgo de la cadena
  de suministro de *software* determinado
  por factores de calidad de los componentes,
  como la licencia, la versión y las vulnerabilidades.

- Cuando se realiza manualmente en combinación con herramientas de SCA,
  arroja resultados con bajas tasas
  de falsos positivos y falsos negativos.

<div>
<cta-banner
buttontxt="Más información"
link="/es/soluciones/pruebas-seguridad/"
title="Empieza ya con la solución de Pruebas de seguridad de Fluid Attacks"
/>
</div>

### ¿Qué es DAST?

Las pruebas de seguridad de aplicaciones dinámicas ([DAST](../../producto/dast/))
son un método para evaluar aplicaciones en ejecución.
Es decir,
estas aplicaciones ya están en un servidor web,
una máquina virtual o un contenedor y funcionando.
A diferencia de SAST,
DAST no requiere acceso al código fuente,
sino que evalúa el comportamiento de la aplicación
desde el lado del usuario, por así decirlo.
Como se realiza sin ver el código fuente,
es un tipo de prueba caja negra.

Las pruebas de seguridad de aplicaciones dinámicas
consisten en enviar vectores de ataque
(p. ej., cadenas de código)
a los extremos de la aplicación
para inspeccionar comportamientos inesperados.
Así,
por ejemplo,
si una aplicación no descarta correctamente las entradas no seguras,
es vulnerable a ataques de inyección
(p. ej., [inyección SQL](../../../blog/sql-injection)).
Estos ataques pueden permitir
a los delincuentes obtener información confidencial
o lograr la ejecución remota de código.
Por lo tanto,
DAST puede ayudar a identificar este tipo
de riesgos mucho antes de que la aplicación
esté siquiera en manos de los usuarios finales.

Una limitación de las pruebas de seguridad de aplicaciones dinámicas
es que no pueden señalar dónde residen exactamente
las vulnerabilidades en el código fuente.
Además,
como limitación compartida con las pruebas
de seguridad de aplicaciones estáticas
y el análisis de composición de *software*,
cuando se realizan solo con herramientas,
pueden producir reportes con altas tasas de falsos positivos
y pasar por alto vulnerabilidades reales.
Pero la forma de superar los falsos positivos
y los falsos negativos es combinar
el uso de herramientas DAST con el trabajo manual.
Cuando DAST se hace manualmente,
la superficie de ataque
puede ser definida con mayor precisión,
y los ataques pueden ser especialmente elaborados
y actualizados sobre las técnicas utilizadas
por los actores de amenazas.

### ¿Por qué es importante DAST?

Frecuentemente publicamos [avisos](../../../advisories/)
de *software* vulnerable a *cross-site scripting*,
*cross-site request forgery* e inyección,
entre otros problemas de seguridad.
Como nuestro equipo de investigación puede atestiguar
un atacante no necesita tener acceso al código fuente
para aprender a causar un gran daño.
Solo necesitan escudriñar las aplicaciones probando formas creativas
de obtener acceso no autorizado.
Esta es la razón por la que DAST debe llevarse a cabo constantemente.
Al atacar proactivamente su propia aplicación desde el exterior,
las organizaciones pueden encontrar problemas antes
de que lo hagan los delincuentes.
Entonces los desarrolladores pueden arreglar la aplicación desde dentro,
reduciendo eficazmente los riesgos.

### ¿Cuáles son las ventajas de DAST?

Algunas de las ventajas más notables de las pruebas
de seguridad de aplicaciones dinámicas son las siguientes:

- Puede realizarse de forma continua,
  temprana y a lo largo de todo el SDLC.

- Ayuda a identificar vulnerabilidades
  causadas por la interacción con la aplicación.

- Permite simular ataques de *hackers* malintencionados.

- Cuando se realiza manualmente en combinación
  con las herramientas DAST,
  los ataques pueden ser personalizados y más ingeniosos,
  produciendo resultados con bajas tasas
  de falsos positivos y falsos negativos.

### ¿SAST vs SCA vs DAST?

Después de todas estas definiciones,
¿qué se puede decir sobre la validez de comparaciones
comunes como SAST vs SCA y SAST vs DAST?
¿Cuál es la mejor?
Es evidente que SAST, DAST y SCA
se ejecutan con diferentes alcances
dentro del mismo objeto de evaluación.
Cada uno de ellos beneficia a la seguridad del *software*
a su manera y ofrece sus propias ventajas.
Así que,
si nos preguntas si alguno de estos métodos
es mejor que los otros dos,
te responderemos con otra pregunta:
¿Qué quieres lograr?

Si tu respuesta es algo así como
"sólo quiero saber cuál protegerá mi *software* de forma más eficaz",
te recomendamos que te des cuenta
y reflexiones sobre la importancia de las pruebas exhaustivas.
Es decir,
hay que eliminar las vulnerabilidades del código fuente,
gestionar el riesgo del código abierto
**y** evaluar continuamente la aplicación adoptando
la postura de un atacante.

## Combinar SAST, SCA y DAST para pruebas exhaustivas

Cuando adoptas un enfoque combinado de pruebas de seguridad,
estás ampliando tu alcance
y tienes más posibilidades de identificar la exposición
al riesgo con mayor precisión.
Además,
te instamos a que apliques SAST, DAST y SCA
de forma continua en todo el SDLC,
incorpóralos lo antes posible y combina el trabajo manual
con las pruebas automatizadas a lo largo de todo el proceso.
La idea es mantener una práctica
de remediación rigurosa a lo largo de todo el desarrollo,
en la que cada vulnerabilidad se detecte
y se aborde con prontitud.
La adopción de pruebas integrales demostrará
ser útil en la construcción
de una cultura [DevSecOps](../concepto-devsecops/)
en tu organización.

## Aprovecha las pruebas de seguridad integrales de Fluid Attacks

En Fluid Attacks,
ofrecemos [SAST](../../producto/sast/),
[SCA](../../producto/sca/)
y [DAST](../../producto/dast/)
a lo largo de todo el SDLC,
todo en una única solución:
[Hacking Continuo](../../servicios/hacking-continuo/).
Nuestro [equipo de *hacking*](../../../certifications/)
[altamente certificado](../../../blog/what-is-ethical-hacking/)
trabaja continuamente junto con las herramientas
de pruebas de seguridad para detectar
todas las vulnerabilidades de las aplicaciones evaluadas.
Ampliamos constantemente los tipos de vulnerabilidades
que las herramientas son capaces de detectar,
generando informes exhaustivos con tasas mínimas
de falsos positivos y aumentando la eficacia de nuestros expertos.
En el proceso,
te ayudamos a cumplir [varios estándares de seguridad](https://docs.fluidattacks.com/criteria/compliance/)
y a [reducir los costos de remediación](https://try.fluidattacks.tech/us/ebook/)
hasta en un 90%.

Pulsa [aquí](https://app.fluidattacks.com/SignUp)
para conocer la **prueba gratuita de 21 días**
de nuestro Plan Machine de Hacking Continuo,
el cual te permite probar nuestras pruebas de seguridad automatizadas,
o pregúntanos ahora por nuestro [Plan Squad](../../planes/)
para añadir *hackers* éticos a la mezcla.
Para obtener más información,
¡[contáctanos](../../contactanos/)\!
