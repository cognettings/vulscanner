import React, { useCallback, useContext } from "react";

import { useGroupActors, useOrganizationActors } from "./hooks";

import { useConfirmDialog } from "components/confirm-dialog";
import { authContext } from "context/auth";

const useConfirmInvitation = (
  shouldConfirm: boolean,
  type: "group" | "organization" | "user",
  groupName: string | undefined,
  organizationId: string | undefined
): {
  ConfirmInvitationDialog: React.FC;
  confirmInvitation: (email: string) => Promise<boolean>;
} => {
  const { userEmail } = useContext(authContext);
  const { confirm, ConfirmDialog: ConfirmInvitationDialog } =
    useConfirmDialog();

  const groupActors = useGroupActors(shouldConfirm ? groupName : undefined);
  const organizationActors = useOrganizationActors(
    shouldConfirm ? organizationId : undefined
  );
  const actorEmails = [...groupActors, ...organizationActors]
    .map((actor): string | undefined => /<(?<email>.*?)>/u.exec(actor)?.[1])
    .filter((actorEmail): actorEmail is string => actorEmail !== undefined);

  const confirmInvitation = useCallback(
    async (email: string): Promise<boolean> => {
      const sameEmailDomain = userEmail.split("@")[1] === email.split("@")[1];
      const inAuthors = actorEmails.includes(email);

      if (!shouldConfirm || sameEmailDomain || inAuthors) {
        return true;
      }

      const target = {
        group: `group ${groupName ?? ""}`,
        organization: "this organization",
        user: "the platform",
      }[type];

      return confirm({
        message: (
          <p>
            {"The user with the email address"}&nbsp;
            <b>{email}</b>&nbsp;
            {"is outside your company."} <br />
            {`Are you sure you want to invite them to ${target}?`}
          </p>
        ),
        title: "Confirm invitation",
      });
    },
    [actorEmails, confirm, groupName, shouldConfirm, type, userEmail]
  );

  return { ConfirmInvitationDialog, confirmInvitation };
};

export { useConfirmInvitation };
