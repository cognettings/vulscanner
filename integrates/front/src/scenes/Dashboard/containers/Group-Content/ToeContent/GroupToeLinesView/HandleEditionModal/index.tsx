import type { ApolloError, FetchResult } from "@apollo/client";
import { useMutation } from "@apollo/client";
import dayjs from "dayjs";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _, { min } from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { TestContext, ValidationError } from "yup";
import { number, object, string } from "yup";

import { HandleEditionModalForm } from "./form";
import { UPDATE_TOE_LINES_ATTACKED_LINES } from "./queries";
import type {
  IFormValues,
  IHandleEditionModalProps,
  IUpdateToeLinesAttackedLinesResultAttr,
} from "./types";

import type { IToeLinesData } from "../types";
import { Modal } from "components/Modal";
import { getErrors } from "utils/helpers";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const HandleEditionModal: React.FC<IHandleEditionModalProps> = ({
  groupName,
  selectedToeLinesDatas,
  handleCloseModal,
  refetchData,
  setSelectedToeLinesDatas,
}: IHandleEditionModalProps): JSX.Element => {
  const { t } = useTranslation();

  const isOneSelected = selectedToeLinesDatas.length === 1;

  // GraphQL operations
  const [handleUpdateToeLinesAttackedLines] =
    useMutation<IUpdateToeLinesAttackedLinesResultAttr>(
      UPDATE_TOE_LINES_ATTACKED_LINES,
      {
        onError: (errors: ApolloError): void => {
          errors.graphQLErrors.forEach((error: GraphQLError): void => {
            switch (error.message) {
              case "Exception - The attack time must be between the previous attack and the current time":
                msgError(
                  t("group.toe.lines.editModal.alerts.invalidAttackedAt")
                );
                break;
              case "Exception - The attacked lines must be between 0 and the loc (lines of code)":
                msgError(
                  t("group.toe.lines.editModal.alerts.invalidAttackedLines")
                );
                break;
              case "Exception - The toe lines has been updated by another operation":
                msgError(t("group.toe.lines.editModal.alerts.alreadyUpdate"));
                break;
              default:
                msgError(t("groupAlerts.errorTextsad"));
                Logger.warning(
                  "An error occurred updating the toe lines attacked lines",
                  error
                );
            }
          });
        },
      }
    );

  const handleOnCompleted = useCallback(
    (result: FetchResult<IUpdateToeLinesAttackedLinesResultAttr>): void => {
      if (
        !_.isNil(result.data) &&
        result.data.updateToeLinesAttackedLines.success
      ) {
        msgSuccess(
          t("group.toe.lines.editModal.alerts.success"),
          t("groupAlerts.updatedTitle")
        );
        refetchData();
        setSelectedToeLinesDatas([]);
        handleCloseModal();
      }
    },
    [handleCloseModal, refetchData, setSelectedToeLinesDatas, t]
  );

  const handleSubmit = useCallback(
    async (values: IFormValues): Promise<void> => {
      const results = await Promise.all(
        selectedToeLinesDatas.map(
          async (
            toeInputData: IToeLinesData
          ): Promise<FetchResult<IUpdateToeLinesAttackedLinesResultAttr>> =>
            handleUpdateToeLinesAttackedLines({
              variables: {
                attackedLines: _.isNumber(values.attackedLines)
                  ? values.attackedLines
                  : undefined,
                comments: values.comments,
                filename: toeInputData.filename,
                groupName,
                rootId: toeInputData.rootId,
              },
            })
        )
      );
      const errors = getErrors<IUpdateToeLinesAttackedLinesResultAttr>(results);

      if (!_.isEmpty(results) && _.isEmpty(errors)) {
        handleOnCompleted(results[0]);
      } else {
        refetchData();
      }
    },
    [
      groupName,
      handleOnCompleted,
      handleUpdateToeLinesAttackedLines,
      refetchData,
      selectedToeLinesDatas,
    ]
  );

  const maxSelectedLoc: number =
    min(
      selectedToeLinesDatas.map(
        (toeLinesData: IToeLinesData): number => toeLinesData.loc
      )
    ) ?? 1;

  const MAX_COMMENTS_LENGTH: number = 200;

  const validations = object().shape({
    attackedLines: number()
      .test(
        "isOptionalInteger",
        translate.t("validations.integer"),
        (value): boolean => {
          return _.isInteger(value) || (_.isString(value) && _.isEmpty(value));
        }
      )
      .test(
        "optionalNumberBetween",
        translate.t("validations.between", { max: maxSelectedLoc, min: 0 }),
        (value): boolean => {
          return _.isNumber(value) && value >= 0 && value <= maxSelectedLoc;
        }
      ),
    comments: string()
      .max(
        MAX_COMMENTS_LENGTH,
        translate.t("validations.maxLength", { count: MAX_COMMENTS_LENGTH })
      )
      .test({
        exclusive: false,
        name: "invalidTextBeginning",
        params: {},
        test: (
          value: string | undefined,
          thisContext: TestContext
        ): ValidationError | boolean => {
          if (value === undefined) {
            return false;
          }
          const beginTextMatch: RegExpMatchArray | null =
            /^=|^-|^\+|^@|^\t|^\r/u.exec(value);

          return _.isNull(beginTextMatch)
            ? true
            : thisContext.createError({
                message: translate.t("validations.invalidTextBeginning", {
                  chars: `'${beginTextMatch[0]}'`,
                }),
              });
        },
      })
      .test({
        exclusive: false,
        name: "invalidTextPattern",
        params: {},
        test: (
          value: string | undefined,
          thisContext: TestContext
        ): ValidationError | boolean => {
          if (value === undefined) {
            return false;
          }
          const contentTextMatch: RegExpMatchArray | null =
            /["',;](?:[-=+@\t\r])/u.exec(value);

          return _.isNull(contentTextMatch)
            ? true
            : thisContext.createError({
                message: translate.t("validations.invalidTextPattern", {
                  chars: `'${contentTextMatch[0]}'`,
                }),
              });
        },
      })
      .test({
        exclusive: false,
        name: "invalidTextField",
        params: {},
        test: (
          value: string | undefined,
          thisContext: TestContext
        ): ValidationError | boolean => {
          if (value === undefined) {
            return false;
          }
          const textMatch: RegExpMatchArray | null =
            /[^a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s(){}[\],./:;@&_$%'#*=¿?¡!+-]/u.exec(
              value
            );

          return _.isNull(textMatch)
            ? true
            : thisContext.createError({
                message: translate.t("validations.invalidTextField", {
                  chars: `'${textMatch[0]}'`,
                }),
              });
        },
      }),
  });

  return (
    <React.StrictMode>
      <Modal open={true} title={t("group.toe.lines.editModal.title")}>
        <Formik
          initialValues={{
            attackedAt: dayjs(),
            attackedLines: isOneSelected ? selectedToeLinesDatas[0].loc : "",
            comments: "",
          }}
          name={"updateToeLinesAttackedLines"}
          onSubmit={handleSubmit}
          validationSchema={validations}
        >
          <HandleEditionModalForm
            handleCloseModal={handleCloseModal}
            selectedToeLinesDatas={selectedToeLinesDatas}
          />
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { HandleEditionModal };
