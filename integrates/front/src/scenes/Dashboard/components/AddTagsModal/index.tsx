import { Form, Formik } from "formik";
import _ from "lodash";
import type { FC } from "react";
import React, { Fragment, StrictMode } from "react";
import { useTranslation } from "react-i18next";
import { array, object, string } from "yup";

import { Input, InputArray, Label } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";

interface IAddTagsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { tags: string[] }) => void;
}

function renderTagsFields(fieldName: string): JSX.Element {
  return (
    <Fragment>
      <Label required={true}>{"Tag"}</Label>
      <Input name={fieldName} type={"text"} />
    </Fragment>
  );
}

const AddTagsModal: FC<IAddTagsModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
}: IAddTagsModalProps): JSX.Element => {
  const { t } = useTranslation();

  const validations = object().shape({
    tags: array().of(
      string()
        .required(t("validations.required"))
        .test("validTag", t("validations.tags"), (value): boolean => {
          if (value === undefined) {
            return false;
          }
          const pattern: RegExp = /^[a-z0-9]+(?:-[a-z0-9]+)*$/u;

          return !_.isEmpty(value) || pattern.test(value);
        })
    ),
  });

  return (
    <StrictMode>
      <Modal
        minWidth={400}
        onClose={onClose}
        open={isOpen}
        title={t("searchFindings.tabIndicators.tags.modalTitle")}
      >
        <Formik
          initialValues={{
            tags: [""],
          }}
          name={"addTags"}
          onSubmit={onSubmit}
          validationSchema={validations}
        >
          {({ dirty }): JSX.Element => (
            <Form>
              <InputArray initValue={""} name={"tags"}>
                {renderTagsFields}
              </InputArray>
              <ModalConfirm
                disabled={!dirty}
                id={"portfolio-add-confirm"}
                onCancel={onClose}
              />
            </Form>
          )}
        </Formik>
      </Modal>
    </StrictMode>
  );
};

export type { IAddTagsModalProps };
export { AddTagsModal };
