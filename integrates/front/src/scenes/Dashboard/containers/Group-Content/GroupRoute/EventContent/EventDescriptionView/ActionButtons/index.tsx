import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import {
  faCheck,
  faPen,
  faRotateRight,
  faTimes,
  faXmark,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { Fragment, useCallback } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { ButtonToolbarStartRow, Row } from "components/Layout";
import { Tooltip } from "components/Tooltip";
import { Can } from "context/authz/Can";
import { authzPermissionsContext } from "context/authz/config";

interface IActionButtonsProps {
  isDirtyForm: boolean;
  isEditing: boolean;
  eventStatus: string;
  onEdit: () => void;
  openRejectSolutionModal: () => void;
  openSolvingModal: () => void;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
  isDirtyForm,
  isEditing,
  eventStatus,
  onEdit: onToggleEdit,
  openRejectSolutionModal,
  openSolvingModal,
}: IActionButtonsProps): JSX.Element => {
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateEvent: boolean = permissions.can(
    "api_mutations_update_event_mutate"
  );

  const DisplayButtons = useCallback((): JSX.Element | null => {
    if (!(isEditing || eventStatus === "SOLVED")) {
      return (
        <Fragment>
          <Can do={"api_mutations_solve_event_mutate"}>
            <Button onClick={openSolvingModal} variant={"primary"}>
              <FontAwesomeIcon icon={faCheck} />
              &nbsp;
              {t("group.events.description.markAsSolved")}
            </Button>
          </Can>
          {eventStatus === "VERIFICATION_REQUESTED" ? (
            <Can do={"api_mutations_reject_event_solution_mutate"}>
              <Tooltip
                id={
                  "group.events.description.rejectSolution.button.tooltip.btn"
                }
                tip={t(
                  "group.events.description.rejectSolution.button.tooltip"
                )}
              >
                <Button onClick={openRejectSolutionModal} variant={"secondary"}>
                  <FontAwesomeIcon icon={faXmark} />
                  &nbsp;
                  {t("group.events.description.rejectSolution.button.text")}
                </Button>
              </Tooltip>
            </Can>
          ) : undefined}
        </Fragment>
      );
    }

    return null;
  }, [eventStatus, isEditing, openRejectSolutionModal, openSolvingModal, t]);

  if (canUpdateEvent && isEditing) {
    return (
      <Row>
        <ButtonToolbarStartRow>
          <DisplayButtons />
          <React.Fragment>
            <Button onClick={onToggleEdit} variant={"secondary"}>
              <React.Fragment>
                <FontAwesomeIcon icon={faTimes} />
                &nbsp;
                {t("group.events.description.cancel")}
              </React.Fragment>
            </Button>
            <Tooltip
              id={"group.events.description.save.tooltip.btn"}
              tip={t("group.events.description.save.tooltip")}
            >
              <Button
                disabled={!isDirtyForm}
                type={"submit"}
                variant={"primary"}
              >
                <FontAwesomeIcon icon={faRotateRight} />
                &nbsp;
                {t("group.events.description.save.text")}
              </Button>
            </Tooltip>
          </React.Fragment>
        </ButtonToolbarStartRow>
      </Row>
    );
  }

  return (
    <Row>
      <ButtonToolbarStartRow>
        <DisplayButtons />
        {canUpdateEvent ? (
          <Tooltip
            id={"group.events.description.edit.tooltip.btn"}
            tip={t("group.events.description.edit.tooltip")}
          >
            <Button onClick={onToggleEdit} variant={"secondary"}>
              <FontAwesomeIcon icon={faPen} />
              &nbsp;
              {t("group.events.description.edit.text")}
            </Button>
          </Tooltip>
        ) : undefined}
      </ButtonToolbarStartRow>
    </Row>
  );
};

export type { IActionButtonsProps };
export { ActionButtons };
