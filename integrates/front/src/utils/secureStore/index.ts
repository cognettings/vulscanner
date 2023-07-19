/* eslint-disable fp/no-let,fp/no-mutation
  --------
  We need both to be able to generate and assign a secret key, every time its
  useful life expires.
*/
import _ from "lodash";
import type React from "react";
import { createContext } from "react";
import type sjcl from "sjcl";
import {
  random,
  codec as sjclCodec,
  decrypt as sjclDecrypt,
  encrypt as sjclEncrypt,
  hash as sjclHash,
} from "sjcl";

import { Logger } from "utils/logger";

/*
 * Secrets declared in this file live as much as the dashboard tab is open
 * or this predefined lifespan
 */
const secondsInMs: number = 1000;
const secretsLifespan: number = 600;
const secretsLifespanInMiliseconds: number = secretsLifespan * secondsInMs;

const wordsNumber: number = 8;

// Secrets
let secretKey: sjcl.BitArray = random.randomWords(wordsNumber);

// Secrets generation
const generateSecrets = (): void => {
  secretKey = random.randomWords(wordsNumber);
};

// Secrets rotation
setInterval(generateSecrets, secretsLifespanInMiliseconds);

// Type aliases
declare type iFrameReferenceType =
  React.MutableRefObject<HTMLIFrameElement | null>;

// Implementation
const decrypt = (ciphertext: string): string =>
  sjclDecrypt(secretKey, JSON.parse(ciphertext) as sjcl.SjclCipherEncrypted);

const encrypt = (plaintext: string): string =>
  JSON.stringify(sjclEncrypt(secretKey, plaintext));

const hash = (input: string): string =>
  sjclCodec.hex.fromBits(sjclHash.sha256.hash(input));

const storeBlob = (
  identifier: string,
  contents: string,
  mime: string
): string => {
  const blob: Blob = new Blob([contents], { type: mime });
  const itemName: string = hash(identifier);
  const url: string = URL.createObjectURL(blob).toString();

  /*
   * Revoke the url that points to the blob, and therefore the blob
   * https://w3c.github.io/FileAPI/#creating-revoking
   */
  const revokeUrl = (): void => {
    URL.revokeObjectURL(url);
  };
  setTimeout(revokeUrl, secretsLifespanInMiliseconds);

  try {
    sessionStorage.setItem(itemName, encrypt(url));
  } catch {
    revokeUrl();
  }

  return url;
};

const removeBlob = (identifier: string): void => {
  const itemName: string = hash(identifier);
  sessionStorage.removeItem(itemName);
  URL.revokeObjectURL(identifier);
};

const retrieveBlob = (identifier: string): string => {
  let url: string | null = identifier;
  const itemName: string = hash(identifier);

  try {
    const itemValue: string | null = sessionStorage.getItem(itemName);
    url = itemValue === null ? identifier : decrypt(itemValue);
  } catch {
    sessionStorage.removeItem(itemName);
  }

  return url;
};

const storeIframeContent = (reference: Readonly<iFrameReferenceType>): void => {
  if (
    location.hostname === reference.current?.contentDocument?.location.hostname
  ) {
    const contents: string =
      reference.current.contentDocument.documentElement.outerHTML;
    const identifier: string | undefined =
      reference.current.contentWindow?.location.href;

    if (!_.isUndefined(identifier) && !_.isUndefined(contents)) {
      storeBlob(identifier, contents, "text/html");
    }
  } else {
    Logger.info("Iframe with Cross-origin: Host != Iframe Host", {
      location,
      reference: reference.current?.contentDocument,
    });
  }
};

interface ISecureStoreConfig {
  decrypt: (ciphertext: string) => string;
  encrypt: (plaintext: string) => string;
  hash: (input: string) => string;
  removeBlob: (identifier: string) => void;
  retrieveBlob: (identifier: string) => string;
  storeBlob: (identifier: string, contents: string, mime: string) => string;
  storeIframeContent: (reference: Readonly<iFrameReferenceType>) => void;
}

const secureStore: ISecureStoreConfig = {
  decrypt,
  encrypt,
  hash,
  removeBlob,
  retrieveBlob,
  storeBlob,
  storeIframeContent,
};

const secureStoreContext: React.Context<ISecureStoreConfig> =
  createContext(secureStore);

export type { ISecureStoreConfig };
export { secureStore, secureStoreContext };
