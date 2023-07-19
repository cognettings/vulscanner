import { faCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { useConfirmDialog } from "components/confirm-dialog";
import { Col, Row } from "components/Layout";
import { Tag } from "components/Tag";
import { DisplayImage } from "scenes/Dashboard/components/EvidenceImage/DisplayImage";
import { EvidenceForm } from "scenes/Dashboard/components/EvidenceImage/EvidenceForm";
import {
  DescriptionContainer,
  EvidenceDescription,
  ImageContainer,
} from "scenes/Dashboard/components/EvidenceImage/styles";

interface IEvidenceImageProps {
  acceptedMimes?: string;
  content: string;
  date?: string;
  description: string;
  isDescriptionEditable: boolean;
  isDraft?: boolean;
  isEditing: boolean;
  isRemovable?: boolean;
  name: string;
  validate?: (value: unknown) => string | undefined;
  onApprove?: () => void;
  onClick: () => void;
  onDelete?: () => void;
}

const getFileNameExtension: (filename: string) => string = (
  filename: string
): string => {
  const splittedName: string[] = filename.split(".");
  const extension: string =
    splittedName.length > 1 ? (_.last(splittedName) as string) : "";

  return extension.toLowerCase();
};

const EvidenceImage: React.FC<Readonly<IEvidenceImageProps>> = (
  props
): JSX.Element => {
  const {
    content,
    isDraft,
    isEditing,
    description,
    date,
    name,
    onApprove,
    onClick,
  } = props;
  const { t } = useTranslation();

  const { confirm, ConfirmDialog } = useConfirmDialog();
  const confirmApproval = useCallback(async (): Promise<void> => {
    const confirmResult = await confirm({
      title: t("searchFindings.tabEvidence.approvalConfirm"),
    });

    if (confirmResult) {
      onApprove?.();
    }
  }, [confirm, onApprove, t]);

  return (
    <React.Fragment>
      <Col lg={33} md={50} sm={100}>
        <div>
          <ImageContainer>
            <DisplayImage
              content={content}
              extension={getFileNameExtension(content)}
              name={name}
              onClick={onClick}
            />
          </ImageContainer>
          <DescriptionContainer>
            <Row>
              <label>
                <b>{t("searchFindings.tabEvidence.detail")}</b>
              </label>
            </Row>
            <Row>
              {isEditing ? (
                // eslint-disable-next-line react/jsx-props-no-spreading
                <EvidenceForm {...props} />
              ) : (
                <React.Fragment>
                  <EvidenceDescription>{description}</EvidenceDescription>
                  {_.isEmpty(date) ? undefined : (
                    <EvidenceDescription>
                      {t("searchFindings.tabEvidence.date")}&nbsp;
                      {date?.split(" ")[0]}
                    </EvidenceDescription>
                  )}
                  {isDraft === true ? (
                    <Col>
                      <Tag variant={"gray"}>{"Draft"}</Tag>
                    </Col>
                  ) : undefined}
                </React.Fragment>
              )}
            </Row>
            {isDraft === true && onApprove ? (
              <Row>
                <Col lg={40} md={40} sm={40}>
                  <Button onClick={confirmApproval} variant={"secondary"}>
                    <FontAwesomeIcon icon={faCheck} />
                    &nbsp;{t("searchFindings.tabEvidence.approve")}
                  </Button>
                </Col>
              </Row>
            ) : undefined}
          </DescriptionContainer>
        </div>
      </Col>
      <ConfirmDialog />
    </React.Fragment>
  );
};

export { EvidenceImage };
export type { IEvidenceImageProps };
