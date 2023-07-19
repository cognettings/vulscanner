import java.security.MessageDigest;
import com.gree.encryption.services.GreeEncryptionService;

public class GFG1 {
    public static void main(String[] argv)
    {
        GreeEncryptionService greeEncryptionService = new GreeEncryptionService();
        String cipher = greeEncryptionService.getAlgo(true);
        MessageDigest sr = MessageDigest.getInstance(cipher);

    }
}
