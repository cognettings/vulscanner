import type { FetchResult } from "@apollo/client";
import { Formik } from "formik";
import _ from "lodash";
import React, { useCallback, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import type { TestContext, ValidationError } from "yup";
import { object, string } from "yup";

import type {
  IUpdateVulnerabilityForm,
  IVulnDataTypeAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateTreatmentModal } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/form";
import { handleSubmitHelper } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/helpers";
import type { IUpdateDescriptionContentProps } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/types";
import {
  groupExternalBugTrackingSystem,
  groupLastHistoricTreatment,
  groupVulnLevel,
  sortTags,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";

interface IConfigFn {
  isDescriptionPristine: boolean;
  isTreatmentDescriptionPristine: boolean;
  isTreatmentPristine: boolean;
  requestZeroRisk: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>;
  updateVulnerability: (
    dataTreatment: IUpdateVulnerabilityForm,
    isDescriptionPristine: boolean,
    isTreatmentDescriptionPristine: boolean,
    isTreatmentPristine: boolean
  ) => Promise<void>;
}

const UpdateDescriptionContent: React.FC<IUpdateDescriptionContentProps> = ({
  findingId = "",
  groupName,
  vulnerabilities,
  handleClearSelected,
  handleCloseModal,
  refetchData,
  confirm,
}: IUpdateDescriptionContentProps): JSX.Element => {
  const { t } = useTranslation();

  const lastTreatment = useMemo(
    (): IHistoricTreatment => ({
      ...groupLastHistoricTreatment(vulnerabilities),
      justification: "",
    }),
    [vulnerabilities]
  );
  const vulnsTags = useMemo(
    (): string[][] =>
      vulnerabilities.map((vuln: IVulnDataTypeAttr): string[] =>
        sortTags(vuln.tag)
      ),
    [vulnerabilities]
  );

  const [fnConfig, setFnConfig] = useState<IConfigFn>({
    isDescriptionPristine: true,
    isTreatmentDescriptionPristine: true,
    isTreatmentPristine: true,
    requestZeroRisk: async (): Promise<FetchResult<unknown>> =>
      Promise.resolve<FetchResult>({}),
    updateVulnerability: async (): Promise<void> => Promise.resolve(undefined),
  });

  const setConfigFn = useCallback(
    (
      requestZeroRisk: (
        variables: Record<string, unknown>
      ) => Promise<FetchResult<unknown>>,
      updateVulnerability: (
        dataTreatment: IUpdateVulnerabilityForm,
        isDescriptionPristine: boolean,
        isTreatmentDescriptionPristine: boolean,
        isTreatmentPristine: boolean
      ) => Promise<void>,
      isDescriptionPristine: boolean,
      isTreatmentDescriptionPristine: boolean,
      isTreatmentPristine: boolean
    ): void => {
      setFnConfig({
        isDescriptionPristine,
        isTreatmentDescriptionPristine,
        isTreatmentPristine,
        requestZeroRisk,
        updateVulnerability,
      });
    },
    []
  );

  const handleSubmit = useCallback(
    async (values: IUpdateVulnerabilityForm): Promise<void> => {
      const changedToRequestZeroRisk: boolean =
        values.treatment === "REQUEST_ZERO_RISK";
      const changedToUndefined: boolean =
        values.treatment === "ACCEPTED_UNDEFINED" &&
        lastTreatment.treatment !== "ACCEPTED_UNDEFINED";
      await handleSubmitHelper(
        fnConfig.updateVulnerability,
        fnConfig.requestZeroRisk,
        confirm,
        values,
        findingId,
        vulnerabilities,
        changedToRequestZeroRisk,
        changedToUndefined,
        fnConfig.isDescriptionPristine,
        fnConfig.isTreatmentDescriptionPristine,
        fnConfig.isTreatmentPristine
      );
    },
    [
      confirm,
      findingId,
      fnConfig.isDescriptionPristine,
      fnConfig.isTreatmentDescriptionPristine,
      fnConfig.isTreatmentPristine,
      fnConfig.requestZeroRisk,
      fnConfig.updateVulnerability,
      lastTreatment.treatment,
      vulnerabilities,
    ]
  );

  const MAX_TREATMENT_JUSTIFICATION_LENGTH: number = 10000;

  const validations = object().shape({
    justification: string().when("$isTreatmentPristine", {
      is: (): boolean => fnConfig.isTreatmentPristine,
      otherwise: string()
        .required(t("validations.required"))
        .max(
          MAX_TREATMENT_JUSTIFICATION_LENGTH,
          t("validations.maxLength", {
            count: MAX_TREATMENT_JUSTIFICATION_LENGTH,
          })
        )
        .test({
          exclusive: false,
          name: "invalidTextBeginning",
          params: {},
          test: (
            value: string | undefined,
            thisContext: TestContext
          ): ValidationError | boolean => {
            if (value === undefined) {
              return false;
            }
            const beginTextMatch: RegExpMatchArray | null =
              /^=|^-|^\+|^@|^\translate.t|^\r/u.exec(value);

            return _.isNull(beginTextMatch)
              ? true
              : thisContext.createError({
                  message: t("validations.invalidTextBeginning", {
                    chars: `'${beginTextMatch[0]}'`,
                  }),
                });
          },
        })
        .test({
          exclusive: false,
          name: "invalidTextPattern",
          params: {},
          test: (
            value: string | undefined,
            thisContext: TestContext
          ): ValidationError | boolean => {
            if (value === undefined) {
              return false;
            }
            const contentTextMatch: RegExpMatchArray | null =
              /["',;](?:[-=+@\translate.t\r])/u.exec(value);

            return _.isNull(contentTextMatch)
              ? true
              : thisContext.createError({
                  message: t("validations.invalidTextPattern", {
                    chars: `'${contentTextMatch[0]}'`,
                  }),
                });
          },
        }),
      then: string(),
    }),
    treatment: string().when("$isTreatmentPristine", {
      is: (): boolean => fnConfig.isTreatmentPristine,
      otherwise: string().required(t("validations.required")),
      then: string(),
    }),
  });

  return (
    <React.StrictMode>
      <Formik
        enableReinitialize={true}
        initialValues={{
          acceptanceDate: lastTreatment.acceptanceDate,
          acceptanceStatus: lastTreatment.acceptanceStatus,
          assigned: lastTreatment.assigned,
          date: lastTreatment.date,
          externalBugTrackingSystem:
            groupExternalBugTrackingSystem(vulnerabilities),
          justification: lastTreatment.justification,
          severity:
            Number(groupVulnLevel(vulnerabilities)) > 0
              ? groupVulnLevel(vulnerabilities)
              : "",
          source:
            vulnerabilities.length === 1 &&
            vulnerabilities[0].source.toUpperCase() !== "ASM"
              ? vulnerabilities[0].source.toUpperCase()
              : "",
          tag: _.join(_.intersection(...vulnsTags), ","),
          treatment: lastTreatment.treatment
            .replace("NEW", "")
            .replace("UNTREATED", ""),
          user: lastTreatment.user,
        }}
        name={"editTreatmentVulnerability"}
        onSubmit={handleSubmit}
        validationSchema={validations}
      >
        <UpdateTreatmentModal
          findingId={findingId}
          groupName={groupName}
          handleClearSelected={handleClearSelected}
          handleCloseModal={handleCloseModal}
          refetchData={refetchData}
          setConfigFn={setConfigFn}
          vulnerabilities={vulnerabilities}
        />
      </Formik>
    </React.StrictMode>
  );
};

export { UpdateDescriptionContent };
