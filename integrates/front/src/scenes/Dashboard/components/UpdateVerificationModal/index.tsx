import type { ApolloError } from "@apollo/client";
import { useMutation } from "@apollo/client";
import type { ColumnDef } from "@tanstack/react-table";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import {
  getAreAllChunckedMutationValid,
  handleAltSubmitHelper,
  handleRequestVerification,
  handleRequestVerificationError,
  handleVerifyRequest,
  handleVerifyRequestError,
} from "./helpers";
import type {
  IRequestVulnVerificationResult,
  IVerifyRequestVulnResult,
} from "./types";

import { Switch } from "components/Switch";
import { Table } from "components/Table";
import { Tooltip } from "components/Tooltip";
import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "pages/home/dashboard/navbar/to-do/queries";
import { RemediationModal } from "scenes/Dashboard/components/RemediationModal/index";
import { changeVulnStateFormatter } from "scenes/Dashboard/components/UpdateVerificationModal/Formatters/changeVulnState";
import {
  REQUEST_VULNERABILITIES_VERIFICATION,
  VERIFY_VULNERABILITIES,
} from "scenes/Dashboard/components/UpdateVerificationModal/queries";

interface IVulnData {
  findingId: string;
  groupName: string;
  id: string;
  specific: string;
  state: "REJECTED" | "SAFE" | "SUBMITTED" | "VULNERABLE";
  where: string;
}
interface IUpdateVerificationModal {
  isReattacking: boolean;
  isVerifying: boolean;
  vulns: IVulnData[];
  clearSelected: () => void;
  handleCloseModal: () => void;
  setRequestState: () => void;
  setVerifyState: () => void;
  refetchData: () => void;
  refetchFindingAndGroup: (() => void) | undefined;
  refetchFindingHeader: (() => void) | undefined;
}

