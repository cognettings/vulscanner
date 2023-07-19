/* eslint @typescript-eslint/no-unnecessary-condition:0 */
import { useLazyQuery, useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import {
  faArrowRight,
  faPlus,
  faTrashAlt,
} from "@fortawesome/free-solid-svg-icons";
import type {
  ColumnDef,
  Row as FormRow,
  SortingState,
  VisibilityState,
} from "@tanstack/react-table";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, {
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import type { FormEvent } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";
import type { TestContext, ValidationError } from "yup";
import { mixed, object, string } from "yup";

import { renderDescription } from "./description";
import {
  ADD_FINDING_MUTATION,
  GET_GROUP_VULNERABILITIES,
  GET_ROOTS,
} from "./queries";
import type {
  IAddFindingFormValues,
  IAddFindingMutationResult,
  IFindingSuggestionData,
  IGroupVulnerabilities,
  IRoot,
  IVulnerabilitiesResume,
  IVulnerability,
} from "./types";
import {
  formatFindings,
  formatState,
  getAreAllMutationValid,
  getFindingSuggestions,
  getResults,
  handleRemoveFindingsError,
} from "./utils";

import { GET_LANGUAGE } from "../../Finding-Content/DescriptionView/queries";
import type { ILanguageData } from "../../Finding-Content/DescriptionView/types";
import { REMOVE_FINDING_MUTATION } from "../../Finding-Content/queries";
import { Button } from "components/Button";
import { Empty } from "components/Empty";
import type { IFilter, IPermanentData } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Input, Select, TextArea } from "components/Input";
import { FormGroup } from "components/Input/styles";
import { Col, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Table } from "components/Table";
import { includeTagsFormatter } from "components/Table/formatters/includeTagsFormatter";
import type { ICellHelper } from "components/Table/types";
import { Tooltip } from "components/Tooltip";
import { Can } from "context/authz/Can";
import { authzPermissionsContext } from "context/authz/config";
import { Have } from "context/authz/Have";
import { meetingModeContext } from "context/meetingMode";
import { useDebouncedCallback, useStoredState } from "hooks";
import { searchingFindings } from "resources";
import { ExpertButton } from "scenes/Dashboard/components/ExpertButton";
import { RiskExposureTour } from "scenes/Dashboard/components/RiskExposureTour/RiskExposureTour";
import { WelcomeModal } from "scenes/Dashboard/components/WelcomeModal";
import { GET_FINDINGS } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/queries";
import { ReportsModal } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/reportsModal";
import type {
  IFindingAttr,
  IGroupFindingsAttr,
} from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/types";
import { vulnerabilitiesContext } from "scenes/Dashboard/group/context";
import type { IVulnerabilitiesContext } from "scenes/Dashboard/group/types";
import {
  attackComplexityValues,
  attackVectorValues,
  availabilityImpactValues,
  availabilityRequirementValues,
  confidentialityImpactValues,
  confidentialityRequirementValues,
  exploitabilityValues,
  getCVSS31VectorString,
  getRiskExposure,
  integrityImpactValues,
  integrityRequirementValues,
  privilegesRequiredValues,
  remediationLevelValues,
  reportConfidenceValues,
  severityScopeValues,
  userInteractionValues,
} from "utils/cvss";
import { formatPercentage, severityFormatter } from "utils/formatHelpers";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const GroupFindingsView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canGetRejectedVulnerabilities: boolean = permissions.can(
    "api_resolvers_finding_rejected_vulnerabilities_resolve"
  );
  const canGetSubmittedVulnerabilities: boolean = permissions.can(
    "api_resolvers_finding_submitted_vulnerabilities_resolve"
  );
  const { meetingMode } = useContext(meetingModeContext);
  const {
    openVulnerabilities,
    setOpenVulnerabilities,
  }: IVulnerabilitiesContext = useContext(vulnerabilitiesContext);
  const { push } = useHistory();
  const { url } = useRouteMatch();
  const { t } = useTranslation();

  // State management
  const [isReportsModalOpen, setIsReportsModalOpen] = useState(false);
  const [isAddFindingModalOpen, setIsAddFindingModalOpen] = useState(false);
  const defaultAddFindingInitialValues = useMemo(
    (): IAddFindingFormValues => ({
      attackComplexity: "",
      attackVector: "",
      availabilityImpact: "",
      availabilityRequirement: "",
      confidentialityImpact: "",
      confidentialityRequirement: "",
      description: "",
      exploitability: "",
      integrityImpact: "",
      integrityRequirement: "",
      modifiedAttackComplexity: "",
      modifiedAttackVector: "",
      modifiedAvailabilityImpact: "",
      modifiedConfidentialityImpact: "",
      modifiedIntegrityImpact: "",
      modifiedPrivilegesRequired: "",
      modifiedSeverityScope: "",
      modifiedUserInteraction: "",
      privilegesRequired: "",
      remediationLevel: "",
      reportConfidence: "",
      severityScope: "",
      threat: "",
      title: "",
      userInteraction: "",
    }),
    []
  );
  const [addFindingInitialValues, setAddFindingInitialValues] = useState(
    defaultAddFindingInitialValues
  );
  const [rootFilter, setRootFilter] = useState<string | undefined>("");
  const rootFilterRef = useRef<string | undefined>(rootFilter);

  const [suggestions, setSuggestions] = useState<
    IFindingSuggestionData[] | undefined
  >(undefined);
  const [filters, setFilters] = useState<IFilter<IFindingAttr>[]>([
    {
      id: "root",
      isBackFilter: true,
      key: "root",
      label: "Location",
      type: "text",
    },
    {
      id: "lastVulnerability",
      key: "lastVulnerability",
      label: t("group.findings.lastReport"),
      type: "number",
    },
    {
      id: "title",
      key: "title",
      label: t("group.findings.type"),
      selectOptions: (findings: IFindingAttr[]): string[] =>
        [
          ...new Set(findings.map((finding): string => finding.title ?? "")),
        ].filter(Boolean),
      type: "select",
    },
    {
      id: "state",
      key: "status",
      label: t("group.findings.status"),
      selectOptions: [
        ...(permissions.can("see_draft_status")
          ? [
              {
                header: t("searchFindings.header.status.stateLabel.draft"),
                value: "DRAFT",
              },
            ]
          : []),
        {
          header: t("searchFindings.header.status.stateLabel.open"),
          value: "VULNERABLE",
        },
        {
          header: t("searchFindings.header.status.stateLabel.closed"),
          value: "SAFE",
        },
      ],
      type: "select",
    },
    {
      id: "treatment",
      key: (finding: IFindingAttr, value?: string): boolean => {
        if (value === "" || value === undefined) return true;

        return (
          finding.treatmentSummary[
            value as keyof typeof finding.treatmentSummary
          ] > 0
        );
      },
      label: t("group.findings.treatment"),
      selectOptions: [
        {
          header: t("searchFindings.tabDescription.treatment.new"),
          value: "untreated",
        },
        {
          header: t("searchFindings.tabDescription.treatment.inProgress"),
          value: "inProgress",
        },
        {
          header: t("searchFindings.tabDescription.treatment.accepted"),
          value: "accepted",
        },
        {
          header: t(
            "searchFindings.tabDescription.treatment.acceptedUndefined"
          ),
          value: "acceptedUndefined",
        },
      ],
      type: "select",
    },
    {
      id: "maxOpenSeverityScore",
      key: "maxOpenSeverityScore",
      label: t("group.findings.severity"),
      type: "numberRange",
    },
    {
      id: "age",
      key: "age",
      label: t("group.findings.age"),
      type: "number",
    },
    {
      id: "reattack",
      key: "reattack",
      label: t("group.findings.reattack"),
      selectOptions: ["-", "Pending"],
      type: "select",
    },
    {
      id: "releaseDate",
      key: "releaseDate",
      label: t("group.findings.releaseDate"),
      type: "dateRange",
    },
    ...(permissions.can("see_review_filter")
      ? ([
          {
            id: "review",
            key: (finding: IFindingAttr, value?: string): boolean => {
              switch (value) {
                case "YES":
                  return (
                    (_.isNumber(finding.rejectedVulnerabilities) &&
                      finding.rejectedVulnerabilities > 0) ||
                    (_.isNumber(finding.submittedVulnerabilities) &&
                      finding.submittedVulnerabilities > 0)
                  );
                case "NO":
                  return (
                    (!_.isNumber(finding.rejectedVulnerabilities) ||
                      finding.rejectedVulnerabilities === 0) &&
                    (!_.isNumber(finding.submittedVulnerabilities) ||
                      finding.submittedVulnerabilities === 0)
                  );
                default:
                  return true;
              }
            },
            label: t("group.findings.review"),
            selectOptions: [
              {
                header: t("group.findings.boolean.True"),
                value: "YES",
              },
              {
                header: t("group.findings.boolean.False"),
                value: "NO",
              },
            ],
            type: "select",
          },
        ] as IFilter<IFindingAttr>[])
      : []),
  ]);
  const [filterVal, setFilterVal] = useStoredState<IPermanentData[]>(
    "tblFindFilters",
    [
      { id: "lastVulnerability", value: "" },
      { id: "title", value: "" },
      { id: "state", value: "" },
      { id: "treatment", value: "" },
      { id: "maxOpenSeverityScore", numberRangeValues: [undefined, undefined] },
      { id: "severityScore", numberRangeValues: [undefined, undefined] },
      { id: "age", value: "" },
      { id: "locationsInfo", value: "" },
      { id: "reattack", value: "" },
      { id: "releaseDate", rangeValues: ["", ""] },
    ],
    localStorage
  );
  const [columnVisibility, setColumnVisibility] =
    useStoredState<VisibilityState>("tblFindings-visibilityState", {
      Treatment: false,
      age: false,
      closingPercentage: false,
      description: false,
      reattack: false,
      releaseDate: false,
    });
  const [sorting, setSorting] = useStoredState<SortingState>(
    "tblFindings-sortingState",
    []
  );

  const closeAddFindingModal: () => void = useCallback((): void => {
    setAddFindingInitialValues(defaultAddFindingInitialValues);
    setIsAddFindingModalOpen(false);
  }, [defaultAddFindingInitialValues]);
  const openReportsModal: () => void = useCallback((): void => {
    setIsReportsModalOpen(true);
  }, []);
  const closeReportsModal: () => void = useCallback((): void => {
    setIsReportsModalOpen(false);
  }, []);

  const [isRunning, setIsRunning] = useState(false);
  const [selectedFindings, setSelectedFindings] = useState<IFindingAttr[]>([]);

  const [findingVulnerabilities, setFindingVulnerabilities] = useState<
    Record<string, IVulnerabilitiesResume>
  >({});

  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const openDeleteModal: () => void = useCallback((): void => {
    setIsDeleteModalOpen(true);
  }, []);
  const closeDeleteModal: () => void = useCallback((): void => {
    setIsDeleteModalOpen(false);
  }, []);

  const goToFinding = useCallback(
    (rowInfo: FormRow<IFindingAttr>): ((event: FormEvent) => void) => {
      return (event: FormEvent): void => {
        const vulnerabilityUrl = `${url}/${rowInfo.original.id}/locations`;
        const location =
          !_.isNil(rootFilterRef) &&
          !_.isEmpty(rootFilterRef.current) &&
          typeof rootFilterRef.current === "string"
            ? `${vulnerabilityUrl}?location=${rootFilterRef.current}`
            : vulnerabilityUrl;
        push(location);
        event.preventDefault();
      };
    },
    [push, rootFilterRef, url]
  );

  const handleQryErrors: (error: ApolloError) => void = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading group data", error);
      });
    },
    [t]
  );

  const { data: groupData } = useQuery<ILanguageData>(GET_LANGUAGE, {
    fetchPolicy: "no-cache",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading group language", error);
      });
    },
    variables: { groupName },
  });

  const { data, loading, refetch } = useQuery<IGroupFindingsAttr>(
    GET_FINDINGS,
    {
      fetchPolicy: "cache-first",
      onError: handleQryErrors,
      variables: {
        canGetRejectedVulnerabilities,
        canGetSubmittedVulnerabilities,
        groupName,
      },
    }
  );

  const [getVuln, { data: vulnData }] = useLazyQuery<IGroupVulnerabilities>(
    GET_GROUP_VULNERABILITIES,
    {
      fetchPolicy: "cache-and-network",
      nextFetchPolicy: "cache-first",
    }
  );

  const { data: rootsData } = useQuery<{ group: { roots: IRoot[] } }>(
    GET_ROOTS,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load roots", error);
        });
      },
      variables: { groupName },
    }
  );

  useEffect((): void => {
    if (!_.isUndefined(data) && !_.isUndefined(setOpenVulnerabilities)) {
      const newValue = data.group.findings.reduce(
        (previousValue: number, find: IFindingAttr): number =>
          previousValue + find.openVulnerabilities,
        0
      );
      if (openVulnerabilities !== newValue) {
        setOpenVulnerabilities(newValue);
      }
    }
  }, [data, openVulnerabilities, setOpenVulnerabilities]);

  useEffect((): void => {
    if (!_.isUndefined(vulnData)) {
      const { edges } = vulnData.group.vulnerabilities;

      edges
        .map((edge): IVulnerability => edge.node)
        .forEach((vulnerability): void => {
          setFindingVulnerabilities(
            (
              prevState: Record<string, IVulnerabilitiesResume>
            ): Record<string, IVulnerabilitiesResume> => {
              const current = prevState[vulnerability.findingId] ?? {
                treatmentAssignmentEmails: new Set(),
                wheres: "",
              };
              const wheres =
                current.wheres === ""
                  ? vulnerability.where
                  : [current.wheres, vulnerability.where].join(", ");

              const treatmentAssignmentEmails = new Set(
                [
                  ...current.treatmentAssignmentEmails,
                  vulnerability.state === "VULNERABLE"
                    ? (vulnerability.treatmentAssigned as string)
                    : "",
                ].filter(Boolean)
              );

              return {
                ...prevState,
                [vulnerability.findingId]: {
                  treatmentAssignmentEmails,
                  wheres,
                },
              };
            }
          );
        });
    }
  }, [vulnData]);

  const hasMachine = data?.group.hasMachine ?? false;
  const filledGroupInfo =
    !_.isEmpty(data?.group.description) &&
    !_.isEmpty(data?.group.businessId) &&
    !_.isEmpty(data?.group.businessName);

  const activeRoots: IRoot[] =
    rootsData === undefined
      ? []
      : [
          ...rootsData.group.roots.filter(
            (root): boolean => root.state === "ACTIVE"
          ),
        ];

  const findings: IFindingAttr[] = useMemo(
    (): IFindingAttr[] =>
      data === undefined
        ? []
        : formatFindings(data.group.findings, findingVulnerabilities),
    [data, findingVulnerabilities]
  );

  const orderedFindings: IFindingAttr[] = _.orderBy(
    findings,
    ["status", (item): number => item.totalOpenCVSSF],
    ["desc", "desc"]
  );

  useEffect((): (() => void) => {
    setRootFilter(
      filters.filter(
        (filter: IFilter<IFindingAttr>): boolean => filter.id === "root"
      )[0].value
    );
    // eslint-disable-next-line fp/no-mutation
    rootFilterRef.current = rootFilter;

    const debouncedRefetch = _.debounce((): void => {
      void refetch({ filters: { root: rootFilter } });
    }, 500);

    debouncedRefetch();

    return (): void => {
      debouncedRefetch.cancel();
    };
  }, [filters, refetch, rootFilter, setRootFilter]);

  const meetingFindings = meetingMode
    ? orderedFindings.filter(
        (finding: IFindingAttr): boolean => finding.status !== "DRAFT"
      )
    : orderedFindings;
  const filteredFindings = useFilters(meetingFindings, filters);

  const groupOpenCVSSF = findings
    .filter((find): boolean => find.status === "VULNERABLE")
    .reduce((sum, finding): number => sum + finding.totalOpenCVSSF, 0);

  const tableColumns: ColumnDef<IFindingAttr>[] = [
    {
      accessorKey: "title",
      cell: (cell: ICellHelper<IFindingAttr>): JSX.Element | string => {
        const finding: IFindingAttr = cell.row.original;

        return includeTagsFormatter({
          newTag:
            finding.lastVulnerability <= 7 && finding.openVulnerabilities > 0,
          reviewTag:
            !meetingMode &&
            ((_.isNumber(finding.rejectedVulnerabilities) &&
              finding.rejectedVulnerabilities > 0) ||
              (_.isNumber(finding.submittedVulnerabilities) &&
                finding.submittedVulnerabilities > 0)),
          text: finding.title,
        });
      },
      header: "Type",
    },
    {
      accessorKey: "status",
      cell: (cell: ICellHelper<IFindingAttr>): JSX.Element =>
        formatState(cell.getValue()),
      header: "Status",
    },
    {
      accessorKey: "maxOpenSeverityScore",
      cell: (cell: ICellHelper<IFindingAttr>): JSX.Element =>
        severityFormatter(cell.getValue()),
      header: "Severity",
    },
    {
      accessorFn: (row: IFindingAttr): string => {
        return getRiskExposure(row.totalOpenCVSSF, groupOpenCVSSF, row.status);
      },
      header: "% Risk exposure",
      id: "riskExposureColumn",
    },
    {
      accessorKey: "openVulnerabilities",
      header: "Open vulnerabilities",
    },
    {
      accessorKey: "lastVulnerability",
      cell: (cell: ICellHelper<IFindingAttr>): string =>
        t("group.findings.description.value", { count: cell.getValue() }),
      header: "Last report",
    },
    {
      accessorKey: "age",
      header: "Age",
    },
    {
      accessorKey: "closingPercentage",
      cell: (cell: ICellHelper<IFindingAttr>): string =>
        formatPercentage(cell.getValue()),
      header: t("group.findings.closingPercentage"),
    },
    {
      accessorKey: "reattack",
      header: "Reattack",
    },
    {
      accessorKey: "releaseDate",
      header: "Release date",
    },
    {
      accessorFn: (row: IFindingAttr): string[] => {
        const treatment = row.treatmentSummary;
        const treatmentNew = treatment.untreated > 0 ? "Untreated" : "";
        const treatmentAccUndef =
          treatment.acceptedUndefined > 0 ? "Permanently accepted" : "";
        const treatmentInProgress =
          treatment.inProgress > 0 ? "In progress" : "";
        const treatmentAccepted =
          treatment.accepted > 0 ? "Temporarily accepted" : "";

        return [
          treatmentNew,
          treatmentInProgress,
          treatmentAccepted,
          treatmentAccUndef,
        ].filter(Boolean);
      },
      cell: (cell: ICellHelper<IFindingAttr>): string => {
        const treatment = cell.row.original.treatmentSummary;

        return `Untreated: ${treatment.untreated}, In progress: ${treatment.inProgress},
        Temporarily accepted:  ${treatment.accepted}, Permamently accepted:
        ${treatment.acceptedUndefined}`;
      },
      header: "Treatment",
    },
    {
      accessorKey: "description",
      header: "Description",
    },
  ];

  const typesArray = findings.map((find: IFindingAttr): string[] => [
    find.title,
    find.title,
  ]);
  const typesOptions = Object.fromEntries(
    _.sortBy(typesArray, (arr): string => arr[0])
  );

  const [addFinding, { loading: addingFinding }] =
    useMutation<IAddFindingMutationResult>(ADD_FINDING_MUTATION, {
      onCompleted: async (result: IAddFindingMutationResult): Promise<void> => {
        if (result.addFinding.success) {
          msgSuccess(
            t("group.findings.addModal.alerts.addedFinding"),
            t("groupAlerts.titleSuccess")
          );
          await refetch();
          closeAddFindingModal();
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - The inserted Draft/Finding title is invalid":
              msgError(t("validations.addFindingModal.invalidTitle"));
              break;
            case "Exception - Finding with the same threat already exists":
              msgError(t("validations.addFindingModal.duplicatedThreat"));
              break;
            case "Exception - Finding with the same description already exists":
              msgError(t("validations.addFindingModal.duplicatedDescription"));
              break;
            case "Exception - Finding with the same description, threat and severity already exists":
              msgError(
                t("validations.addFindingModal.duplicatedMachineDescription")
              );
              break;
            case "Exception - Severity score is invalid":
              msgError(t("validations.addFindingModal.invalidSeverityScore"));
              break;
            case "Exception - Invalid characters":
              msgError(t("validations.invalidChar"));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred adding finding", error);
          }
        });
      },
    });

  const openAddFindingModal: () => void =
    useCallback(async (): Promise<void> => {
      setIsAddFindingModalOpen(true);
      if (_.isUndefined(suggestions)) {
        const findingSuggestions: IFindingSuggestionData[] =
          await getFindingSuggestions(
            groupData?.group.language.toLowerCase() as "en" | "es" | undefined
          ).catch((error: Error): IFindingSuggestionData[] => {
            Logger.error(
              "An error occurred getting finding suggestions",
              error
            );

            return [];
          });
        setSuggestions(findingSuggestions);
      }
    }, [groupData?.group.language, suggestions]);

  const handleAddFinding = useCallback(
    async (values: IAddFindingFormValues): Promise<void> => {
      const [matchingSuggestion]: IFindingSuggestionData[] = _.isUndefined(
        suggestions
      )
        ? []
        : suggestions.filter(
            (suggestion: IFindingSuggestionData): boolean =>
              `${suggestion.code}. ${suggestion.title}` === values.title
          );
      const suggestionData = _.omit(matchingSuggestion, ["code"]);
      await addFinding({
        variables: {
          ...suggestionData,
          attackComplexity: 0,
          attackVector: 0,
          availabilityImpact: 0,
          availabilityRequirement: 0,
          confidentialityImpact: 0,
          confidentialityRequirement: 0,
          cvssVector: getCVSS31VectorString(values),
          description: values.description,
          exploitability: 0,
          groupName,
          integrityImpact: 0,
          integrityRequirement: 0,
          modifiedAttackComplexity: 0,
          modifiedAttackVector: 0,
          modifiedAvailabilityImpact: 0,
          modifiedConfidentialityImpact: 0,
          modifiedIntegrityImpact: 0,
          modifiedPrivilegesRequired: 0,
          modifiedSeverityScope: 0,
          modifiedUserInteraction: 0,
          privilegesRequired: 0,
          remediationLevel: 0,
          reportConfidence: 0,
          severityScope: 0,
          threat: values.threat,
          title: values.title,
          userInteraction: 0,
        },
      });
    },
    [addFinding, groupName, suggestions]
  );

  const [removeFinding, { loading: deleting }] = useMutation(
    REMOVE_FINDING_MUTATION,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred deleting finding", error);
        });
      },
    }
  );

  const validMutationsHelper = useCallback(
    (handleCloseModal: () => void, areAllMutationValid: boolean[]): void => {
      if (areAllMutationValid.every(Boolean)) {
        msgSuccess(
          t("group.findings.deleteModal.alerts.vulnerabilitiesDeleted"),
          t("searchFindings.successTitle")
        );
        void refetch();
        handleCloseModal();
      }
    },
    [refetch, t]
  );

  const handleRemoveFinding = useCallback(
    async (justification: unknown): Promise<void> => {
      setIsRunning(true);
      if (selectedFindings.length === 0) {
        msgError(t("searchFindings.tabResources.noSelection"));
        setIsRunning(false);
      } else {
        try {
          const results = await getResults(
            removeFinding,
            selectedFindings,
            justification
          );
          const areAllMutationValid = getAreAllMutationValid(results);
          validMutationsHelper(closeDeleteModal, areAllMutationValid);
        } catch (updateError: unknown) {
          handleRemoveFindingsError(updateError);
        } finally {
          setIsRunning(false);
        }
      }
    },
    [closeDeleteModal, removeFinding, selectedFindings, t, validMutationsHelper]
  );

  const handleDelete = useCallback(
    async (values: Record<string, unknown>): Promise<void> => {
      await handleRemoveFinding(values.justification);
    },
    [handleRemoveFinding]
  );

  const handleSearch = useDebouncedCallback((root: string): void => {
    void getVuln({ variables: { first: 1200, groupName, root } });
  }, 500);

  const handleRowExpand = useCallback(
    (row: FormRow<IFindingAttr>): JSX.Element => {
      return renderDescription(row.original);
    },
    []
  );

  const getFindingMatchingSuggestion = useCallback(
    (findingName: string): IFindingSuggestionData | undefined => {
      const [matchingSuggestion]: IFindingSuggestionData[] = _.isUndefined(
        suggestions
      )
        ? []
        : suggestions.filter(
            (suggestion: IFindingSuggestionData): boolean =>
              `${suggestion.code}. ${suggestion.title}` === findingName
          );

      return matchingSuggestion;
    },
    [suggestions]
  );

  const handleAddFindingTitleChange = useCallback(
    ({ target }: React.ChangeEvent<HTMLInputElement>): void => {
      const matchingSuggestion = getFindingMatchingSuggestion(target.value);
      if (!_.isUndefined(matchingSuggestion)) {
        setAddFindingInitialValues({
          ...addFindingInitialValues,
          attackComplexity: matchingSuggestion.attackComplexity,
          attackVector: matchingSuggestion.attackVector,
          availabilityImpact: matchingSuggestion.availabilityImpact,
          confidentialityImpact: matchingSuggestion.confidentialityImpact,
          description: matchingSuggestion.description,
          exploitability: matchingSuggestion.exploitability,
          integrityImpact: matchingSuggestion.integrityImpact,
          privilegesRequired: matchingSuggestion.privilegesRequired,
          remediationLevel: matchingSuggestion.remediationLevel,
          reportConfidence: matchingSuggestion.reportConfidence,
          severityScope: matchingSuggestion.severityScope,
          threat: matchingSuggestion.threat,
          title: target.value,
          userInteraction: matchingSuggestion.userInteraction,
        });
      }
    },
    [addFindingInitialValues, getFindingMatchingSuggestion]
  );

  const MAX_DESCRIPTION_LENGTH = 500;
  const MAX_THREAT_LENGTH = 300;
  const titleSuggestions = _.isUndefined(suggestions)
    ? []
    : _.sortBy(
        suggestions.map(
          (suggestion: IFindingSuggestionData): string =>
            `${suggestion.code}. ${suggestion.title}`
        )
      );

  const validations = object().shape({
    attackComplexity: mixed().required(t("validations.required")),
    attackVector: mixed().required(t("validations.required")),
    availabilityImpact: mixed().required(t("validations.required")),
    confidentialityImpact: mixed().required(t("validations.required")),
    description: string()
      .required(t("validations.required"))
      .max(
        MAX_DESCRIPTION_LENGTH,
        t("validations.maxLength", { count: MAX_DESCRIPTION_LENGTH })
      )
      .test({
        exclusive: false,
        name: "invalidTextBeginning",
        test: (
          value: string | undefined,
          thisContext: TestContext
        ): ValidationError | boolean => {
          if (value === undefined) {
            return false;
          }
          const beginTextMatch: RegExpMatchArray | null = /^=/u.exec(value);

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
        name: "invalidTextField",
        test: (
          value: string | undefined,
          thisContext: TestContext
        ): ValidationError | boolean => {
          if (value === undefined) {
            return false;
          }
          const textMatch: RegExpMatchArray | null =
            /[^a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s(){}[\],./:;@&_$%'#*=¿?¡!+-]/u.exec(
              value
            );

          return _.isNull(textMatch)
            ? true
            : thisContext.createError({
                message: t("validations.invalidTextField", {
                  chars: `'${textMatch[0]}'`,
                }),
              });
        },
      }),
    exploitability: mixed().required(t("validations.required")),
    integrityImpact: mixed().required(t("validations.required")),
    privilegesRequired: mixed().required(t("validations.required")),
    remediationLevel: mixed().required(t("validations.required")),
    reportConfidence: mixed().required(t("validations.required")),
    severityScope: mixed().required(t("validations.required")),
    threat: string()
      .required(t("validations.required"))
      .max(
        MAX_THREAT_LENGTH,
        t("validations.maxLength", { count: MAX_THREAT_LENGTH })
      )
      .test({
        exclusive: false,
        name: "invalidTextBeginning",
        test: (
          value: string | undefined,
          thisContext: TestContext
        ): ValidationError | boolean => {
          if (value === undefined) {
            return false;
          }
          const beginTextMatch: RegExpMatchArray | null = /^=/u.exec(value);

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
        name: "invalidTextField",
        test: (
          value: string | undefined,
          thisContext: TestContext
        ): ValidationError | boolean => {
          if (value === undefined) {
            return false;
          }
          const textMatch: RegExpMatchArray | null =
            /[^a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s(){}[\],./:;@&_$%'#*=¿?¡!+-]/u.exec(
              value
            );

          return _.isNull(textMatch)
            ? true
            : thisContext.createError({
                message: t("validations.invalidTextField", {
                  chars: `'${textMatch[0]}'`,
                }),
              });
        },
      }),
    title: string()
      .required(t("validations.required"))
      .matches(/^\d{3}\. .+/gu, t("validations.draftTitle"))
      .test(
        "validFindingTypology",
        t("validations.draftTypology"),
        (value?: string): boolean => {
          if (value === undefined || _.isEmpty(value)) {
            return false;
          }

          return titleSuggestions.includes(value);
        }
      ),
    userInteraction: mixed().required(t("validations.required")),
  });

  return (
    <React.StrictMode>
      {!loading &&
      _.isEmpty(findings) &&
      _.isEmpty(rootFilter) &&
      !_.isEmpty(activeRoots) &&
      data?.group.userRole !== "hacker" ? (
        <Empty
          srcImage={searchingFindings}
          subtitle={t("searchFindings.noFindingsFound.subtitle")}
          title={t("searchFindings.noFindingsFound.title")}
        />
      ) : (
        <Table
          columnToggle={true}
          columnVisibilitySetter={setColumnVisibility}
          columnVisibilityState={columnVisibility}
          columns={tableColumns}
          data={filteredFindings}
          expandedRow={handleRowExpand}
          extraButtons={
            <React.Fragment>
              <Have I={"can_report_vulnerabilities"}>
                <Can I={"api_mutations_add_finding_mutate"}>
                  <Tooltip
                    id={"group.findings.buttons.add.tooltip.id"}
                    tip={t("group.findings.buttons.add.tooltip")}
                  >
                    <Button
                      disabled={_.isUndefined(groupData)}
                      icon={faPlus}
                      id={"addFinding"}
                      onClick={openAddFindingModal}
                    >
                      {t("group.findings.buttons.add.text")}
                    </Button>
                  </Tooltip>
                </Can>
              </Have>
              <Can do={"api_mutations_remove_finding_mutate"}>
                <Tooltip
                  id={"group.findings.buttons.delete.tooltip"}
                  tip={t("group.findings.buttons.delete.tooltip")}
                >
                  <Button
                    disabled={selectedFindings.length === 0 || deleting}
                    icon={faTrashAlt}
                    onClick={openDeleteModal}
                  >
                    {t("group.findings.buttons.delete.text")}
                  </Button>
                </Tooltip>
              </Can>
              <Can I={"api_resolvers_query_report__get_url_group_report"}>
                <Tooltip
                  id={"group.findings.buttons.report.tooltip.id"}
                  tip={t("group.findings.buttons.report.tooltip")}
                >
                  <Button
                    icon={faArrowRight}
                    iconSide={"right"}
                    id={"reports"}
                    onClick={openReportsModal}
                    variant={"primary"}
                  >
                    {t("group.findings.buttons.report.text")}
                  </Button>
                </Tooltip>
              </Can>
            </React.Fragment>
          }
          filters={
            <Filters
              dataset={findings}
              filters={filters}
              permaset={[filterVal, setFilterVal]}
              setFilters={setFilters}
            />
          }
          id={"tblFindings"}
          onRowClick={goToFinding}
          onSearch={handleSearch}
          rowSelectionSetter={
            permissions.can("api_mutations_remove_finding_mutate")
              ? setSelectedFindings
              : undefined
          }
          rowSelectionState={selectedFindings}
          searchPlaceholder={t("searchFindings.searchPlaceholder")}
          sortingSetter={setSorting}
          sortingState={sorting}
        />
      )}

      <ReportsModal
        enableCerts={hasMachine && filledGroupInfo}
        isOpen={isReportsModalOpen}
        onClose={closeReportsModal}
        typesOptions={Object.keys(typesOptions)}
        userRole={data?.group.userRole ?? "user"}
      />
      <Modal
        minWidth={500}
        onClose={closeAddFindingModal}
        open={isAddFindingModalOpen}
        title={t("group.findings.addModal.title")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={addFindingInitialValues}
          name={"addFinding"}
          onSubmit={handleAddFinding}
          validationSchema={validations}
        >
          {(): JSX.Element => {
            return (
              <Form>
                <Row>
                  <Col lg={100} md={100} sm={100}>
                    <Input
                      label={t("group.findings.addModal.fields.title.label")}
                      list={"ExList"}
                      name={"title"}
                      onChange={handleAddFindingTitleChange}
                      required={true}
                      suggestions={_.sortBy(titleSuggestions)}
                      tooltip={t(
                        "group.findings.addModal.fields.title.tooltip"
                      )}
                    />
                  </Col>
                </Row>
                <Row>
                  <Col lg={100} md={100} sm={100}>
                    <TextArea
                      label={t(
                        "group.findings.addModal.fields.description.label"
                      )}
                      name={"description"}
                      required={true}
                      tooltip={t(
                        "group.findings.addModal.fields.description.tooltip"
                      )}
                    />
                  </Col>
                </Row>
                <Row>
                  <Col lg={100} md={100} sm={100}>
                    <TextArea
                      label={t("group.findings.addModal.fields.threat.label")}
                      name={"threat"}
                      required={true}
                      tooltip={t(
                        "group.findings.addModal.fields.threat.tooltip"
                      )}
                    />
                  </Col>
                </Row>
                <Row>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.attackComplexity.label"
                      )}
                      name={"attackComplexity"}
                      required={true}
                    >
                      <option value={""} />
                      {Object.entries(attackComplexityValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t("searchFindings.tabSeverity.attackVector.label")}
                      name={"attackVector"}
                      required={true}
                    >
                      <option value={""} />
                      {Object.entries(attackVectorValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                </Row>
                <Row>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.availabilityImpact.label"
                      )}
                      name={"availabilityImpact"}
                      required={true}
                    >
                      <option value={""} />
                      {Object.entries(availabilityImpactValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.availabilityRequirement.label"
                      )}
                      name={"availabilityRequirement"}
                    >
                      <option value={""} />
                      {Object.entries(availabilityRequirementValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                </Row>
                <Row>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.confidentialityImpact.label"
                      )}
                      name={"confidentialityImpact"}
                      required={true}
                    >
                      <option value={""} />
                      {Object.entries(confidentialityImpactValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.confidentialityRequirement.label"
                      )}
                      name={"confidentialityRequirement"}
                    >
                      <option value={""} />
                      {Object.entries(confidentialityRequirementValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                </Row>
                <Row>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.exploitability.label"
                      )}
                      name={"exploitability"}
                      required={true}
                    >
                      <option value={""} />
                      {Object.entries(exploitabilityValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.integrityImpact.label"
                      )}
                      name={"integrityImpact"}
                      required={true}
                    >
                      <option value={""} />
                      {Object.entries(integrityImpactValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                </Row>
                <Row>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.integrityRequirement.label"
                      )}
                      name={"integrityRequirement"}
                    >
                      <option value={""} />
                      {Object.entries(integrityRequirementValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.modifiedAttackComplexity"
                      )}
                      name={"modifiedAttackComplexity"}
                    >
                      <option value={""} />
                      {Object.entries(attackComplexityValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                </Row>
                <Row>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.modifiedAttackVector"
                      )}
                      name={"modifiedAttackVector"}
                    >
                      <option value={""} />
                      {Object.entries(attackVectorValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.modifiedAvailabilityImpact"
                      )}
                      name={"modifiedAvailabilityImpact"}
                    >
                      <option value={""} />
                      {Object.entries(availabilityImpactValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                </Row>
                <Row>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.modifiedConfidentialityImpact"
                      )}
                      name={"modifiedConfidentialityImpact"}
                    >
                      <option value={""} />
                      {Object.entries(confidentialityImpactValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.modifiedIntegrityImpact"
                      )}
                      name={"modifiedIntegrityImpact"}
                    >
                      {Object.entries(integrityImpactValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                      <option value={""} />
                    </Select>
                  </Col>
                </Row>
                <Row>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.modifiedPrivilegesRequired"
                      )}
                      name={"modifiedPrivilegesRequired"}
                    >
                      <option value={""} />
                      {Object.entries(privilegesRequiredValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.modifiedUserInteraction"
                      )}
                      name={"modifiedUserInteraction"}
                    >
                      <option value={""} />
                      {Object.entries(userInteractionValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                </Row>
                <Row>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.modifiedSeverityScope"
                      )}
                      name={"modifiedSeverityScope"}
                    >
                      <option value={""} />
                      {Object.entries(severityScopeValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.privilegesRequired.label"
                      )}
                      name={"privilegesRequired"}
                      required={true}
                    >
                      <option value={""} />
                      {Object.entries(privilegesRequiredValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                </Row>
                <Row>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.remediationLevel.label"
                      )}
                      name={"remediationLevel"}
                      required={true}
                    >
                      <option value={""} />
                      {Object.entries(remediationLevelValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.reportConfidence.label"
                      )}
                      name={"reportConfidence"}
                      required={true}
                    >
                      <option value={""} />
                      {Object.entries(reportConfidenceValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                </Row>
                <Row>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.severityScope.label"
                      )}
                      name={"severityScope"}
                      required={true}
                    >
                      <option value={""} />
                      {Object.entries(severityScopeValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                  <Col lg={50} md={50} sm={100}>
                    <Select
                      label={t(
                        "searchFindings.tabSeverity.userInteraction.label"
                      )}
                      name={"userInteraction"}
                      required={true}
                    >
                      <option value={""} />
                      {Object.entries(userInteractionValues).map(
                        ([value, label]): JSX.Element => (
                          <option key={value} value={value}>
                            {t(label)}
                          </option>
                        )
                      )}
                    </Select>
                  </Col>
                </Row>
                <ModalConfirm
                  disabled={addingFinding}
                  onCancel={closeAddFindingModal}
                />
              </Form>
            );
          }}
        </Formik>
      </Modal>
      <Modal
        onClose={closeDeleteModal}
        open={isDeleteModalOpen}
        title={t("group.findings.deleteModal.title")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{}}
          name={"removeVulnerability"}
          onSubmit={handleDelete}
          validationSchema={object().shape({
            justification: mixed().required(t("validations.required")),
          })}
        >
          <Form id={"removeVulnerability"}>
            <FormGroup>
              <Select
                label={t("group.findings.deleteModal.justification.label")}
                name={"justification"}
              >
                <option value={""} />
                <option value={"DUPLICATED"}>
                  {t("group.findings.deleteModal.justification.duplicated")}
                </option>
                <option value={"FALSE_POSITIVE"}>
                  {t("group.findings.deleteModal.justification.falsePositive")}
                </option>
                <option value={"NOT_REQUIRED"}>
                  {t("group.findings.deleteModal.justification.notRequired")}
                </option>
              </Select>
            </FormGroup>
            <ModalConfirm disabled={isRunning} onCancel={closeDeleteModal} />
          </Form>
        </Formik>
      </Modal>
      <ExpertButton />
      {!loading && filteredFindings.length > 0 ? (
        <RiskExposureTour
          findingId={filteredFindings[0].id}
          findingRiskExposure={getRiskExposure(
            filteredFindings[0].totalOpenCVSSF,
            groupOpenCVSSF,
            filteredFindings[0].status
          )}
          step={1}
        />
      ) : null}
      <WelcomeModal />
    </React.StrictMode>
  );
};

export { GroupFindingsView };
