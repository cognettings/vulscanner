import { faHeadset } from "@fortawesome/free-solid-svg-icons";
import React, { useCallback, useState } from "react";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Col, Row } from "components/Layout";
import { UpgradeGroupsModal } from "features/upgrade-groups-modal";
import { useCalendly } from "hooks";
import { TalkToHackerModal } from "pages/home/dashboard/navbar/help-button/talk-to-a-hacker";

const ExpertButton: FC = (): JSX.Element => {
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
    <div>
      {isAvailable ? (
        <Container margin={"16px 0 0 0"} scroll={"none"}>
          <Row justify={"end"}>
            <Col>
              <Button
                disp={"inline-block"}
                icon={faHeadset}
                onClick={openTalkToHackerModal}
                variant={"primary"}
              >
                {t("navbar.help.options.expert.title")}
              </Button>
            </Col>
          </Row>
        </Container>
      ) : (
        <div />
      )}
      {isUpgradeOpen ? (
        <UpgradeGroupsModal onClose={closeUpgradeModal} />
      ) : (
        <div />
      )}
      {isTalkToHackerModalOpen ? (
        <TalkToHackerModal closeTalkToHackerModal={closeTalkToHackerModal} />
      ) : undefined}
    </div>
  );
};

export { ExpertButton };
