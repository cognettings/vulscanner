import React from "react";

import type { IRootFieldProps } from "./types";

import { Input } from "components/Input";
import { FormGroup } from "components/Input/styles";
import { translate } from "utils/translations/translate";

const RootField: React.FC<IRootFieldProps> = (
  props: IRootFieldProps
): JSX.Element => {
  const { roots } = props;
  const nicknames = roots.map((root): string => root.nickname);

  return (
    <FormGroup>
      <Input
        label={translate.t("group.toe.inputs.addModal.fields.root")}
        list={"rootNickname-list"}
        name={"rootNickname"}
        suggestions={nicknames}
      />
    </FormGroup>
  );
};

export { RootField };
