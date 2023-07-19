import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faPen } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Tooltip } from "components/Tooltip";
import { authzPermissionsContext } from "context/authz/config";

interface IEditButtonProps {
  isDisabled: boolean;
  onEdit: () => void;
}

const EditButton: React.FC<IEditButtonProps> = ({
  isDisabled,
  onEdit,
}: IEditButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateAttackedLines: boolean = permissions.can(
    "api_mutations_update_toe_lines_attacked_lines_mutate"
  );

  return (
    <React.StrictMode>
      {canUpdateAttackedLines ? (
        <Tooltip
          disp={"inline-block"}
          id={"group.toe.lines.actionButtons.editButton.tooltip.id"}
          tip={t("group.toe.lines.actionButtons.editButton.tooltip")}
        >
          <Button
            disabled={isDisabled}
            id={"editToeLines"}
            onClick={onEdit}
            variant={"secondary"}
          >
            <FontAwesomeIcon icon={faPen} />
            &nbsp;
            {t("group.toe.lines.actionButtons.editButton.text")}
          </Button>
        </Tooltip>
      ) : undefined}
    </React.StrictMode>
  );
};

export type { IEditButtonProps };
export { EditButton };
