import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { VisibilityState } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { Fragment, useCallback, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddEnvironment } from "./AddEnvironment";

import { Button } from "components/Button";
import type { IConfirmFn } from "components/ConfirmDialog";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Modal, ModalConfirm } from "components/Modal";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { authzPermissionsContext } from "context/authz/config";
import { useStoredState } from "hooks";
import {
  GET_ROOT_ENVIRONMENT_URLS,
  REMOVE_ENVIRONMENT_URL,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/queries";
import type {
  IBasicEnvironmentUrl,
  IFormValues,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IEnvironmentsProps {
  rootInitialValues: IFormValues;
  groupName: string;
  onClose: () => void;
}

interface IEnvironmentUrlItem extends IBasicEnvironmentUrl {
  element: JSX.Element;
}

const Environments: React.FC<IEnvironmentsProps> = ({
  rootInitialValues,
  groupName,
  onClose,
}: IEnvironmentsProps): JSX.Element => {
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  const [isAddEnvModalOpen, setIsAddEnvModalOpen] = useState(false);
  const { data, loading } = useQuery<{
    root: { gitEnvironmentUrls: IBasicEnvironmentUrl[] };
  }>(GET_ROOT_ENVIRONMENT_URLS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load environment urls", error);
      });
    },
    variables: { groupName, rootId: rootInitialValues.id },
  });
  const [columnVisibility, setColumnVisibility] =
    useStoredState<VisibilityState>("tblGitRootSecrets-visibilityState", {
      element: permissions.can("api_mutations_remove_environment_url_mutate"),
    });
  const [removeEnvironmentUrl, { loading: isRemoving }] = useMutation(
    REMOVE_ENVIRONMENT_URL,
    {
      onCompleted: (): void => {
        msgSuccess(
          t("group.scope.git.removeEnvironment.success"),
          t("group.scope.git.removeEnvironment.successTitle")
        );
      },
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.error("Couldn't remove enviroment url", error);
        });
      },
      refetchQueries: [
        {
          query: GET_ROOT_ENVIRONMENT_URLS,
          variables: { groupName, rootId: rootInitialValues.id },
        },
      ],
    }
  );

  const openAddModal = useCallback((): void => {
    setIsAddEnvModalOpen(true);
  }, []);
  const closeAddModal = useCallback((): void => {
    setIsAddEnvModalOpen(false);
  }, []);

  const handleRemoveClick = useCallback(
    (urlId: string): void => {
      void removeEnvironmentUrl({
        variables: { groupName, rootId: rootInitialValues.id, urlId },
      });
    },
    [groupName, rootInitialValues.id, removeEnvironmentUrl]
  );

  const onConfirmDelete = useCallback(
    (confirm: IConfirmFn, gitEnvironment: IBasicEnvironmentUrl): (() => void) =>
      (): void => {
        confirm((): void => {
          handleRemoveClick(gitEnvironment.id);
        });
      },
    [handleRemoveClick]
  );

  const gitEnvironmentUrls = useMemo((): IEnvironmentUrlItem[] => {
    if (_.isUndefined(data) || _.isNull(data)) {
      return [];
    }

    return data.root.gitEnvironmentUrls.map(
      (gitEnvironment: IBasicEnvironmentUrl): IEnvironmentUrlItem => {
        return {
          ...gitEnvironment,
          element: (
            <ConfirmDialog title={t("group.scope.git.removeEnvironment.title")}>
              {(confirm): JSX.Element => {
                return (
                  <Button
                    disabled={loading || isRemoving}
                    id={"git-root-remove-environment-url"}
                    onClick={onConfirmDelete(confirm, gitEnvironment)}
                    variant={"secondary"}
                  >
                    <FontAwesomeIcon icon={faTrashAlt} />
                  </Button>
                );
              }}
            </ConfirmDialog>
          ),
        };
      }
    );
  }, [data, isRemoving, loading, onConfirmDelete, t]);

  return (
    <Fragment>
      <Table
        columnVisibilitySetter={setColumnVisibility}
        columnVisibilityState={columnVisibility}
        columns={[
          {
            accessorKey: "url",
            header: String(t("group.scope.git.envUrl")),
          },
          {
            accessorKey: "urlType",
            header: String(t("group.scope.git.envUrlType")),
          },
          {
            accessorKey: "element",
            cell: (cell: ICellHelper<IEnvironmentUrlItem>): JSX.Element =>
              cell.getValue(),
            header: "",
          },
        ]}
        data={gitEnvironmentUrls}
        id={"tblGitRootSecrets"}
      />

      <Modal
        onClose={closeAddModal}
        open={isAddEnvModalOpen}
        title={t("group.scope.git.addEnvUrl")}
      >
        <AddEnvironment
          closeFunction={closeAddModal}
          groupName={groupName}
          rootId={rootInitialValues.id}
        />
      </Modal>
      <ModalConfirm
        id={"add-env-url"}
        onCancel={onClose}
        onConfirm={openAddModal}
        txtConfirm={t("group.scope.git.addEnvUrl")}
      />
    </Fragment>
  );
};

export { Environments };
