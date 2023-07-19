import { Form, Formik } from "formik";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Alert } from "components/Alert";
import { Input, Label } from "components/Input";
import { FormGroup } from "components/Input/styles";
import { Modal, ModalConfirm } from "components/Modal";

interface IUnsubscribeModalProps {
  groupName: string;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { confirmation: string }) => void;
}

const UnsubscribeModal: React.FC<IUnsubscribeModalProps> = (
  props: IUnsubscribeModalProps
): JSX.Element => {
  const { groupName, isOpen, onClose, onSubmit } = props;
  const { t } = useTranslation();

  const formValidations: (values: { confirmation: string }) => {
    confirmation?: string;
  } = useCallback(
    (values: { confirmation: string }): { confirmation?: string } => {
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
    confirmation: string().required(t("validations.required")),
  });

  return (
    <React.StrictMode>
      <Modal
        open={isOpen}
        title={t("searchFindings.servicesTable.unsubscribe.title")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{
            confirmation: "",
          }}
          name={"unsubscribeFromGroup"}
          onSubmit={onSubmit}
          validate={formValidations}
          validationSchema={validations}
        >
          {({ dirty, isValid, submitForm }): JSX.Element => (
            <Form id={"unsubscribeFromGroup"}>
              <Label>
                {t("searchFindings.servicesTable.unsubscribe.warningTitle")}
              </Label>
              <Alert>
                {t("searchFindings.servicesTable.unsubscribe.warningBody")}
              </Alert>
              <FormGroup>
                <Input
                  label={t(
                    "searchFindings.servicesTable.unsubscribe.typeGroupName"
                  )}
                  name={"confirmation"}
                  placeholder={groupName.toLowerCase()}
                  type={"text"}
                />
              </FormGroup>
              <ModalConfirm
                disabled={!isValid || !dirty}
                onCancel={onClose}
                onConfirm={submitForm}
              />
            </Form>
          )}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export type { IUnsubscribeModalProps };
export { UnsubscribeModal };
