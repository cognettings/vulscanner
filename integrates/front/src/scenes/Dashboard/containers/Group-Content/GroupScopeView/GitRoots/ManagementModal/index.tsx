import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route, Switch } from "react-router-dom";

import { Environments } from "./Environments";
import { Repository } from "./Repository";

import { Secrets } from "../../Secrets";
import type { IFormValues } from "../../types";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Modal } from "components/Modal";
import { Tab, TabContent, Tabs } from "components/Tabs";
import { Can } from "context/authz/Can";
import { authzPermissionsContext } from "context/authz/config";

interface IManagementModalProps {
  groupName: string;
  initialValues: IFormValues | undefined;
  isEditing: boolean;
  manyRows: boolean | undefined;
  modalMessages: { message: string; type: string };
  onClose: () => void;
  onSubmitRepo: (values: IFormValues) => Promise<void>;
  runTour: boolean;
  finishTour: () => void;
}

const ManagementModal: React.FC<IManagementModalProps> = ({
  groupName,
  isEditing,
  initialValues = {
    branch: "",
    cloningStatus: {
      message: "",
      status: "UNKNOWN",
    },
    credentials: {
      auth: "",
      azureOrganization: "",
      id: "",
      isPat: false,
      isToken: false,
      key: "",
      name: "",
      password: "",
      token: "",
      type: "",
      typeCredential: "",
      user: "",
    },
    environment: "",
    environmentUrls: [],
    gitEnvironmentUrls: [],
    gitignore: [],
    hasExclusions: "",
    healthCheckConfirm: [],
    id: "",
    includesHealthCheck: "",
    nickname: "",
    secrets: [],
    state: "ACTIVE",
    url: "",
    useVpn: false,
  },
  manyRows = false,
  modalMessages,
  onClose,
  onSubmitRepo,
  runTour,
  finishTour,
}: IManagementModalProps): JSX.Element => {
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateRootState: boolean = permissions.can(
    "api_mutations_update_git_root_mutate"
  );
  const { t } = useTranslation();

  return (
    <Modal
      maxWidth={"1050px"}
      minWidth={700}
      onClose={onClose}
      open={true}
      title={t(`group.scope.common.${isEditing ? "edit" : "add"}`, {
        count: manyRows ? 2 : 1,
      })}
    >
      <MemoryRouter
        initialEntries={[canUpdateRootState ? "/repository" : "/secrets"]}
      >
        {isEditing ? (
          <Tabs>
            <Can do={"api_mutations_update_git_root_mutate"}>
              <Tab
                id={"repoTab"}
                link={"/repository"}
                tooltip={t("group.scope.git.repo.title")}
              >
                {t("group.scope.git.repo.title")}
              </Tab>
            </Can>
            <Can do={"api_mutations_update_git_environments_mutate"}>
              <Tab
                id={"envsTab"}
                link={"/environments"}
                tooltip={t("group.scope.git.manageEnvsTooltip")}
              >
                {t("group.scope.git.envUrls")}
              </Tab>
            </Can>
            <Can do={"api_resolvers_git_root_secrets_resolve"}>
              <Tab
                id={"secretsTab"}
                link={"/secrets"}
                tooltip={t("group.scope.git.repo.title")}
              >
                {"Secrets"}
              </Tab>
            </Can>
          </Tabs>
        ) : undefined}
        <TabContent>
          <Switch>
            <Route path={"/repository"}>
              <ConfirmDialog
                message={t("group.scope.git.confirmBranch")}
                title={t("group.scope.common.confirm")}
              >
                {(confirm): React.ReactNode => {
                  return (
                    <Repository
                      confirm={confirm}
                      finishTour={finishTour}
                      initialValues={initialValues}
                      isEditing={isEditing}
                      manyRows={manyRows}
                      modalMessages={modalMessages}
                      onClose={onClose}
                      onSubmitRepo={onSubmitRepo}
                      runTour={runTour}
                    />
                  );
                }}
              </ConfirmDialog>
            </Route>
            <Route path={"/environments"}>
              <Environments
                groupName={groupName}
                onClose={onClose}
                rootInitialValues={initialValues}
              />
            </Route>
            <Route path={"/secrets"}>
              <Secrets gitRootId={initialValues.id} groupName={groupName} />
            </Route>
          </Switch>
        </TabContent>
      </MemoryRouter>
    </Modal>
  );
};

export { ManagementModal };
