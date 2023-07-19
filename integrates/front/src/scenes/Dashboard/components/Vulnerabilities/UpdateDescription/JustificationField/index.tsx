import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import _ from "lodash";
import React from "react";

import type { IJustificationFieldProps } from "./types";

import { Editable, TextArea } from "components/Input";
import { authzPermissionsContext } from "context/authz/config";
import { translate } from "utils/translations/translate";

const JustificationField: React.FC<IJustificationFieldProps> = (
  props: IJustificationFieldProps
): JSX.Element => {
  const { areSelectedSubmittedVulnerabilities, lastTreatment } = props;

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRequestZeroRiskVuln: boolean =
    permissions.can("api_mutations_request_vulnerabilities_zero_risk_mutate") &&
    !areSelectedSubmittedVulnerabilities;
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );

  return (
    <div className={"mb3 nt2 w-100"}>
      <Editable
        currentValue={
          _.isUndefined(lastTreatment.justification)
            ? ""
            : lastTreatment.justification
        }
        isEditing={canUpdateVulnsTreatment || canRequestZeroRiskVuln}
        label={translate.t("searchFindings.tabDescription.treatmentJust")}
      >
        <TextArea
          label={translate.t("searchFindings.tabDescription.treatmentJust")}
          name={"justification"}
        />
      </Editable>
    </div>
  );
};

export { JustificationField };
