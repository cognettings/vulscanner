FROM myimage@hash-256
USER fluiduser
COPY *.jar app.jar
ENV JAVA_OPTS="-XX:+UseContainerSupport -Dcom.sun.management.jmxremote.ssl=false"
ENTRYPOINT [ "sh", "-c", "java -jar app.jar" ]
