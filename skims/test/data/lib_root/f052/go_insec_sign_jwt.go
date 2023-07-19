import (
    "github.com/dgrijalva/jwt-go"
    "time"
)

// Must fail line 14 first case.
func createTokenDang() (string, error) {
    claims := jwt.MapClaims{
        "sub": "1234567890",
        "name": "John Doe",
        "iat": time.Now().Unix(),
        "exp": time.Now().Add(time.Hour * 24).Unix(),
    }
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    secret := "mysecret" // Replace with your own secret key
    tokenString, err := token.SignedString([]byte(secret))
    if err != nil {
        return "", err
    }
    return tokenString, nil
}

// Must Fail line 39 & 40 second case:
func createTokenDangII() (string, error) {
    now := time.Now()
    opt := &jwt.Options{
        JWTID:          "unique_id",
        Timestamp:      true,
        ExpirationTime: now.Add(24 * 30 * 12 * time.Hour),
        NotBefore:      now.Add(30 * time.Minute),
        Subject:        "123",
        Audience:       "admin",
        Issuer:         "auth_server",
        KeyID:          "my_key",
        Public:         map[string]interface{}{"foo": "bar", "myBool": true},
    }

    // Define a signer.
    sig := jwt.HS256("my_53cr37")
    algValidator := jwt.AlgorithmValidator(jwt.MethodHS256)

    // Issue a new token.
    token, err := jwt.Sign(sig, opt)
}

// Must pase, safe alg, first case
func createTokenSafe() (string, error) {
    claims := jwt.MapClaims{
        "sub": "1234567890",
        "name": "John Doe",
        "iat": time.Now().Unix(),
        "exp": time.Now().Add(time.Hour * 24).Unix(),
    }
    token := jwt.NewWithClaims(jwt.SigningMethodHS512, claims)
    secret := "mysecret" // Replace with your own secret key
    tokenString, err := token.SignedString([]byte(secret))
    if err != nil {
        return "", err
    }
    return tokenString, nil
}

// Must pase, safe alg, second case
func createTokenSafeII() (string, error) {
    now := time.Now()
    opt := &jwt.Options{
        JWTID:          "unique_id",
        Timestamp:      true,
        ExpirationTime: now.Add(24 * 30 * 12 * time.Hour),
        NotBefore:      now.Add(30 * time.Minute),
        Subject:        "123",
        Audience:       "admin",
        Issuer:         "auth_server",
        KeyID:          "my_key",
        Public:         map[string]interface{}{"foo": "bar", "myBool": true},
    }

    // Define a signer.
    sig := jwt.HS512("my_53cr37")
    algValidator := jwt.AlgorithmValidator(jwt.MethodHS512)


    // Issue a new token.
    token, err := jwt.Sign(sig, opt)
}
