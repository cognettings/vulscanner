import { Formik } from "formik";
import _ from "lodash";
import type { FC } from "react";
import React, { Fragment, StrictMode, useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { TestContext, ValidationError } from "yup";
import { object, string } from "yup";

import { Alert } from "components/Alert";
import { Input, Label, Select, TextArea } from "components/Input";
import { Row } from "components/Layout/Row";
import { Modal, ModalConfirm } from "components/Modal";

const MAX_LENGTH_VALIDATOR = 250;

interface IDeleteGroupModalProps {
  groupName: string;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: {
    comments: string;
    confirmation: string;
    reason: string;
  }) => void;
}

const DeleteGroupModal: FC<IDeleteGroupModalProps> = ({
  groupName,
  isOpen,
  onClose,
  onSubmit,
}: IDeleteGroupModalProps): JSX.Element => {
  const { t } = useTranslation();

  const formValidations = useCallback(
    (values: {
      confirmation: string;
      reason: string;
    }): {
      confirmation?: string;
      reason?: string;
    } => {
      return values.confirmation === groupName
        ? {}
        : {
            confirmation: t(
              "searchFindings.servicesTable.errors.expectedGroupName",
              { groupName }
            ),
          };
    },
    [groupName, t]
  );

  const validations = object().shape({
    comments: string()
      .max(
        MAX_LENGTH_VALIDATOR,
        t("validations.maxLength", { count: MAX_LENGTH_VALIDATOR })
      )
      .test({
        exclusive: false,
        name: "invalidTextBeginning",
        test: (
          value: string | undefined,
          thisContext: TestContext
        ): ValidationError | boolean => {
          if (value === undefined) {
            return false;
          }
          const beginTextMatch: RegExpMatchArray | null = /^=/u.exec(value);

          return _.isNull(beginTextMatch)
            ? true
            : thisContext.createError({
                message: t("validations.invalidTextBeginning", {
                  chars: `'${beginTextMatch[0]}'`,
                }),
              });
        },
      })
      .test({
        exclusive: false,
        name: "invalidTextField",
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
                message: t("validations.invalidTextField", {
                  chars: `'${textMatch[0]}'`,
                }),
              });
        },
      }),
    confirmation: string().required(t("validations.required")),
  });

  return (
    <StrictMode>
      <Modal
        open={isOpen}
        title={t("searchFindings.servicesTable.deleteGroup.deleteGroup")}
      >
        <Formik
          initialValues={{
            comments: "",
            confirmation: "",
            reason: "NO_SYSTEM",
          }}
          name={"removeGroup"}
          onSubmit={onSubmit}
          validate={formValidations}
          validationSchema={validations}
        >
          {({ submitForm, isValid, dirty }): JSX.Element => (
            <Fragment>
              <Row>
                <Label>
                  {t("searchFindings.servicesTable.deleteGroup.warningTitle")}
                </Label>
                <Alert>
                  {t("searchFindings.servicesTable.deleteGroup.warningBody")}
                </Alert>
                <Label>
                  {t("searchFindings.servicesTable.deleteGroup.typeGroupName")}
                </Label>
              </Row>
              <Row>
                <Input
                  name={"confirmation"}
                  placeholder={groupName.toLowerCase()}
                  type={"text"}
                />
              </Row>
              <Row>
                <Select
                  label={t(
                    "searchFindings.servicesTable.deleteGroup.reason.title"
                  )}
                  name={"reason"}
                  tooltip={t(
                    "searchFindings.servicesTable.deleteGroup.reason.tooltip"
                  )}
                >
                  <option value={"NO_SYSTEM"}>
                    {t(
                      "searchFindings.servicesTable.deleteGroup.reason.noSystem"
                    )}
                  </option>
                  <option value={"NO_SECTST"}>
                    {t(
                      "searchFindings.servicesTable.deleteGroup.reason.noSectst"
                    )}
                  </option>
                  <option value={"DIFF_SECTST"}>
                    {t(
                      "searchFindings.servicesTable.deleteGroup.reason.diffSectst"
                    )}
                  </option>
                  <option value={"RENAME"}>
                    {t(
                      "searchFindings.servicesTable.deleteGroup.reason.rename"
                    )}
                  </option>
                  <option value={"MIGRATION"}>
                    {" "}
                    {t(
                      "searchFindings.servicesTable.deleteGroup.reason.migration"
                    )}
                  </option>
                  <option value={"POC_OVER"}>
                    {t(
                      "searchFindings.servicesTable.deleteGroup.reason.pocOver"
                    )}
                  </option>
                  <option value={"TR_CANCELLED"}>
                    {t(
                      "searchFindings.servicesTable.deleteGroup.reason.trCancelled"
                    )}
                  </option>
                  <option value={"MISTAKE"}>
                    {t(
                      "searchFindings.servicesTable.deleteGroup.reason.mistake"
                    )}
                  </option>
                  <option value={"OTHER"}>
                    {t("searchFindings.servicesTable.deleteGroup.reason.other")}
                  </option>
                </Select>
              </Row>
              <Row>
                <TextArea
                  label={t("searchFindings.servicesTable.modal.observations")}
                  name={"comments"}
                  placeholder={t(
                    "searchFindings.servicesTable.modal.observationsPlaceholder"
                  )}
                />
              </Row>
              <ModalConfirm
                disabled={!dirty || !isValid}
                onCancel={onClose}
                onConfirm={submitForm}
              />
            </Fragment>
          )}
        </Formik>
      </Modal>
    </StrictMode>
  );
};

export { DeleteGroupModal };
