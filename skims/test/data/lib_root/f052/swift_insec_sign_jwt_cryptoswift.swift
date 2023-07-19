import CryptoSwift

func shouldFailSha256(message: String, secretKey: String) throws -> String {
    guard let keyData = secretKey.data(using: .utf8) else {
        throw NSError(domain: "Invalid secret key", code: 0, userInfo: nil)
    }

    let key = SymmetricKey(data: keyData)
    let messageData = message.data(using: .utf8)!
    let signature = try HMAC(key: key, variant: .sha256).authenticate(messageData.bytes)

    return signature.toBase64() // Encode the signature in Base64 format
}

func shouldFailSha1(message: String, secretKey: String) throws -> String {
    guard let keyData = secretKey.data(using: .utf8) else {
        throw NSError(domain: "Invalid secret key", code: 0, userInfo: nil)
    }

    let key = SymmetricKey(data: keyData)
    let messageData = message.data(using: .utf8)!
    let signature = try HMAC(key: key, variant: .sha1).authenticate(messageData.bytes)

    return signature.toBase64() // Encode the signature in Base64 format
}

func shouldPass(message: String, secretKey: String) throws -> String {
    guard let keyData = secretKey.data(using: .utf8) else {
        throw NSError(domain: "Invalid secret key", code: 0, userInfo: nil)
    }

    let key = SymmetricKey(data: keyData)
    let messageData = message.data(using: .utf8)!
    let signature = try HMAC(key: key, variant: .sha512).authenticate(messageData.bytes)

    return signature.toBase64() // Encode the signature in Base64 format
}
