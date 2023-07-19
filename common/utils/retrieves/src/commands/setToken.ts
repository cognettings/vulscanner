import _ from "lodash";
import type { InputBoxValidationMessage } from "vscode";
import {
  ConfigurationTarget,
  InputBoxValidationSeverity,
  window,
  workspace,
  // eslint-disable-next-line import/no-unresolved
} from "vscode";

import { Logger } from "../utils/logging";
import { validTextField } from "../utils/validations";

const setToken = async (): Promise<void> => {
  const armToken = await window.showInputBox({
    placeHolder: "Paste your token here",
    title: "Fluid Attacks API Token",
    validateInput: (token): InputBoxValidationMessage | undefined => {
      const validationMessage = validTextField(token);

      if (!_.isNil(validationMessage)) {
        return {
          message: `Invalid JSON Web Token: ${validationMessage}`,
          severity: InputBoxValidationSeverity.Error,
        };
      }

      return undefined;
    },
  });

  if (!_.isNil(armToken)) {
    const fluidConfig = workspace.getConfiguration("fluidattacks");
    await fluidConfig.update("apiToken", armToken, ConfigurationTarget.Global);
    Logger.info("Fluid Attacks token updated");
  }
};

export { setToken };
