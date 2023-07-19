import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";
import { useTranslation } from "react-i18next";

import type { ITagFieldProps } from "./types";

import { InputTags } from "components/Input";
import { authzPermissionsContext } from "context/authz/config";

const TagField: React.FC<ITagFieldProps> = ({
  handleDeletion,
}: ITagFieldProps): JSX.Element => {
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );
  const canDeleteVulnsTags: boolean = permissions.can(
    "api_mutations_remove_vulnerability_tags_mutate"
  );

  return (
    <React.StrictMode>
      <div className={"mb3 nt2 w-100"}>
        <InputTags
          disabled={!(canUpdateVulnsTreatment && canDeleteVulnsTags)}
          label={t("searchFindings.tabDescription.tag")}
          name={"tag"}
          onRemove={handleDeletion}
        />
      </div>
    </React.StrictMode>
  );
};

export { TagField };
