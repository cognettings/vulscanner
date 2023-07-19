import { Form, Formik } from "formik";
import type { FC, ReactNode } from "react";
import React, { StrictMode } from "react";
import { useTranslation } from "react-i18next";

import { addFilesModalSchema } from "./validations";

import { Alert } from "components/Alert";
import { InputFile, TextArea } from "components/Input";
import { Gap } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import type { IAddFilesModalProps } from "scenes/Dashboard/components/AddFilesModal/types";

const AddFilesModal: FC<IAddFilesModalProps> = ({
  isOpen,
  isUploading,
  onClose,
  onSubmit,
}: IAddFilesModalProps): JSX.Element => {
  const { t } = useTranslation();

  const initialValues = {
    description: "",
    file: undefined as unknown as FileList,
  };

  return (
    <StrictMode>
      <Modal
        minWidth={400}
        onClose={onClose}
        open={isOpen}
        title={t("searchFindings.tabResources.modalFileTitle")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={initialValues}
          name={"addFiles"}
          onSubmit={onSubmit}
          validationSchema={addFilesModalSchema}
        >
          {({ dirty }): ReactNode => (
            <Form>
              <Gap disp={"block"} mh={0} mv={12}>
                <div>
                  <InputFile id={"file"} name={"file"} required={true} />
                </div>
                <div>
                  <TextArea
                    label={t("searchFindings.tabResources.description")}
                    name={"description"}
                    required={true}
                  />
                </div>
                {isUploading ? (
                  <Alert variant={"info"}>
                    {t("searchFindings.tabResources.uploadingProgress")}
                  </Alert>
                ) : undefined}
              </Gap>
              <ModalConfirm
                disabled={!dirty || isUploading}
                onCancel={onClose}
              />
            </Form>
          )}
        </Formik>
      </Modal>
    </StrictMode>
  );
};

export type { IAddFilesModalProps };
export { AddFilesModal };
