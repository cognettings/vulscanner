import React, { useCallback } from "react";

import { NewRepository } from "./NewRepository";

import type { IFormValues } from "../../../types";
import type { IConfirmFn } from "components/ConfirmDialog";

interface IUpdateRepositoryProps {
  confirm: IConfirmFn;
  initialValues: IFormValues | undefined;
  isEditing: boolean;
  manyRows: boolean | undefined;
  modalMessages: { message: string; type: string };
  onClose: () => void;
  onSubmitRepo: (values: IFormValues) => Promise<void>;
  runTour: boolean;
  finishTour: () => void;
}

export const Repository: React.FC<IUpdateRepositoryProps> = ({
  confirm,
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
  finishTour,
  manyRows,
  modalMessages,
  onClose,
  onSubmitRepo,
  runTour,
}: IUpdateRepositoryProps): JSX.Element => {
  const confirmAndSubmit = useCallback(
    async (values: IFormValues): Promise<void> => {
      if (isEditing && values.branch !== initialValues.branch) {
        return new Promise((resolve): void => {
          confirm(
            (): void => {
              resolve(onSubmitRepo(values));
            },
            (): void => {
              resolve();
            }
          );
        });
      }

      return onSubmitRepo(values);
    },
    [confirm, initialValues.branch, isEditing, onSubmitRepo]
  );

  return (
    <NewRepository
      finishTour={finishTour}
      initialValues={initialValues}
      isEditing={isEditing}
      manyRows={manyRows}
      modalMessages={modalMessages}
      onClose={onClose}
      onSubmit={confirmAndSubmit}
      runTour={runTour}
    />
  );
};
