
string input = "This is a test message.";
byte[] key = Encoding.UTF8.GetBytes("my-secret-key");

// Must not fail. Dangerous namespace was not imported.
using (HMACSHA256 hmac = new HMACSHA256(key))
{
    byte[] hash = hmac.ComputeHash(Encoding.UTF8.GetBytes(input));
    string hashString = BitConverter.ToString(hash).Replace("-", "").ToLower();
}
