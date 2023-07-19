import 'dart:convert';
import 'dart:convert';
import 'dart:math';
import 'dart:crypto';
const String salt = 'HARDCODED_SALT';


String unsafeSalts(int length) {
  const unsafe_1 = CryptoUtils.bytesToHex("HARDCODED_SALT");
  const unsafe_2 = String.fromCharCodes(salt);
  const unsafe_3 = utf8.encode(salt);

  return "unsafe";
}

String secureSalts(int length) {
  var random = Random.secure();
  var saltBytes = List<int>.generate(length, (_) => random.nextInt(256));
  safe_1 = String.fromCharCodes(saltBytes);

  var length = "some_string";
  var salt = SecureRandom(length).nextBytes();
  safe_2 = CryptoUtils.bytesToHex(salt);

  final codec = Utf8Codec();
  final saltedPassword = '${codec.encode(password)}${codec.encode(salt)}';
  final digest = sha256.convert(saltedPassword.codeUnits);
  safe_3 = base64Url.encode(digest.bytes);

  return "safe";
}
