import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useIdleTimer } from "react-idle-timer";

import { Modal, ModalConfirm } from "components/Modal";

/*
 * 5 min is recommended. More than that is assumed risk.
 * Check with the product owner before modifying these values
 *
 * {@link https://docs.fluidattacks.com/criteria/requirements/023}
 */
const TIME_TO_IDLE_MS = 15 * 60 * 1000;
const TIME_TO_LOGOUT_MS = 1 * 60 * 1000;

const SessionIdle: React.FC = (): JSX.Element => {
  const [idleWarningOpen, setIdleWarningOpen] = useState(false);
  const { t } = useTranslation();

  const { activate } = useIdleTimer({
    crossTab: true,
    onActive: (): void => {
      setIdleWarningOpen(false);
    },
    onIdle: (): void => {
      location.replace("/logout");
    },
    onPrompt: (): void => {
      setIdleWarningOpen(true);
    },
    promptBeforeIdle: TIME_TO_LOGOUT_MS,
    syncTimers: 500,
    timeout: TIME_TO_IDLE_MS,
  });

  const dismissWarning = useCallback((): void => {
    activate();
  }, [activate]);

  return (
    <Modal open={idleWarningOpen} title={t("validations.inactiveSessionModal")}>
      <p>{t("validations.inactiveSession")}</p>
      <ModalConfirm
        onConfirm={dismissWarning}
        txtConfirm={t("validations.inactiveSessionDismiss")}
      />
    </Modal>
  );
};

export { SessionIdle };
