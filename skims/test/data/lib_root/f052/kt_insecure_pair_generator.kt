

val keyPairGen1 = KeyPairGenerator.getInstance("RSA")
keyPairGen1.initialize(1024) // Noncompliant

val keyPairGen6 = KeyPairGenerator.getInstance("RSA")
keyPairGen6.initialize(2048) // Compliant
