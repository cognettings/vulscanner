import { Form, Formik } from "formik";
import _ from "lodash";
import React, { Fragment, StrictMode } from "react";
import { useTranslation } from "react-i18next";
import type { TestContext, ValidationError } from "yup";
import { object, string } from "yup";

import { TextArea } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";

interface IAddRemediationProps {
  additionalInfo?: string;
  children?: React.ReactNode;
  isLoading: boolean;
  isOpen: boolean;
  maxJustificationLength?: number;
  message: string;
  title: string;
  onClose: () => void;
  onSubmit: (values: { treatmentJustification: string }) => void;
}

const MAX_TREATMENT_JUSTIFICATION_LENGTH: number = 10000;
const MIN_TREATMENT_JUSTIFICATION_LENGTH: number = 10;

const RemediationModal: React.FC<Readonly<IAddRemediationProps>> = ({
  additionalInfo,
  children,
  isLoading,
  isOpen,
  message,
  title,
  onClose,
  onSubmit,
}): JSX.Element => {
  const { t } = useTranslation();

  const validations = object().shape({
    treatmentJustification: string()
      .required(t("validations.required"))
      .min(
        MIN_TREATMENT_JUSTIFICATION_LENGTH,
        t("validations.minLength", {
          count: MIN_TREATMENT_JUSTIFICATION_LENGTH,
        })
      )
      .max(
        MAX_TREATMENT_JUSTIFICATION_LENGTH,
        t("validations.maxLength", {
          count: MAX_TREATMENT_JUSTIFICATION_LENGTH,
        })
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
  });

  return (
    <StrictMode>
      <Modal minWidth={450} onClose={onClose} open={isOpen} title={title}>
        <Formik
          initialValues={{
            treatmentJustification: "",
          }}
          name={"updateRemediation"}
          onSubmit={onSubmit}
          validationSchema={validations}
        >
          {({ dirty }): JSX.Element => (
            <Form>
              <Fragment>
                {children}
                <TextArea
                  count={true}
                  label={message}
                  name={"treatmentJustification"}
                  required={true}
                  rows={6}
                />
                {additionalInfo}
                <ModalConfirm
                  disabled={!dirty || isLoading}
                  id={"remediation-confirm"}
                  onCancel={onClose}
                />
              </Fragment>
            </Form>
          )}
        </Formik>
      </Modal>
    </StrictMode>
  );
};

export type { IAddRemediationProps };
export { RemediationModal };
