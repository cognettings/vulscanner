

let cryptor = try Cryptor(operation: .encrypt, algorithm: .des, options: .none, key: key, iv: []) // Noncompliant

let crypt = CkoCrypt2()
crypt.CryptAlgorithm = "3des" // Noncompliant



let cryptor = try Cryptor(operation: .encrypt, algorithm: .aes, options: .none, key: key, iv: []) // Compliant

let crypt = CkoCrypt2()
crypt.CryptAlgorithm = "aes" // Compliant
