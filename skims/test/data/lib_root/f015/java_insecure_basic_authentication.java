package mypackage.test;

public class Test {

  public void unsafe(String customEndPoint) throws Exception {

    private String auth = "Authorization";

    from("testAdapter").setHeader("Authorization", "Basic " + customEndPoint);
    from("testAdapter").setHeader(auth, "Basic Authentication");
  }

  public void safe(String customEndPoint) throws Exception {

    private String auth = "Authorization";

    from("testAdapter").setHeader("OwnHeader", "Basic Authorization");
    from("testAdapter").setHeader(auth, "SAFE");
  }
}
