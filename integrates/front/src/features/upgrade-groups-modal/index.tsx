import { useMutation, useQuery } from "@apollo/client";
import { Form, Formik } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { array, object } from "yup";

import type { IGroup, IUserOrganizationsGroups } from "./queries";
import {
  GET_USER_ORGANIZATIONS_GROUPS,
  REQUEST_GROUPS_UPGRADE_MUTATION,
} from "./queries";

import { ExternalLink } from "components/ExternalLink";
import { Checkbox, Label } from "components/Input";
import { FormGroup } from "components/Input/styles";
import { Modal, ModalConfirm } from "components/Modal";
import { Logger } from "utils/logger";
import { msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IUpgradeGroupsModalProps {
  onClose: () => void;
}

const validations = object().shape({
  groupNames: array().min(1, translate.t("validations.someRequired")),
});

const UpgradeGroupsModal: React.FC<IUpgradeGroupsModalProps> = ({
  onClose,
}): JSX.Element => {
  const { t } = useTranslation();

  const { data } = useQuery<IUserOrganizationsGroups>(
    GET_USER_ORGANIZATIONS_GROUPS,
    {
      fetchPolicy: "cache-first",
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          Logger.warning("Couldn't load user organizations groups", error);
        });
      },
    }
  );
  const organizations = data === undefined ? [] : data.me.organizations;
  const groups = organizations.reduce<IGroup[]>(
    (previousValue, currentValue): IGroup[] => [
      ...previousValue,
      ...currentValue.groups,
    ],
    []
  );
  const upgradableGroups = groups
    .filter(
      (group): boolean =>
        !group.serviceAttributes.includes("has_squad") &&
        group.permissions.includes("request_group_upgrade")
    )
    .map((group): string => group.name);
  const canUpgrade = upgradableGroups.length > 0;

  const [requestGroupsUpgrade] = useMutation(REQUEST_GROUPS_UPGRADE_MUTATION, {
    onCompleted: (): void => {
      msgSuccess(t("upgrade.success.text"), t("upgrade.success.title"));
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.error("Couldn't request groups upgrade", error);
      });
    },
  });

  const handleSubmit = useCallback(
    async (values: { groupNames: string[] }): Promise<void> => {
      onClose();
      await requestGroupsUpgrade({
        variables: { groupNames: values.groupNames },
      });
    },
    [onClose, requestGroupsUpgrade]
  );

  return (
    <Modal open={true} title={t("upgrade.title")}>
      <p>
        {t("upgrade.text")}&nbsp;
        <ExternalLink href={"https://fluidattacks.com/plans/"}>
          {t("upgrade.link")}
        </ExternalLink>
      </p>
      <Formik
        initialValues={{ groupNames: upgradableGroups }}
        name={"upgradeGroups"}
        onSubmit={handleSubmit}
        validationSchema={validations}
      >
        <Form>
          <FormGroup>
            {canUpgrade ? (
              <React.Fragment>
                <Label>{t("upgrade.select")}</Label>
                <br />
                {upgradableGroups.map(
                  (groupName): JSX.Element => (
                    <Checkbox
                      key={groupName}
                      label={_.capitalize(groupName)}
                      name={"groupNames"}
                      value={groupName}
                    />
                  )
                )}
              </React.Fragment>
            ) : (
              <p>{t("upgrade.unauthorized")}</p>
            )}
          </FormGroup>
          <ModalConfirm
            disabled={!canUpgrade}
            onCancel={onClose}
            txtConfirm={t("upgrade.upgrade")}
          />
        </Form>
      </Formik>
    </Modal>
  );
};

export { UpgradeGroupsModal };
