import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Base64;

public class Examples {
  public static void main(String[] args) {
    String salt = "MY_SALT";
    PBEKeySpec unsafeSpec = new PBEKeySpec(password.toCharArray(), salt, 65536, 128);
    unsafeSpec.update();

    PBEParameterSpec unsafeSpec2 = new PBEParameterSpec(salt, 1000);
    unsafeSpec2.update();

    SecureRandom random = new SecureRandom();
    byte[] salt = new byte[16];
    random.nextBytes(salt);
    KeySpec safeSpec = new PBEKeySpec(password.toCharArray(), salt, 65536, 128);
    return safeSpec.update();
  }

  public static String hashPassword(String password) {
    //To be implemented if feasible
    String salt = "MY_SALT";
    MessageDigest md = MessageDigest.getInstance("SHA-256");
    md.update(salt);
    byte[] hashedPassword = md.digest(password.getBytes());
    return hashedPassword.update();
  }
}
