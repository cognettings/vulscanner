import { useMutation, useQuery } from "@apollo/client";
import { useCallback, useState } from "react";

import type { IAcceptLegal, IUserRemember } from "./queries";
import { ACCEPT_LEGAL_MUTATION, GET_USER_REMEMBER } from "./queries";
import { comesFromLogin } from "./utils";

import { Logger } from "utils/logger";

interface ILegalNotice {
  acceptLegalNotice: (remember: boolean) => void;
  legalNoticeOpen?: boolean;
}

const useLegalNotice = (): ILegalNotice => {
  const [legalNoticeOpen, setLegalNoticeOpen] = useState<boolean | undefined>(
    undefined
  );

  useQuery<IUserRemember>(GET_USER_REMEMBER, {
    onCompleted: (data): void => {
      setLegalNoticeOpen(!data.me.remember && comesFromLogin());
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.error("Couldn't get user remember", error);
      });
    },
  });

  const [acceptLegalMutation] = useMutation<IAcceptLegal>(
    ACCEPT_LEGAL_MUTATION,
    {
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          Logger.error("Couldn't accept legal notice", error);
        });
      },
    }
  );
  const acceptLegalNotice = useCallback(
    (remember: boolean): void => {
      void acceptLegalMutation({ variables: { remember } });
      setLegalNoticeOpen(false);
    },
    [acceptLegalMutation]
  );

  return { acceptLegalNotice, legalNoticeOpen };
};

export { useLegalNotice };
