import { createHash } from "crypto";

function unsafeHashPassword(password) {
  const hash = createHash("sha256");
  hash.update(password + "HARDCODED_SALT");
}

function safeHashPassword(password) {
  const salt = crypto.randomBytes(16).toString("hex");
  const hash = crypto.createHash("sha256");
  hash.update(password + salt);
}

function safeHashPassword(password) {
  const salt = crypto.randomBytes(16).toString("hex");
  const hash = crypto.createHash("sha256").update(`009${process.env.var}`);
  return hash;
}
