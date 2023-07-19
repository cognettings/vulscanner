import com.auth0.jwt.JWT
import com.auth0.jwt.algorithms.Algorithm

// create a JWT token
// Must Fail line 7

val algorithm = Algorithm.HMAC256("secret")
val token = JWT.create()
    .withIssuer("my-app")
    .withSubject("user123")
    .sign(algorithm)

// verify a JWT token
val verifier = JWT.require(algorithm)
    .withIssuer("my-app")
    .withSubject("user123")
    .build()

val decodedToken = verifier.verify(token)

// Must fail Line 28

val tokenII = JWT.create()
        .withAudience(audience)
        .withIssuer(issuer)
        .withClaim("username", user.username)
        .withExpiresAt(Date(System.currentTimeMillis() + 60000))
        .sign(Algorithm.HMAC256(secret))
    call.respond(hashMapOf("token" to token))

// Following code must not fail (Safe algorithms)

val algorithm = Algorithm.HMAC512("secret")

val tokenSafe = JWT.create()
        .withAudience(audience)
        .withIssuer(issuer)
        .withClaim("username", user.username)
        .withExpiresAt(Date(System.currentTimeMillis() + 60000))
        .sign(Algorithm.HMAC512(secret))
    call.respond(hashMapOf("token" to token))
