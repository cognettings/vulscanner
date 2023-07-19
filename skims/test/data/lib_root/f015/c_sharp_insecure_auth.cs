using System;

namespace TestSpace
{
  public class Test
  {
    string url;

    WebResponse TestResponse(){
      WebRequest cRequest = WebRequest.Create(url);
      cRequest.Method = "post";
      cRequest.ContentType = "application/json;charset=UTF-8";
      cRequest.PreAuthenticate = true;
      String my_str = "Base64";
      cRequest.Headers.Add("Authorization", "Basic " + my_str);
      return cRequest;
    }
  }
}
