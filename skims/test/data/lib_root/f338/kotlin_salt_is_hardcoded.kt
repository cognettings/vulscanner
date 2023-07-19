import java.security.MessageDigest
import java.util.*

private val SALT = "HARDCODED_SALT"

fun insecureSalt(): String {
    val unsafe_spec = PBEParameterSpec(SALT, 10000)
    val unsafe_spec2 = PBEKeySpec(password, SALT, 10000, 256)
}

fun secureSalt() : String {
    val random = SecureRandom()
    val salt = ByteArray(16)
    random.nextBytes(salt)
    val safe_spec = PBEParameterSpec(salt, 10000)
    val safe_spec2 = PBEKeySpec(password, salt, 10000, 256)
}

fun hashPasswordInsecure(password: String): String {
    val md = MessageDigest.getInstance("SHA-256")
    md.update(SALT.toByteArray())
    val hashedPassword = md.digest(password.toByteArray())
    return Base64.getEncoder().encodeToString(hashedPassword)
}
