import java.io.IOException;
import javax.servlet.http.HttpServletRequest;

public class Test1 {

  public void runUnsafe(HttpServletRequest request) {
    param = request.getHeader("someheader");
    ProcessBuilder pb = new ProcessBuilder();
    pb.command(param);
    Process p = pb.start();

  }
}

public class Test2 {

	public void doPost(HttpServletRequest request) {

		String param = "";
		java.util.Enumeration<String> headers = request.getHeaders("BenchmarkTest00017");
		param = headers.nextElement();
		param = java.net.URLDecoder.decode(param, "UTF-8");
		Runtime r = Runtime.getRuntime();
    Process p = r.exec(param);
	}

}
