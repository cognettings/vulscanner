/*
 * You can import and use all API from the 'vscode' module
 * as well as import your extension to test it
 */
import { window } from "vscode";
import { expect } from "chai";

describe("Extension Test Suite", () => {
  window.showInformationMessage("Start all tests.");

  it("Placeholder test", () => {
    const simpleSum = 1 + 1;

   expect(simpleSum).to.equal(2);
  });
});
