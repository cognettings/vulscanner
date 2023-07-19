using System.Security.Cryptography;

string input = "This is a test message.";
byte[] key = Encoding.UTF8.GetBytes("my-secret-key");

// Must fail pointing to line 7
using (HMACSHA256 hmac = new HMACSHA256(key))
{
    byte[] hash = hmac.ComputeHash(Encoding.UTF8.GetBytes(input));
    string hashString = BitConverter.ToString(hash).Replace("-", "").ToLower();
}

// must not fail
using (HMACSHA512 hmacII = new HMACSHA512(key))
{
    byte[] hash = hmacII.ComputeHash(Encoding.UTF8.GetBytes(input));
    string hashString = BitConverter.ToString(hash).Replace("-", "").ToLower();
}