const UpdateVerificationModal: React.FC<IUpdateVerificationModal> = ({
  isReattacking,
  isVerifying,
  vulns,
  clearSelected,
  handleCloseModal,
  setRequestState,
  setVerifyState,
  refetchData,
  refetchFindingAndGroup,
  refetchFindingHeader,
}: IUpdateVerificationModal): JSX.Element => {
  const MAX_JUSTIFICATION_LENGTH = 10000;
  const { t } = useTranslation();

  // State management
  const [vulnerabilitiesList, setVulnerabilitiesList] = useState(vulns);
  const [isOpen, setIsOpen] = useState(true);
  const [isRunning, setIsRunning] = useState(false);
  const closeRemediationModal: () => void = useCallback((): void => {
    handleCloseModal();
  }, [handleCloseModal]);

  // GraphQL operations
  const [requestVerification, { client, loading: submittingRequest }] =
    useMutation<IRequestVulnVerificationResult>(
      REQUEST_VULNERABILITIES_VERIFICATION
    );

  const [verifyRequest, { loading: submittingVerify }] =
    useMutation<IVerifyRequestVulnResult>(VERIFY_VULNERABILITIES);

  const handleSubmit = useCallback(
    async (values: { treatmentJustification: string }): Promise<void> => {
      setIsRunning(true);
      try {
        const results = await handleAltSubmitHelper(
          requestVerification,
          verifyRequest,
          values,
          vulnerabilitiesList,
          isReattacking
        );
        const areAllMutationValid = getAreAllChunckedMutationValid(results);
        if (areAllMutationValid.every(Boolean)) {
          refetchData();
          if (refetchFindingAndGroup !== undefined) {
            refetchFindingAndGroup();
          }
          if (isVerifying && refetchFindingHeader !== undefined) {
            refetchFindingHeader();
          }
          if (isReattacking) {
            handleRequestVerification(clearSelected, setRequestState, true);
          } else {
            handleVerifyRequest(
              clearSelected,
              setVerifyState,
              true,
              vulns.length
            );
          }
        }
      } catch (requestError: unknown) {
        if (isReattacking) {
          (requestError as ApolloError).graphQLErrors.forEach((error): void => {
            handleRequestVerificationError(error);
          });
        } else {
          (requestError as ApolloError).graphQLErrors.forEach((error): void => {
            handleVerifyRequestError(error);
          });
        }
      } finally {
        await client.refetchQueries({
          include: [GET_ME_VULNERABILITIES_ASSIGNED_IDS],
        });
        setIsRunning(false);
        closeRemediationModal();
      }
    },
    [
      clearSelected,
      client,
      closeRemediationModal,
      isReattacking,
      isVerifying,
      requestVerification,
      refetchData,
      refetchFindingAndGroup,
      refetchFindingHeader,
      setRequestState,
      setVerifyState,
      verifyRequest,
      vulnerabilitiesList,
      vulns.length,
    ]
  );

  const handleOnChange = useCallback((): void => {
    setIsOpen((currentValue: boolean): boolean => {
      const newVulnList: IVulnData[] = vulnerabilitiesList.map(
        (vuln: IVulnData): IVulnData => ({
          ...vuln,
          state: currentValue ? "SAFE" : "VULNERABLE",
        })
      );
      setVulnerabilitiesList([...newVulnList]);

      return !currentValue;
    });
  }, [vulnerabilitiesList]);

  const renderVulnsToVerify: () => JSX.Element = (): JSX.Element => {
    const handleUpdateRepo: (vulnInfo: Record<string, string>) => void = (
      vulnInfo: Record<string, string>
    ): void => {
      const newVulnList: IVulnData[] = vulnerabilitiesList.map(
        (vuln: IVulnData): IVulnData =>
          vuln.id === vulnInfo.id
            ? {
                ...vuln,
                state: vuln.state === "VULNERABLE" ? "SAFE" : "VULNERABLE",
              }
            : vuln
      );
      setVulnerabilitiesList([...newVulnList]);
    };

    const columns: ColumnDef<IVulnData>[] = [
      {
        accessorKey: "where",
        header: "Where",
      },
      {
        accessorKey: "specific",
        header: "Specific",
      },
      {
        accessorKey: "state",
        cell: (cell): JSX.Element =>
          changeVulnStateFormatter(
            cell.row.original as unknown as Record<string, string>,
            handleUpdateRepo
          ),
        header: "State",
      },
    ];

    return (
      <React.StrictMode>
        <Tooltip
          id={"toogleToolTip"}
          place={"top"}
          tip={t(
            "searchFindings.tabDescription.remediationModal.globalSwitch.tooltip"
          )}
        >
          <div className={"pr4 tr w-100"}>
            <span className={"mb0 mt1 pr2"}>
              {t(
                "searchFindings.tabDescription.remediationModal.globalSwitch.text"
              )}
            </span>
            &nbsp;
            <Switch
              checked={isOpen}
              label={{ off: "Safe", on: "Vulnerable" }}
              onChange={handleOnChange}
            />
          </div>
        </Tooltip>
        <Table
          columns={columns}
          data={vulnerabilitiesList}
          enableSearchBar={true}
          id={"vulnstoverify"}
        />
      </React.StrictMode>
    );
  };

  return (
    <React.StrictMode>
      <RemediationModal
        additionalInfo={
          isReattacking
            ? t("searchFindings.tabDescription.remediationModal.message", {
                vulns: vulns.length,
              })
            : undefined
        }
        isLoading={submittingRequest || submittingVerify || isRunning}
        isOpen={true}
        maxJustificationLength={MAX_JUSTIFICATION_LENGTH}
        message={
          isReattacking
            ? t("searchFindings.tabDescription.remediationModal.justification")
            : t("searchFindings.tabDescription.remediationModal.observations")
        }
        onClose={closeRemediationModal}
        onSubmit={handleSubmit}
        title={
          isReattacking
            ? t("searchFindings.tabDescription.remediationModal.titleRequest")
            : t(
                "searchFindings.tabDescription.remediationModal.titleObservations"
              )
        }
      >
        {isVerifying ? renderVulnsToVerify() : undefined}
      </RemediationModal>
    </React.StrictMode>
  );
};

export type { IUpdateVerificationModal, IVulnData };
export { UpdateVerificationModal };
