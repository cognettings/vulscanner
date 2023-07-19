import React from "react";
import { useTranslation } from "react-i18next";
import { useLocation } from "react-router-dom";

import { AddRoot } from "./add-root";
import { Autoenrollment } from "./auto-enrollment";
import { Dashboard } from "./dashboard";
import { DesktopModal } from "./desktop-modal";
import { EnrolledUser } from "./enrolled-user";
import { useCurrentUser } from "./hooks";
import { LaptopModal } from "./laptop-modal";
import { NoEnrolledUser } from "./no-enrolled-user";

import { useWindowSize } from "hooks";

const Home: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { width } = useWindowSize();
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const user = useCurrentUser();

  if (user === undefined) {
    return <div />;
  }

  const isExplicitSignUp = sessionStorage.getItem("trial") === "true";
  const comesFromFastTrack = searchParams.get("fast_track_end") === "true";
  const isInTrial = user.trial !== null && !user.trial.completed;

  if (user.enrolled) {
    // Restrict small screens while we improve the responsive layout
    if (width < 768) {
      if (comesFromFastTrack) {
        return (
          <LaptopModal
            button={t("autoenrollment.fastTrackMobile.end.button")}
            message={t("autoenrollment.fastTrackMobile.end.message")}
            title={t("autoenrollment.fastTrackMobile.end.title")}
            url={"https://fluidattacks.com/platform/"}
          />
        );
      }

      return (
        <DesktopModal
          emphasis={t("dashboard.minimumWidth.emphasis")}
          message={t("dashboard.minimumWidth.message")}
        />
      );
    }

    if (comesFromFastTrack || isInTrial) {
      return <AddRoot />;
    }

    if (isExplicitSignUp) {
      return <EnrolledUser email={user.userEmail} />;
    }

    return <Dashboard />;
  }

  if (isExplicitSignUp || width < 768) {
    return <Autoenrollment />;
  }

  return <NoEnrolledUser email={user.userEmail} />;
};

export { Home };
