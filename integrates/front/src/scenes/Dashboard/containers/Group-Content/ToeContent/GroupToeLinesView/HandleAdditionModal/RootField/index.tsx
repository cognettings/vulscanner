import React from "react";

import type { IRootFieldProps } from "./types";

import type { IGitRootAttr } from "../types";
import { Select } from "components/Input";
import { FormGroup } from "components/Input/styles";
import { translate } from "utils/translations/translate";

const RootField: React.FC<IRootFieldProps> = (
  props: IRootFieldProps
): JSX.Element => {
  const { roots } = props;

  return (
    <FormGroup>
      <Select
        label={translate.t("group.toe.lines.addModal.fields.root")}
        name={"rootId"}
      >
        {roots.map((root: IGitRootAttr): JSX.Element => {
          return (
            <option key={root.id} value={root.id}>
              {root.nickname}
            </option>
          );
        })}
      </Select>
    </FormGroup>
  );
};

export { RootField };
