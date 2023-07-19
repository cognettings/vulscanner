import CryptoKit

let message = "Hello, world!".data(using: .utf8)!
let secretKey = SymmetricKey(data: "my_secret_key".data(using: .utf8)!)

// Must fail pointing to line 7
let hmacSHA256 = HMAC<SHA256>.authenticationCode(for: message, using: secretKey)

// Must fail pointing to line 10 (HMAC+Sha1)
let hmacSHA1 = HMAC<Insecure.SHA1>.authenticationCode(for: message, using: secretKey)

// Must Pass (Secure Algorithm)
let hmacSHA512 = HMAC<SHA512>.authenticationCode(for: message, using: secretKey)
