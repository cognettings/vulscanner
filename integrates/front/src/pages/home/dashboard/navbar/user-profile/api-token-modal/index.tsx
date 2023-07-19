import { faPlus, faXmark } from "@fortawesome/free-solid-svg-icons";
import type { ColumnDef } from "@tanstack/react-table";
import dayjs, { extend } from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import timezone from "dayjs/plugin/timezone";
import utc from "dayjs/plugin/utc";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { useConfirmDialog } from "components/confirm-dialog";
import { Modal } from "components/Modal";
import { Table } from "components/Table";
import { Text } from "components/Text";
import { AddTokenModal } from "pages/home/dashboard/navbar/user-profile/api-token-modal/add";
import {
  useGetAPIToken,
  useInvalidateAPIToken,
} from "pages/home/dashboard/navbar/user-profile/api-token-modal/hooks";
import type {
  IAccessTokens,
  ITokensModalProps,
} from "pages/home/dashboard/navbar/user-profile/api-token-modal/types";

const AccessTokenModal: React.FC<ITokensModalProps> = ({
  open,
  onClose,
}): JSX.Element => {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const handleOpen = useCallback((): void => {
    setIsOpen((current): boolean => !current);
  }, []);

  const [data, refetch] = useGetAPIToken();
  const { confirm, ConfirmDialog } = useConfirmDialog();

  const lastAccessTokenUseFromNow = useCallback(
    (lastTokenUse: Date | null): string => {
      if (lastTokenUse === null) {
        return "Never";
      }
      extend(relativeTime);
      extend(utc);
      extend(timezone);

      return dayjs(lastTokenUse).tz(dayjs.tz.guess()).fromNow();
    },
    []
  );

  const invalidateToken = useInvalidateAPIToken(refetch);

  const revokeToken = useCallback(
    (token: IAccessTokens): (() => void) =>
      async (): Promise<void> => {
        const confirmResult = await confirm({
          message:
            token.lastUse === null ? (
              t("updateAccessToken.warningConfirm")
            ) : (
              <React.Fragment>
                <label>
                  <b>{t("updateAccessToken.warning")}</b>
                </label>
                <div className={"mb1"}>
                  <Text disp={"inline"} fw={7}>
                    {t("updateAccessToken.tokenLastUsed")}
                  </Text>
                  &nbsp;
                  {lastAccessTokenUseFromNow(token.lastUse)}
                </div>
              </React.Fragment>
            ),
          title: t("updateAccessToken.invalidate"),
        });
        if (confirmResult) {
          await invalidateToken({ variables: { id: token.id } });
        }
      },
    [confirm, invalidateToken, lastAccessTokenUseFromNow, t]
  );

  const revoke = useCallback(
    (token: IAccessTokens): JSX.Element => (
      <Button icon={faXmark} onClick={revokeToken(token)} variant={"secondary"}>
        {t("updateAccessToken.buttons.revoke")}
      </Button>
    ),
    [revokeToken, t]
  );

  const tableColumns: ColumnDef<IAccessTokens>[] = [
    {
      accessorKey: "name",
      header: t("updateAccessToken.header.name"),
    },
    {
      accessorKey: "issuedAt",
      cell: (cell): string =>
        new Date(cell.row.original.issuedAt * 1000)
          .toISOString()
          .substring(0, 10),
      header: t("updateAccessToken.header.issuedAt"),
    },
    {
      accessorKey: "lastUse",
      cell: (cell): string =>
        lastAccessTokenUseFromNow(cell.row.original.lastUse),
      header: t("updateAccessToken.header.lastUse"),
    },
    {
      accessorKey: "action",
      cell: (cell): JSX.Element => revoke(cell.row.original),
      enableSorting: false,
      header: "",
    },
  ];

  return (
    <React.Fragment>
      <Modal onClose={onClose} open={open} title={t("updateAccessToken.title")}>
        <Table
          columns={tableColumns}
          data={data?.me.accessTokens ?? []}
          enableSearchBar={false}
          extraButtons={
            (data?.me.accessTokens.length ?? 2) < 2 ? (
              <Button icon={faPlus} onClick={handleOpen} variant={"primary"}>
                {t("updateAccessToken.buttons.add")}
              </Button>
            ) : undefined
          }
          id={"tblAccessTokens"}
        />
        <ConfirmDialog />
      </Modal>
      {isOpen ? (
        <AddTokenModal onClose={handleOpen} open={isOpen} refetch={refetch} />
      ) : undefined}
    </React.Fragment>
  );
};

export { AccessTokenModal };
