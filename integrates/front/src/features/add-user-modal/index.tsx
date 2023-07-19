import { Form, Formik } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { useConfirmInvitation } from "./confirm-invitation";
import { useStakeholderAutofill } from "./hooks";
import type {
  IAddStakeholderModalProps,
  IStakeholderFormValues,
} from "./types";
import { getInitialValues, getSuggestions } from "./utils";
import { validations } from "./validations";

import { Input, Select } from "components/Input";
import { Gap } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Can } from "context/authz/Can";
import { validTextField } from "utils/validations";

const userLevelRoles = ["user", "hacker", "admin"];
const groupLevelRoles = [
  "user",
  "user_manager",
  "customer_manager",
  "vulnerability_manager",
  "architect",
  "hacker",
  "reattacker",
  "resourcer",
  "reviewer",
];
const organizationLevelRoles = ["user", "user_manager", "customer_manager"];

const AddUserModal: React.FC<IAddStakeholderModalProps> = ({
  action,
  editTitle,
  initialValues,
  onClose,
  onSubmit,
  open,
  organizationId,
  groupName,
  domainSuggestions,
  suggestions,
  title,
  type,
}): JSX.Element => {
  const { t } = useTranslation();

  const modalTitle = action === "add" ? title : editTitle;
  const userRoles = type === "user" ? userLevelRoles : [];
  const groupRoles = type === "group" ? groupLevelRoles : [];
  const organizationRoles =
    type === "organization" ? organizationLevelRoles : [];

  const formInitialValues = getInitialValues(initialValues, action);
  const { autofill, loadAutofill } = useStakeholderAutofill(
    type,
    groupName,
    organizationId
  );
  const shouldConfirm = open && action === "add";
  const { confirmInvitation, ConfirmInvitationDialog } = useConfirmInvitation(
    shouldConfirm,
    type,
    groupName,
    organizationId
  );
  const confirmAndSubmit = useCallback(
    async (values: IStakeholderFormValues): Promise<void> => {
      if (await confirmInvitation(values.email)) {
        await onSubmit(values);
      }
    },
    [confirmInvitation, onSubmit]
  );

  return (
    <React.Fragment>
      <Modal onClose={onClose} open={open} title={modalTitle}>
        <Formik
          context={{ groupName }}
          enableReinitialize={true}
          initialValues={{ ...formInitialValues, ...autofill, ...{ type } }}
          name={"addUser"}
          onSubmit={confirmAndSubmit}
          validationSchema={validations}
        >
          {({ isSubmitting, values }): JSX.Element => {
            const { email } = values;
            const allSuggestions = getSuggestions(
              email,
              suggestions,
              domainSuggestions
            );

            return (
              <Form>
                <Gap disp={"block"} mv={12}>
                  <Input
                    disabled={action === "edit"}
                    label={t("userModal.emailText")}
                    list={"email-datalist"}
                    name={"email"}
                    onBlur={type === "group" ? loadAutofill : undefined}
                    placeholder={t("userModal.emailPlaceholder")}
                    required={true}
                    suggestions={allSuggestions}
                    type={"email"}
                  />
                  <Select
                    label={t("userModal.role")}
                    name={"role"}
                    required={true}
                  >
                    <option value={""} />
                    {groupRoles.map(
                      (role): JSX.Element => (
                        <Can do={`grant_group_level_role:${role}`} key={role}>
                          <option value={role.toUpperCase()}>
                            {t(`userModal.roles.${_.camelCase(role)}`)}
                          </option>
                        </Can>
                      )
                    )}
                    {userRoles.map(
                      (role): JSX.Element => (
                        <Can do={`grant_user_level_role:${role}`} key={role}>
                          <option value={role.toUpperCase()}>
                            {t(`userModal.roles.${_.camelCase(role)}`)}
                          </option>
                        </Can>
                      )
                    )}
                    {organizationRoles.map(
                      (role): JSX.Element => (
                        <option key={role} value={role.toUpperCase()}>
                          {t(`userModal.roles.${_.camelCase(role)}`)}
                        </option>
                      )
                    )}
                  </Select>
                  {type === "group" ? (
                    <Input
                      label={t("userModal.responsibility")}
                      name={"responsibility"}
                      placeholder={t("userModal.responsibilityPlaceholder")}
                      required={true}
                      type={"text"}
                      validate={validTextField}
                    />
                  ) : undefined}
                </Gap>
                <ModalConfirm disabled={isSubmitting} onCancel={onClose} />
              </Form>
            );
          }}
        </Formik>
      </Modal>
      <ConfirmInvitationDialog />
    </React.Fragment>
  );
};

export { AddUserModal };
