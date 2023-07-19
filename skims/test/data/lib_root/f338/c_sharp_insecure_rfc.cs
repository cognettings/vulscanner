namespace Controllers
{
    public class Encrypt
    {
        public static void unsafe(string password)
        {
            String salt = "HARDCODED_SALT";
            var saltBytes = Encoding.UTF8.GetBytes(salt);
            var unsafe1 = new Rfc2898DeriveBytes(password, saltBytes);

            var unsafe2 = new Rfc2898DeriveBytes(password, Encoding.Unicode.GetBytes("UNSAFE"));
        }

        public static void safe(string password)
        {
            // Create a byte array to hold the random value.
            byte[] randomArray = new byte[8];
            using (RNGCryptoServiceProvider rngCsp = newRNGCryptoServiceProvider())
            {
                // Fill the array with a random value.
                rngCsp.GetBytes(randomArray);
            }
            randomArray.toString();
            salt1 = Encoding.Unicode.GetBytes(randomArray);
            var safe1 = new Rfc2898DeriveBytes(password, salt1);
        }
    }
}
