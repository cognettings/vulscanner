import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { HandleAdditionModalForm } from "./form";
import { ADD_TOE_LINES, GET_GIT_ROOTS } from "./queries";
import type {
  IAddToeInputResultAttr,
  IFormValues,
  IGitRootAttr,
  IHandleAdditionModalProps,
} from "./types";
import { validations } from "./validations";

import { Modal } from "components/Modal";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const HandleAdditionModal: React.FC<IHandleAdditionModalProps> = ({
  isAdding,
  groupName,
  handleCloseModal,
  refetchData,
}: IHandleAdditionModalProps): JSX.Element => {
  const { t } = useTranslation();

  const { data: rootsData } = useQuery<{ group: { roots: IGitRootAttr[] } }>(
    GET_GIT_ROOTS,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load roots", error);
        });
      },
      variables: { groupName },
    }
  );
  const roots =
    rootsData === undefined
      ? []
      : rootsData.group.roots.filter(
          (root): boolean => root.state === "ACTIVE"
        );

  // GraphQL operations
  const [handleAddToeLines] = useMutation<IAddToeInputResultAttr>(
    ADD_TOE_LINES,
    {
      onCompleted: (data: IAddToeInputResultAttr): void => {
        if (data.addToeLines.success) {
          msgSuccess(
            t("group.toe.lines.addModal.alerts.success"),
            t("groupAlerts.titleSuccess")
          );
          refetchData();
          handleCloseModal();
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          if (error.message === "Exception - Toe lines already exists") {
            msgError(t("group.toe.lines.addModal.alerts.alreadyExists"));
          } else {
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning("An error occurred adding toe input", error);
          }
        });
      },
    }
  );

  const handleSubmit = useCallback(
    (values: IFormValues): void => {
      void handleAddToeLines({
        variables: {
          ...values,
          groupName,
          modifiedDate: values.modifiedDate?.toISOString(),
        },
      });
    },
    [groupName, handleAddToeLines]
  );

  return (
    <React.StrictMode>
      {rootsData === undefined ? undefined : (
        <Modal open={isAdding} title={t("group.toe.lines.addModal.title")}>
          <Formik
            initialValues={{
              filename: "",
              lastAuthor: "",
              lastCommit: "",
              loc: "" as unknown as number,
              modifiedDate: "" as unknown as Date,
              rootId: _.isEmpty(roots) ? "" : roots[0].id,
            }}
            name={"addToeLines"}
            onSubmit={handleSubmit}
            validationSchema={validations}
          >
            <HandleAdditionModalForm
              handleCloseModal={handleCloseModal}
              roots={roots}
            />
          </Formik>
        </Modal>
      )}
    </React.StrictMode>
  );
};

export { HandleAdditionModal };
