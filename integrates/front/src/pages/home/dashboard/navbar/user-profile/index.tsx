import { useMutation } from "@apollo/client";
import {
  faKey,
  faMessage,
  faMobileAlt,
  faSignOutAlt,
  faUser,
  faUserCog,
  faUserPlus,
  faUserTimes,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useContext, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useHistory } from "react-router-dom";
import styled from "styled-components";

import { AccessTokenModal } from "./api-token-modal";
import { useAddStakeholder } from "./hooks";
import { MobileModal } from "./mobile-modal";
import { REMOVE_STAKEHOLDER_MUTATION } from "./queries";
import { Role } from "./role";
import type { IRemoveStakeholderAttr } from "./types";

import { Alert } from "components/Alert";
import { Button } from "components/Button";
import { useConfirmDialog } from "components/confirm-dialog";
import { Dropdown } from "components/Dropdown";
import { ExternalLink } from "components/ExternalLink";
import { Label } from "components/Input";
import { Hr } from "components/Layout";
import { Switch } from "components/Switch";
import { Text } from "components/Text";
import { authContext } from "context/auth";
import { Can } from "context/authz/Can";
import type { IFeaturePreviewContext } from "context/featurePreview";
import { featurePreviewContext } from "context/featurePreview";
import type { IMeetingModeContext } from "context/meetingMode";
import { meetingModeContext } from "context/meetingMode";
import { AddUserModal } from "features/add-user-modal";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const SpeakUpLink = styled(ExternalLink)`
  display: block;
  padding-left: 0px;

  > button {
    width: 100%;
  }
`;

