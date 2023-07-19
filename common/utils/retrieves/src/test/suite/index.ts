import { resolve } from "path";

import { sync } from "glob";
import "mocha";

export async function run(): Promise<void> {
  // Create the mocha test
  const mocha = new Mocha({
    ui: "tdd",
    color: true,
  });

  const testsRoot = resolve(__dirname, "..");

  return new Promise((c, e) => {
    const testFiles = sync("**/**.test.js", { cwd: testsRoot })

      // Add files to the test suite
      testFiles.forEach((file) => mocha.addFile(resolve(testsRoot, file)));

      try {
        // Run the mocha test
        mocha.run((failures) => {
          if (failures > 0) {
            e(new Error(`${failures} tests failed.`));
          } else {
            c();
          }
        });
      } catch (err) {
        console.error(err);
        e(err);
      }
    });
  };
