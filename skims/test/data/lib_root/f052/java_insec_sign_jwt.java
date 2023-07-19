import static org.junit.Assert.assertTrue;
import java.util.Date;
import org.junit.Test;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jws;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

public class JwtTest {

	@Test
	public void testJWT() {
		String token = generateJwtToken();
		assertTrue(token != null);
		printStructure(token);
		printBody(token);
	}

	@SuppressWarnings("deprecation")
	private String generateJwtToken() {
		String token = Jwts.builder().setSubject("adam")
				.setExpiration(new Date(2018, 1, 1))
				.setIssuer("info@wstutorial.com")
				.claim("groups", new String[] { "user", "admin" })
				// HMAC using SHA-256  and 12345678 base64 encoded
				.signWith(SignatureAlgorithm.HS256, "MTIzNDU2Nzg=").compact();
		return token;
	}

	private static Mac mustFail(byte[] key) {
		// Java forbids empty keys
		if (key.length == 0) {
			key = new byte[1];
		}
		try {
			Mac mac = Mac.getInstance("HmacSHA256");
			mac.init(new SecretKeySpec(key, "HmacSHA256"));
			return mac;
		} catch (GeneralSecurityException e) {
			throw new RuntimeException(e);
		}
	}

	@SuppressWarnings("deprecation")
	private String generateJwtTokenSAFE() {
		String token = Jwts.builder().setSubject("adam")
				.setExpiration(new Date(2018, 1, 1))
				.setIssuer("info@wstutorial.com")
				.claim("groups", new String[] { "user", "admin" })
				// HMAC using SHA-512 and 12345678 base64 encoded
				.signWith(SignatureAlgorithm.HS512, "MTIzNDU2Nzg=").compact();
		return token;
	}

	private static Mac mustPass(byte[] key) {
		// Java forbids empty keys
		if (key.length == 0) {
			key = new byte[1];
		}
		try {
			Mac mac = Mac.getInstance("HmacSHA512");
			mac.init(new SecretKeySpec(key, "HmacSHA512"));
			return mac;
		} catch (GeneralSecurityException e) {
			throw new RuntimeException(e);
		}
	}
}
