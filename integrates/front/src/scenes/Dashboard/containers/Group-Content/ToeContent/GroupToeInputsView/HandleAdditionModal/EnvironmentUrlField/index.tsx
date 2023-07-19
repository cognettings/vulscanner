import { useFormikContext } from "formik";
import _ from "lodash";
import React, { useEffect } from "react";

import type { IEnvironmentUrlFieldProps } from "./types";

import type { IFormValues } from "../types";
import { isGitRoot } from "../utils";
import { Select } from "components/Input";
import { FormGroup } from "components/Input/styles";
import { translate } from "utils/translations/translate";

const EnvironmentUrlField: React.FC<IEnvironmentUrlFieldProps> = ({
  selectedRoot,
}: IEnvironmentUrlFieldProps): JSX.Element => {
  const { values, setFieldValue } = useFormikContext<IFormValues>();

  useEffect((): void => {
    if (
      !_.isEmpty(values.environmentUrl) &&
      (_.isUndefined(selectedRoot) ||
        !isGitRoot(selectedRoot) ||
        (!_.isUndefined(selectedRoot) &&
          isGitRoot(selectedRoot) &&
          _.isEmpty(selectedRoot.gitEnvironmentUrls)))
    ) {
      setFieldValue("environmentUrl", "");
    }
    if (
      _.isEmpty(values.environmentUrl) &&
      !_.isUndefined(selectedRoot) &&
      isGitRoot(selectedRoot) &&
      !_.isEmpty(selectedRoot.gitEnvironmentUrls)
    ) {
      setFieldValue("environmentUrl", selectedRoot.gitEnvironmentUrls[0].url);
    }
  }, [setFieldValue, selectedRoot, values]);

  return (
    <FormGroup>
      {!_.isUndefined(selectedRoot) && isGitRoot(selectedRoot) ? (
        <Select
          id={"environmentUrl"}
          label={translate.t("group.toe.inputs.addModal.fields.environmentUrl")}
          name={"environmentUrl"}
        >
          <option value={""}>{""}</option>
          {selectedRoot.gitEnvironmentUrls.map(
            (envUrl): JSX.Element => (
              <option key={envUrl.id} value={envUrl.url}>
                {envUrl.url}
              </option>
            )
          )}
        </Select>
      ) : undefined}
    </FormGroup>
  );
};

export { EnvironmentUrlField };