const UserProfile: React.FC = (): JSX.Element => {
  const { userEmail, userName, userIntPhone } = useContext(authContext);
  const { t } = useTranslation();
  const { push } = useHistory();

  const { featurePreview, setFeaturePreview } = useContext(
    featurePreviewContext as React.Context<Required<IFeaturePreviewContext>>
  );
  const toggleFeaturePreview = useCallback((): void => {
    setFeaturePreview((currentValue): boolean => {
      mixpanel.track(`${currentValue ? "Disable" : "Enable"}FeaturePreview`);

      return !currentValue;
    });
  }, [setFeaturePreview]);

  const { meetingMode, setMeetingMode } = useContext(
    meetingModeContext as React.Context<Required<IMeetingModeContext>>
  );
  const toggleMeetingMode = useCallback((): void => {
    setMeetingMode((currentValue): boolean => {
      mixpanel.track(`${currentValue ? "Disable" : "Enable"}MeetingMode`);

      return !currentValue;
    });
  }, [setMeetingMode]);

  const [isMobileModalOpen, setIsMobileModalOpen] = useState(false);
  const [isTokenModalOpen, setIsTokenModalOpen] = useState(false);
  const openMobileModal = useCallback((): void => {
    setIsMobileModalOpen(true);
  }, []);
  const closeMobileModal = useCallback((): void => {
    setIsMobileModalOpen(false);
  }, []);
  const openTokenModal = useCallback((): void => {
    setIsTokenModalOpen(true);
  }, []);
  const closeTokenModal = useCallback((): void => {
    setIsTokenModalOpen(false);
  }, []);

  const [addStakeholder, isStakeholderModalOpen, setStakeholderModalOpen] =
    useAddStakeholder();
  const handleAddUserSubmit = useCallback(
    async ({ email, role }): Promise<void> => {
      await addStakeholder({ variables: { email, role } });
    },
    [addStakeholder]
  );
  const openStakeholderModal = useCallback((): void => {
    setStakeholderModalOpen(true);
  }, [setStakeholderModalOpen]);
  const closeStakeholderModal = useCallback((): void => {
    setStakeholderModalOpen(false);
  }, [setStakeholderModalOpen]);

  const [removeStakeholder] = useMutation(REMOVE_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IRemoveStakeholderAttr): void => {
      if (mtResult.removeStakeholder.success) {
        msgSuccess(
          t("navbar.deleteAccount.success"),
          t("navbar.deleteAccount.successTitle")
        );
      } else {
        push("/home");
      }
    },
    onError: (removeError): void => {
      removeError.graphQLErrors.forEach((error): void => {
        if (
          error.message ===
          "Exception - The previous invitation to this user was requested less than a minute ago"
        ) {
          msgError(t("navbar.deleteAccount.requestedTooSoon"));
        } else {
          Logger.error("An error occurred while deleting account", error);
          msgError(t("groupAlerts.errorTextsad"));
        }
      });
      push("/home");
    },
  });

  const { confirm, ConfirmDialog } = useConfirmDialog();

  const deleteAccount = useCallback(async (): Promise<void> => {
    const confirmResult = await confirm({
      message: (
        <React.Fragment>
          <Label>{t("navbar.deleteAccount.modal.warning")}</Label>
          <Alert>{t("navbar.deleteAccount.modal.text")}</Alert>
        </React.Fragment>
      ),
      title: t("navbar.deleteAccount.text"),
    });

    if (confirmResult) {
      await removeStakeholder();
    }
  }, [confirm, removeStakeholder, t]);

  const logout = useCallback(async (): Promise<void> => {
    const confirmResult = await confirm({ title: t("navbar.logout") });

    if (confirmResult) {
      mixpanel.reset();
      location.assign("/logout");
    }
  }, [confirm, t]);

  return (
    <Dropdown
      align={"left"}
      button={
        <Button icon={faUser} size={"md"}>
          {userName.split(" ")[0]}
        </Button>
      }
      id={"navbar-user-profile"}
    >
      <div className={"flex flex-column tl"}>
        <div className={"pa2"}>
          <Text bright={7} fw={7} mb={1}>
            {userName}
          </Text>
          <Text bright={7} mb={1}>
            {userEmail}
          </Text>
          {_.isUndefined(userIntPhone) ? undefined : (
            <Text bright={7} mb={1}>
              {t("navbar.mobile")}
              &nbsp;
              {userIntPhone}
            </Text>
          )}
          <Role />
          <Can do={"front_can_enable_meeting_mode"}>
            <Text bright={7}>
              {t("navbar.meeting")}
              &nbsp;
              <Switch
                checked={meetingMode}
                name={"meetingMode"}
                onChange={toggleMeetingMode}
              />
            </Text>
          </Can>
          {userEmail.endsWith("@fluidattacks.com") ? (
            <Text bright={7}>
              {t("navbar.featurePreview")}
              &nbsp;
              <Switch
                checked={featurePreview}
                name={"featurePreview"}
                onChange={toggleFeaturePreview}
              />
            </Text>
          ) : undefined}
        </div>
        <Hr />
        <Button disp={"block"} onClick={openTokenModal}>
          <Text bright={8}>
            <FontAwesomeIcon icon={faKey} />
            &nbsp;
            {t("navbar.token")}
          </Text>
        </Button>
        <Button>
          <Link to={"/user/config"}>
            <Text bright={8}>
              <FontAwesomeIcon icon={faUserCog} />
              &nbsp;
              {t("navbar.notification")}
            </Text>
          </Link>
        </Button>
        <Button onClick={openMobileModal}>
          <Text bright={8}>
            <FontAwesomeIcon icon={faMobileAlt} />
            &nbsp;
            {t("navbar.mobile")}
          </Text>
        </Button>
        <SpeakUpLink
          href={"https://speakup.fluidattacks.tech/contactform/mail"}
        >
          <Button>
            <Text bright={8}>
              <FontAwesomeIcon icon={faMessage} />
              &nbsp;
              {t("navbar.speakup")}
            </Text>
          </Button>
        </SpeakUpLink>
        <Can do={"api_mutations_add_stakeholder_mutate"}>
          <Button onClick={openStakeholderModal}>
            <Text bright={8}>
              <FontAwesomeIcon icon={faUserPlus} />
              &nbsp;
              {t("navbar.user")}
            </Text>
          </Button>
          {isStakeholderModalOpen ? (
            <AddUserModal
              action={"add"}
              domainSuggestions={[]}
              editTitle={""}
              onClose={closeStakeholderModal}
              onSubmit={handleAddUserSubmit}
              open={true}
              suggestions={[]}
              title={t("navbar.user")}
              type={"user"}
            />
          ) : undefined}
        </Can>
        <Button onClick={deleteAccount}>
          <Text bright={8}>
            <FontAwesomeIcon icon={faUserTimes} />
            &nbsp;
            {t("navbar.deleteAccount.text")}
          </Text>
        </Button>
        <Hr />
        <Button onClick={logout}>
          <Text bright={8}>
            <FontAwesomeIcon icon={faSignOutAlt} />
            &nbsp;
            {t("navbar.logout")}
          </Text>
        </Button>
      </div>
      {isTokenModalOpen ? (
        <AccessTokenModal onClose={closeTokenModal} open={true} />
      ) : undefined}
      {isMobileModalOpen ? (
        <MobileModal onClose={closeMobileModal} />
      ) : undefined}
      <ConfirmDialog />
    </Dropdown>
  );
};

export { UserProfile };
