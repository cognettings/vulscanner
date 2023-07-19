using System;

namespace TestSpace
{
  public class Test
  {
    public static string unsafe_cred(string connString){
      CryptLib _crypt = new CryptLib();
      string key = CryptLib.getHashSha256("bGZkYjIwMTgq", 32);
      return _crypt.decrypt(connString, key, "75npchtk5DpbTGbB");
    }

    public static string safe_cred(string connString, string env_keys, string iv_secret){
      CryptLib _crypt = new CryptLib();
      string key = env_keys["encrypted_key"];
      return _crypt.decrypt(connString, key, iv_secret);
    }
  }
}
