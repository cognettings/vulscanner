import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Random;


// UNSAFE
public class MyServlet extends HttpServlet {

  public void doGet(HttpServletRequest request, HttpServletResponse response) {

    Cookie myCookie = new Cookie("cookie", "cadenaEnv");
    myCookie.setSecure(false);
    myCookie.setPath("/asd/");
    myCookie.setHttpOnly(true);
    response.addCookie(myCookie);

  }

}

// UNSAFE
public class MyServlet extends HttpServlet {

  public void doGet(HttpServletRequest request, HttpServletResponse response) {

    Cookie myCookie = new javax.servlet.http.Cookie("cookie", "cadenaEnv");
    myCookie.setPath("/asd/");
    myCookie.setHttpOnly(true);
    response.addCookie(myCookie);

  }

}

// SAFE
public class MyServlet extends HttpServlet {

  public void doGet(HttpServletRequest request, HttpServletResponse response) {

    Cookie myCookie = new Cookie("cookie", "cadenaEnv");
    myCookie.setSecure(true);
    myCookie.setPath("/asd/");
    myCookie.setHttpOnly(true);
    response.addCookie(myCookie);

  }

}
