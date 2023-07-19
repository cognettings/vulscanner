import {
  faBook,
  faEnvelope,
  faGraduationCap,
  faHeadset,
  faMessage,
  faQuestionCircle,
} from "@fortawesome/free-solid-svg-icons";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { HelpOption } from "./help-option";
import { LearningModal } from "./learning-modal";
import { TalkToHackerModal } from "./talk-to-a-hacker";

import { Button } from "components/Button";
import { Dropdown } from "components/Dropdown";
import { ExternalLink } from "components/ExternalLink";
import { UpgradeGroupsModal } from "features/upgrade-groups-modal";
import { useCalendly } from "hooks";
import { toggleZendesk } from "utils/widgets";

const HelpButton: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const {
    closeUpgradeModal,
    isAvailable,
    isSquadActive,
    isUpgradeOpen,
    openUpgradeModal,
  } = useCalendly();

  const [isLearningModalOpen, setIsLearningModalOpen] = useState(false);
  const [isTalkToHackerModalOpen, setIsTalkToHackerModalOpen] = useState(false);

  const openLearningModal = useCallback((): void => {
    setIsLearningModalOpen(true);
  }, []);
  const closeLearningModal = useCallback((): void => {
    setIsLearningModalOpen(false);
  }, []);

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
    <Dropdown
      align={"left"}
      button={
        <Button icon={faQuestionCircle} size={"md"} variant={"primary"}>
          {t("components.navBar.help")}
        </Button>
      }
      id={"navbar-help-options"}
    >
      <div>
        {isAvailable ? (
          <HelpOption
            description={t("navbar.help.options.expert.description")}
            icon={faHeadset}
            onClick={openTalkToHackerModal}
            title={t("navbar.help.options.expert.title")}
          />
        ) : (
          <div />
        )}
        {isUpgradeOpen ? (
          <UpgradeGroupsModal onClose={closeUpgradeModal} />
        ) : undefined}
        <HelpOption
          description={t("navbar.help.options.chat.description")}
          icon={faMessage}
          onClick={toggleZendesk}
          title={t("navbar.help.options.chat.title")}
        />
        <HelpOption
          description={t("navbar.help.options.learn.description")}
          icon={faGraduationCap}
          onClick={openLearningModal}
          title={t("navbar.help.options.learn.title")}
        />
        <ExternalLink href={"mailto:help@fluidattacks.com"}>
          <HelpOption
            description={t("navbar.help.options.mail.description")}
            icon={faEnvelope}
            title={t("navbar.help.options.mail.title")}
          />
        </ExternalLink>
        <ExternalLink href={"https://docs.fluidattacks.com/"}>
          <HelpOption
            description={t("navbar.help.options.docs.description")}
            icon={faBook}
            title={t("navbar.help.options.docs.title")}
          />
        </ExternalLink>
      </div>
      {isLearningModalOpen ? (
        <LearningModal closeLearningModal={closeLearningModal} />
      ) : undefined}
      {isTalkToHackerModalOpen ? (
        <TalkToHackerModal closeTalkToHackerModal={closeTalkToHackerModal} />
      ) : undefined}
    </Dropdown>
  );
};

export { HelpButton };
