import * as crypto from 'crypto';

function unsafeHashPassword(password: string): string {
  const hash = crypto.createHash('sha256');
  hash.update(password + "HARDCODED_SALT");
  return hash.digest("hex");
}

function safeHashPassword(password: string): string {
  const salt = crypto.randomBytes(16).toString('hex');
  const hash = crypto.createHash('sha256');
  hash.update(password + salt);
  return hash.digest("hex");
}
