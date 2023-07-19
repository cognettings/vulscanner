import java.io.IOException;
import javax.servlet.http.HttpServletRequest;

public class Test {

  public void unsafeSession(HttpServletRequest request){
    param = request.getHeader("someheader");
    request.getSession().setAttribute("something", param);
  }

  public void safeSession(HttpServletRequest request){
    param = "Hello from the server";
    request.getSession().setAttribute(param);
  }
}
