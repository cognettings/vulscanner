import {
  faComment,
  faEnvelope,
  faExternalLinkAlt,
  faHeadset,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { StrictMode, useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";

import { TalkToHackerModal } from "../help-button/talk-to-a-hacker";
import { Button } from "components/Button";
import { Card } from "components/Card";
import { ExternalLink } from "components/ExternalLink";
import { Col, Row } from "components/Layout";
import type { IModalProps } from "components/Modal";
import { Modal } from "components/Modal";
import { Text } from "components/Text";
import { UpgradeGroupsModal } from "features/upgrade-groups-modal";
import { useCalendly } from "hooks";
import { toggleZendesk } from "utils/widgets";

type IHelpModalProps = Pick<IModalProps, "onClose" | "open">;
const HelpLink = styled(ExternalLink)`
  display: inline;
`;

const HelpBlockLink = styled(ExternalLink)`
  display: block;
`;

const HelpModal: React.FC<IHelpModalProps> = ({
  onClose,
  open,
}): JSX.Element => {
  const { t } = useTranslation();
  const {
    closeUpgradeModal,
    isAvailable,
    isSquadActive,
    isUpgradeOpen,
    openUpgradeModal,
  } = useCalendly();
  const [isTalkToHackerModalOpen, setIsTalkToHackerModalOpen] = useState(false);

  const openTalkToHackerModal = useCallback((): void => {
    if (isSquadActive) {
      setIsTalkToHackerModalOpen(true);
    } else {
      openUpgradeModal();
    }
  }, [isSquadActive, openUpgradeModal]);
  const closeTalkToHackerModal = useCallback((): void => {
    setIsTalkToHackerModalOpen(false);
  }, []);

  return (
    <StrictMode>
      <Modal onClose={onClose} open={open} title={t("navbar.help.support")}>
        <Row cols={3}>
          <Col>
            <Card>
              <div>
                <Button onClick={toggleZendesk} size={"lg"}>
                  <FontAwesomeIcon icon={faComment} />
                  &nbsp;
                  {t("navbar.help.chat")}
                </Button>
              </div>
              <Text disp={"inline"}>{t("navbar.help.extra.chat")}</Text>
              <HelpLink
                href={
                  "https://docs.fluidattacks.com/machine/platform/support/live-chat"
                }
              >
                <Button
                  id={"liveChat"}
                  size={"xs"}
                  tooltip={t("navbar.help.tooltip")}
                >
                  <FontAwesomeIcon icon={faExternalLinkAlt} />
                </Button>
              </HelpLink>
            </Card>
          </Col>
          {isAvailable ? (
            <Col>
              <Card>
                <div>
                  <Button onClick={openTalkToHackerModal} size={"lg"}>
                    <FontAwesomeIcon icon={faHeadset} />
                    &nbsp;
                    {t("navbar.help.expert")}
                  </Button>
                </div>
                {isUpgradeOpen ? (
                  <UpgradeGroupsModal onClose={closeUpgradeModal} />
                ) : undefined}
                <Text disp={"inline"}>{t("navbar.help.extra.expert")}</Text>
                <HelpLink
                  href={
                    "https://docs.fluidattacks.com/squad/support/talk-hacker"
                  }
                >
                  <Button
                    id={"talkExpert"}
                    size={"xs"}
                    tooltip={t("navbar.help.tooltip")}
                  >
                    <FontAwesomeIcon icon={faExternalLinkAlt} />
                  </Button>
                </HelpLink>
              </Card>
            </Col>
          ) : (
            <StrictMode />
          )}
          {isTalkToHackerModalOpen ? (
            <TalkToHackerModal
              closeTalkToHackerModal={closeTalkToHackerModal}
            />
          ) : undefined}
          <Col lg={3} md={3} sm={3}>
            <Card>
              <HelpBlockLink href={"mailto:help@fluidattacks.com"}>
                <Button size={"lg"}>
                  <FontAwesomeIcon icon={faEnvelope} />
                  &nbsp;
                  {"help@fluidattacks.com"}
                </Button>
              </HelpBlockLink>
              <Text disp={"inline"}>{t("navbar.help.extra.mail")}</Text>
              <HelpLink
                href={
                  "https://docs.fluidattacks.com/about/security/transparency/help-channel"
                }
              >
                <Button
                  id={"helpChannel"}
                  size={"xs"}
                  tooltip={t("navbar.help.tooltip")}
                >
                  <FontAwesomeIcon icon={faExternalLinkAlt} />
                </Button>
              </HelpLink>
            </Card>
          </Col>
        </Row>
      </Modal>
    </StrictMode>
  );
};

export { HelpModal };
