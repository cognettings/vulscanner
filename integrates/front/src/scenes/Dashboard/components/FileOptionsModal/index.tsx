import { faDownload, faMinus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import type { IConfirmFn } from "components/ConfirmDialog";
import { ConfirmDialog } from "components/ConfirmDialog";
import { ButtonToolbarCenter, Col, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";

interface IFileOptionsModalProps {
  canRemove: boolean;
  fileName: string;
  isOpen: boolean;
  onClose: () => void;
  onDelete: () => void;
  onDownload: () => void;
}

const FileOptionsModal: React.FC<IFileOptionsModalProps> = ({
  canRemove,
  fileName,
  isOpen,
  onClose,
  onDelete,
  onDownload,
}: IFileOptionsModalProps): JSX.Element => {
  const { t } = useTranslation();

  const onConfirmDelete = useCallback(
    (confirm: IConfirmFn): (() => void) =>
      (): void => {
        confirm((): void => {
          onDelete();
        });
      },
    [onDelete]
  );

  return (
    <React.StrictMode>
      <Modal
        onClose={onClose}
        open={isOpen}
        title={t("searchFindings.tabResources.modalOptionsTitle")}
      >
        <ConfirmDialog
          title={t("searchFindings.tabResources.files.confirm.title")}
        >
          {(confirm): JSX.Element => {
            return (
              <React.Fragment>
                <Row>
                  <Col>
                    <label>
                      {t("searchFindings.tabResources.modalOptionsContent")}
                      <b>{fileName}</b>
                      {"?"}
                    </label>
                  </Col>
                  <ButtonToolbarCenter>
                    <br />
                    {canRemove ? (
                      <Col>
                        <Button
                          onClick={onConfirmDelete(confirm)}
                          variant={"secondary"}
                        >
                          <FontAwesomeIcon icon={faMinus} />
                          &nbsp;
                          {t("searchFindings.tabResources.removeRepository")}
                        </Button>
                      </Col>
                    ) : undefined}
                    <Col>
                      <Button onClick={onDownload} variant={"secondary"}>
                        <FontAwesomeIcon icon={faDownload} />
                        &nbsp;
                        {t("searchFindings.tabResources.download")}
                      </Button>
                    </Col>
                  </ButtonToolbarCenter>
                </Row>
                <ModalConfirm onCancel={onClose} />
              </React.Fragment>
            );
          }}
        </ConfirmDialog>
      </Modal>
    </React.StrictMode>
  );
};

export { FileOptionsModal };
