import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

public class Test {
	public static void unsafeConfigs(){
		JSch ssh = new JSch();
		session = ssh.getSession(Utils.DEFAULT_USER, value.getPublicIpAddress());
		String check_host = "No";
		session.setConfig("StrictHostKeyChecking", check_host);
		session.connect();
	}

	public static void secureConfig(){
		JSch ssh = new JSch();
		Session session = ssh.getSession(Utils.DEFAULT_USER, value.getPublicIpAddress());
		java.util.Properties config = new java.util.Properties();
		config.put("StrictHostKeyChecking", "Yes");
		config.put("SomethingElse", "No");
		session.setConfig(config);
	}
}
