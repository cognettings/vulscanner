using System;
using System.IdentityModel.Tokens.Jwt;
using Jose;
using Microsoft.IdentityModel.Tokens;
using System.Text;

class MustFail
{
    static void Main(string[] args)
    {
        MustFail1();
        MustFail2();
        MustFail3();
    }

    static void MustFail1()
    {
        // create a security key
        var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes("my_secret_key"));

        // create signing credentials
        var signingCredentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

        // create a JWT token with invalid issuer
        var token = new JwtSecurityToken(
            issuer: "invalid_issuer",
            audience: "my_audience",
            claims: null,
            expires: DateTime.Now.AddDays(1),
            signingCredentials: signingCredentials);

        // serialize the token to a string
        var tokenHandler = new JwtSecurityTokenHandler();
        var tokenString = tokenHandler.WriteToken(token);

    }

    static void MustFail2()
    {
        // create a security key
        var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes("my_secret_key"));

        // create signing credentials
        var signingCredentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

        // create a JWT token with invalid signing credentials
        var tokenDescriptor = new SecurityTokenDescriptor
        {
            Subject = new System.Security.Claims.ClaimsIdentity(new System.Security.Claims.Claim[] { }),
            Expires = DateTime.UtcNow.AddDays(1),
            SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(Encoding.UTF8.GetBytes("invalid_secret_key")), SecurityAlgorithms.HmacSha256)
        };

        var tokenHandler = new JwtSecurityTokenHandler();
        var token = tokenHandler.CreateJwtSecurityToken(tokenDescriptor);

        // serialize the token to a string
        var tokenString = tokenHandler.WriteToken(token);

    }

    static void MustFail3()
    {
        // create a JWT token with invalid signature
        var token = JWT.Encode(
            new { sub = "my_subject", exp = DateTimeOffset.UtcNow.AddDays(1).ToUnixTimeSeconds() },
            Encoding.UTF8.GetBytes("invalid_secret_key"),
            JwsAlgorithm.HS256);

        // decode the JWT token
        var decoded = JWT.Decode(token, Encoding.UTF8.GetBytes("my_secret_key"));

        // verify the JWT token
        var isValid = JWT.TryDecode(token, Encoding.UTF8.GetBytes("my_secret_key"), out var payload);

    }
}

class MustPass
{
    static void Main(string[] args)
    {
        MustPass1();
        MustPass2();
        MustPass3();
    }

    static void MustPass1()
    {
        // create a security key
        var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes("my_secret_key"));

        // create signing credentials
        var signingCredentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha512);

        // create a JWT token with invalid issuer
        var token = new JwtSecurityToken(
            issuer: "invalid_issuer",
            audience: "my_audience",
            claims: null,
            expires: DateTime.Now.AddDays(1),
            signingCredentials: signingCredentials);

        // serialize the token to a string
        var tokenHandler = new JwtSecurityTokenHandler();
        var tokenString = tokenHandler.WriteToken(token);

    }

    static void MustPass2()
    {
        // create a security key
        var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes("my_secret_key"));

        // create signing credentials
        var signingCredentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha512);

        // create a JWT token with invalid signing credentials
        var tokenDescriptor = new SecurityTokenDescriptor
        {
            Subject = new System.Security.Claims.ClaimsIdentity(new System.Security.Claims.Claim[] { }),
            Expires = DateTime.UtcNow.AddDays(1),
            SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(Encoding.UTF8.GetBytes("invalid_secret_key")), SecurityAlgorithms.HmacSha512)
        };

        var tokenHandler = new JwtSecurityTokenHandler();
        var token = tokenHandler.CreateJwtSecurityToken(tokenDescriptor);

        // serialize the token to a string
        var tokenString = tokenHandler.WriteToken(token);

    }

    static void MustPass3()
    {
        // create a JWT token with invalid signature
        var token = JWT.Encode(
            new { sub = "my_subject", exp = DateTimeOffset.UtcNow.AddDays(1).ToUnixTimeSeconds() },
            Encoding.UTF8.GetBytes("invalid_secret_key"),
            JwsAlgorithm.HS512);

        // decode the JWT token
        var decoded = JWT.Decode(token, Encoding.UTF8.GetBytes("my_secret_key"));

        // verify the JWT token
        var isValid = JWT.TryDecode(token, Encoding.UTF8.GetBytes("my_secret_key"), out var payload);

    }
}
