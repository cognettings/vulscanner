import { useApolloClient, useMutation, useQuery } from "@apollo/client";
import type { ApolloError, FetchResult } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type {
  ColumnDef,
  SortingState,
  VisibilityState,
} from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, {
  Fragment,
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { ActionButtons } from "./ActionButtons";
import { editableAttackedLinesFormatter } from "./formatters/editableAttackedLinesFormatter";
import { HandleAdditionModal } from "./HandleAdditionModal";
import { HandleEditionModal } from "./HandleEditionModal";
import { SortsSuggestionsModal } from "./SortsSuggestionsModal";
import { SortsSuggestionsButton } from "./styles";
import { formatToeLines, unformatFilterValues } from "./utils";

import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { SortDropdown } from "components/SortDropdown";
import type { ISelectedOptions } from "components/SortDropdown/types";
import { Table } from "components/Table";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/Table/types";
import { authzPermissionsContext } from "context/authz/config";
import { useStoredState } from "hooks";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import {
  GET_TOE_LINES,
  VERIFY_TOE_LINES,
} from "scenes/Dashboard/containers/Group-Content/ToeContent/GroupToeLinesView/queries";
import type {
  IGroupToeLinesViewProps,
  ISortsSuggestionAttr,
  IToeLinesConnection,
  IToeLinesData,
  IToeLinesEdge,
  IVerifyToeLinesResultAttr,
} from "scenes/Dashboard/containers/Group-Content/ToeContent/GroupToeLinesView/types";
import { formatPercentage } from "utils/formatHelpers";
import { getErrors } from "utils/helpers";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const GroupToeLinesView: React.FC<IGroupToeLinesViewProps> = ({
  isInternal,
}: IGroupToeLinesViewProps): JSX.Element => {
  const { t } = useTranslation();
  const client = useApolloClient();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateAttackedLines: boolean = permissions.can(
    "api_mutations_update_toe_lines_attacked_lines_mutate"
  );
  const canGetAttackedAt: boolean = permissions.can(
    "api_resolvers_toe_lines_attacked_at_resolve"
  );
  const canGetAttackedBy: boolean = permissions.can(
    "api_resolvers_toe_lines_attacked_by_resolve"
  );
  const canGetAttackedLines: boolean = permissions.can(
    "api_resolvers_toe_lines_attacked_lines_resolve"
  );
  const canGetBePresentUntil: boolean = permissions.can(
    "api_resolvers_toe_lines_be_present_until_resolve"
  );
  const canGetComments: boolean = permissions.can(
    "api_resolvers_toe_lines_comments_resolve"
  );
  const canGetFirstAttackAt: boolean = permissions.can(
    "api_resolvers_toe_lines_first_attack_at_resolve"
  );
  const canSeeCoverage: boolean = permissions.can("see_toe_lines_coverage");
  const canSeeDaysToAttack: boolean = permissions.can(
    "see_toe_lines_days_to_attack"
  );

  const { groupName } = useParams<{ groupName: string }>();

  const [isAdding, setIsAdding] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [toeLinesSort, setToeLinesSort] = useState({
    field: "SORTS_PRIORITY_FACTOR",
    order: "DESC",
  });
  const [selectedToeLinesDatas, setSelectedToeLinesDatas] = useState<
    IToeLinesData[]
  >([]);
  const [isSortsSuggestionsModalOpen, setIsSortsSuggestionsModalOpen] =
    useState(false);
  const [filters, setFilters] = useState<IFilter<IToeLinesData>[]>([]);
  const [
    selectedToeLinesSortsSuggestions,
    setSelectedToeLinesSortsSuggestions,
  ] = useState<ISortsSuggestionAttr[]>();
  const closeSortsSuggestionsModal: () => void = useCallback((): void => {
    setIsSortsSuggestionsModalOpen(false);
  }, []);

  const [columnVisibility, setColumnVisibility] =
    useStoredState<VisibilityState>(
      "tblToeLines-visibilityState",
      {
        attackedBy: false,
        bePresent: false,
        bePresentUntil: false,
        daysToAttack: false,
        filename: false,
        firstAttackAt: false,
        lastAuthor: false,
        seenAt: false,
        sortsPriorityFactor: false,
        sortsSuggestions: false,
      },
      localStorage
    );
  const [sorting, setSorting] = useStoredState<SortingState>(
    "tblToeLines-sortingState",
    []
  );

  const formatDate: (date: Date | undefined) => string = (
    date: Date | undefined
  ): string => {
    if (_.isUndefined(date)) {
      return "";
    }

    // eslint-disable-next-line new-cap
    return Intl.DateTimeFormat("fr-CA", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    }).format(date);
  };
  const formatBoolean = (value: boolean): string =>
    value ? t("group.toe.lines.yes") : t("group.toe.lines.no");
  const formatHasVulnerabilityStatus = (value: boolean): string =>
    value ? t("group.toe.lines.vulnerable") : t("group.toe.lines.safe");
  const formatSortsPriorityFactor = (sortsPriorityFactor: number): string =>
    sortsPriorityFactor >= 0 ? `${sortsPriorityFactor.toString()} %` : "n/a";

  const handleOnClick = useCallback(
    (sortsSuggestions: ISortsSuggestionAttr[] | null): (() => void) =>
      (): void => {
        if (!_.isNil(sortsSuggestions)) {
          setSelectedToeLinesSortsSuggestions(sortsSuggestions);
          setIsSortsSuggestionsModalOpen(true);
        }
      },
    []
  );

  const formatSortsSuggestions = (
    sortsSuggestions: ISortsSuggestionAttr[] | null
  ): JSX.Element => {
    const value =
      _.isNil(sortsSuggestions) || sortsSuggestions.length === 0
        ? "None"
        : `${sortsSuggestions.length} available`;

    return (
      <SortsSuggestionsButton
        isNone={value === "None"}
        onClick={handleOnClick(sortsSuggestions)}
      >
        {value}
      </SortsSuggestionsButton>
    );
  };

  // // GraphQL operations
  const [handleVerifyToeLines] = useMutation<IVerifyToeLinesResultAttr>(
    VERIFY_TOE_LINES,
    {
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - The toe lines has been updated by another operation":
              msgError(t("group.toe.lines.editModal.alerts.alreadyUpdate"));
              break;
            case "Exception - The attacked lines must be between 0 and the loc (lines of code)":
              msgError(
                t(
                  "group.toe.lines.editModal.alerts.invalidAttackedLinesBetween"
                )
              );
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred verifying a toe lines", error);
          }
        });
      },
    }
  );
  const filterToSearch: Record<string, unknown> = filters.reduce(
    (prev, curr): Record<string, string> => {
      const currentValue = unformatFilterValues(curr);

      return {
        ...prev,
        ...currentValue,
      };
    },
    {}
  );
  const toeLinesPermissions = useMemo(
    (): Record<string, boolean | string> => ({
      canGetAttackedAt,
      canGetAttackedBy,
      canGetAttackedLines,
      canGetBePresentUntil,
      canGetComments,
      canGetFirstAttackAt,
      groupName,
    }),
    [
      canGetAttackedAt,
      canGetAttackedBy,
      canGetAttackedLines,
      canGetBePresentUntil,
      canGetComments,
      canGetFirstAttackAt,
      groupName,
    ]
  );
  const toeLinesVariables = useMemo(
    (): Record<string, boolean | object | string> => ({
      ...toeLinesPermissions,
      ...filterToSearch,
      sort: toeLinesSort,
    }),
    [filterToSearch, toeLinesPermissions, toeLinesSort]
  );

  const { data, fetchMore, refetch } = useQuery<{
    group: {
      toeLinesConnection: IToeLinesConnection;
    };
  }>(GET_TOE_LINES, {
    fetchPolicy: "network-only",
    nextFetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load group toe lines", error);
      });
    },
    variables: {
      ...toeLinesVariables,
      first: 150,
    },
  });
  const size = data?.group.toeLinesConnection.total;

  const toeLinesEdges: IToeLinesEdge[] =
    data === undefined ? [] : data.group.toeLinesConnection.edges;

  const toeLines: IToeLinesData[] = formatToeLines(toeLinesEdges);

  const handleUpdateAttackedLines: (
    rootId: string,
    filename: string,
    attackedLines: number
  ) => Promise<void> = async (
    rootId: string,
    filename: string,
    attackedLines: number
  ): Promise<void> => {
    const result = await handleVerifyToeLines({
      variables: {
        ...toeLinesPermissions,
        attackedLines,
        filename,
        groupName,
        rootId,
        shouldGetNewToeLines: true,
      },
    });

    if (
      !_.isNil(result.data) &&
      result.data.updateToeLinesAttackedLines.success
    ) {
      msgSuccess(
        t("group.toe.lines.alerts.verifyToeLines.success"),
        t("groupAlerts.updatedTitle")
      );
      const updatedToeLines = result.data.updateToeLinesAttackedLines.toeLines;

      if (!_.isUndefined(updatedToeLines)) {
        client.writeQuery({
          data: {
            ...data,
            group: {
              ...data?.group,
              toeLinesConnection: {
                ...data?.group.toeLinesConnection,
                edges: data?.group.toeLinesConnection.edges.map(
                  (value: IToeLinesEdge): IToeLinesEdge =>
                    value.node.root.id === rootId &&
                    value.node.filename === filename
                      ? {
                          node: updatedToeLines,
                        }
                      : { node: value.node }
                ),
              },
            },
          },
          query: GET_TOE_LINES,
          variables: {
            ...toeLinesVariables,
            first: 150,
          },
        });
      }
    }
  };

  const columns: ColumnDef<IToeLinesData>[] = [
    {
      accessorKey: "rootNickname",
      header: t("group.toe.lines.root"),
    },
    {
      accessorKey: "filename",
      header: t("group.toe.lines.filename"),
    },
    {
      accessorKey: "loc",
      header: t("group.toe.lines.loc"),
    },
    {
      accessorFn: (row: IToeLinesData): string =>
        formatHasVulnerabilityStatus(row.hasVulnerabilities),
      cell: (cell: ICellHelper<IToeLinesData>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: t("group.toe.lines.status"),
      id: "hasVulnerabilities",
    },
    {
      accessorKey: "modifiedDate",
      cell: (cell: ICellHelper<IToeLinesData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.lines.modifiedDate"),
    },
    {
      accessorKey: "lastCommit",
      header: t("group.toe.lines.lastCommit"),
    },
    {
      accessorKey: "lastAuthor",
      header: t("group.toe.lines.lastAuthor"),
    },
    {
      accessorKey: "seenAt",
      cell: (cell: ICellHelper<IToeLinesData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.lines.seenAt"),
    },
    {
      accessorKey: "sortsPriorityFactor",
      cell: (cell: ICellHelper<IToeLinesData>): string =>
        formatSortsPriorityFactor(cell.getValue()),
      header: t("group.toe.lines.sortsPriorityFactor"),
    },
    {
      accessorFn: (row: IToeLinesData): string => formatBoolean(row.bePresent),
      header: t("group.toe.lines.bePresent"),
      id: "bePresent",
    },
    {
      accessorFn: (row): number => row.coverage * 100,
      cell: (cell: ICellHelper<IToeLinesData>): string =>
        formatPercentage(cell.row.original.coverage),
      header: t("group.toe.lines.coverage"),
      id: "coverage",
    },
    {
      accessorKey: "attackedLines",
      cell: (cell: ICellHelper<IToeLinesData>): JSX.Element | string =>
        editableAttackedLinesFormatter(
          canUpdateAttackedLines,
          handleUpdateAttackedLines,
          cell.row.original
        ),
      header: t("group.toe.lines.attackedLines"),
      id: "attackedLines",
    },
    {
      accessorKey: "daysToAttack",
      header: t("group.toe.lines.daysToAttack"),
      id: "daysToAttack",
    },
    {
      accessorKey: "attackedAt",
      cell: (cell: ICellHelper<IToeLinesData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.lines.attackedAt"),
      id: "attackedAt",
    },
    {
      accessorKey: "attackedBy",
      header: t("group.toe.lines.attackedBy"),
      id: "attackedBy",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "firstAttackAt",
      cell: (cell: ICellHelper<IToeLinesData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.lines.firstAttackAt"),
      id: "firstAttackAt",
    },
    {
      accessorKey: "comments",
      header: t("group.toe.lines.comments"),
      id: "comments",
    },
    {
      accessorKey: "sortsSuggestions",
      cell: (cell: ICellHelper<IToeLinesData>): JSX.Element =>
        formatSortsSuggestions(cell.getValue()),
      header: t("group.toe.lines.sortsSuggestions"),
      id: "sortsSuggestions",
    },
    {
      accessorKey: "bePresentUntil",
      cell: (cell: ICellHelper<IToeLinesData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.lines.bePresentUntil"),
      id: "bePresentUntil",
    },
  ];

  const baseFilters: IFilter<IToeLinesData>[] = [
    {
      id: "filename",
      key: "filename",
      label: t("group.toe.lines.filename"),
      type: "text",
    },
    {
      id: "loc",
      key: "loc",
      label: t("group.toe.lines.loc"),
      minMaxRangeValues: [1, 350],
      type: "numberRange",
    },
    {
      id: "hasVulnerabilities",
      key: "hasVulnerabilities",
      label: t("group.toe.lines.status"),
      selectOptions: [
        { header: formatHasVulnerabilityStatus(true), value: "true" },
        { header: formatHasVulnerabilityStatus(false), value: "false" },
      ],
      type: "select",
    },
    {
      id: "modifiedDate",
      key: "modifiedDate",
      label: t("group.toe.lines.modifiedDate"),
      type: "dateRange",
    },
    {
      id: "lastCommit",
      key: "lastCommit",
      label: t("group.toe.lines.lastCommit"),
      type: "text",
    },
    {
      id: "lastAuthor",
      key: "lastAuthor",
      label: t("group.toe.lines.lastAuthor"),
      type: "text",
    },
    {
      id: "seenAt",
      key: "seenAt",
      label: t("group.toe.lines.seenAt"),
      type: "dateRange",
    },
    {
      id: "sortsPriorityFactor",
      key: "sortsPriorityFactor",
      label: t("group.toe.lines.sortsPriorityFactor"),
      minMaxRangeValues: [0, 100],
      type: "numberRange",
    },
    {
      id: "bePresent",
      key: "bePresent",
      label: t("group.toe.lines.bePresent"),
      selectOptions: [
        { header: formatBoolean(true), value: "true" },
        { header: formatBoolean(false), value: "false" },
      ],
      type: "select",
    },
    {
      id: "attackedLines",
      key: "attackedLines",
      label: t("group.toe.lines.attackedLines"),
      minMaxRangeValues: [0, 350],
      type: "numberRange",
    },
    {
      id: "coverage",
      isBackFilter: true,
      key: "coverage",
      label: t("group.toe.lines.coverage"),
      minMaxRangeValues: [0, 100],
      type: "numberRange",
    },
    {
      id: "attackedAt",
      key: "attackedAt",
      label: t("group.toe.lines.attackedAt"),
      type: "dateRange",
    },
    {
      id: "attackedBy",
      key: "attackedBy",
      label: t("group.toe.lines.attackedBy"),
      type: "text",
    },
    {
      id: "firstAttackAt",
      key: "firstAttackAt",
      label: t("group.toe.lines.firstAttackAt"),
      type: "dateRange",
    },
    {
      id: "comments",
      key: "comments",
      label: t("group.toe.lines.comments"),
      type: "text",
    },
    {
      id: "bePresentUntil",
      key: "bePresentUntil",
      label: t("group.toe.lines.bePresentUntil"),
      type: "dateRange",
    },
  ];

  const dataSortOptions: ISelectedOptions[] = [
    {
      header: "Priority",
      value: "SORTS_PRIORITY_FACTOR",
    },
    {
      header: "LOC",
      value: "LOC",
    },
  ];

  const tablecolumns = columns.filter((column): boolean => {
    switch (column.id) {
      case "coverage":
        return isInternal && canSeeCoverage && canGetAttackedLines;
      case "attackedLines":
        return isInternal && canGetAttackedLines;
      case "daysToAttack":
        return isInternal && canSeeDaysToAttack && canGetAttackedAt;
      case "attackedAt":
        return isInternal && canGetAttackedAt;
      case "attackedBy":
        return isInternal && canGetAttackedBy;
      case "firstAttackAt":
        return isInternal && canGetFirstAttackAt;
      case "comments":
        return isInternal && canGetComments;
      case "sortsSuggestions":
        return isInternal;
      case "bePresentUntil":
        return isInternal && canGetBePresentUntil;
      default:
        return true;
    }
  });

  const tableFilters = baseFilters.filter((filter): boolean => {
    switch (filter.id) {
      case "coverage":
        return isInternal && canSeeCoverage && canGetAttackedLines;
      case "attackedLines":
        return isInternal && canGetAttackedLines;
      case "daysToAttack":
        return isInternal && canSeeDaysToAttack && canGetAttackedAt;
      case "attackedAt":
        return isInternal && canGetAttackedAt;
      case "attackedBy":
        return isInternal && canGetAttackedBy;
      case "firstAttackAt":
        return isInternal && canGetFirstAttackAt;
      case "comments":
        return isInternal && canGetComments;
      case "sortsSuggestions":
        return isInternal;
      case "bePresentUntil":
        return isInternal && canGetBePresentUntil;
      default:
        return true;
    }
  });

  useEffect((): void => {
    setFilters(tableFilters);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const setDataOrder = useCallback((field: string, order: string): void => {
    setToeLinesSort({ field, order });
  }, []);

  const filteredToeLines = useFilters(toeLines, filters);

  const handleNextPage = useCallback(async (): Promise<void> => {
    const pageInfo =
      data === undefined
        ? { endCursor: [], hasNextPage: false }
        : {
            endCursor: JSON.parse(
              data.group.toeLinesConnection.pageInfo.endCursor
            ),
            hasNextPage: data.group.toeLinesConnection.pageInfo.hasNextPage,
          };

    if (pageInfo.hasNextPage) {
      await fetchMore({ variables: { after: pageInfo.endCursor } });
    }
  }, [data, fetchMore]);

  const toggleAdd = useCallback((): void => {
    setIsAdding(!isAdding);
  }, [isAdding]);

  const toggleEdit = useCallback((): void => {
    setIsEditing(!isEditing);
  }, [isEditing]);

  const getUpdatedEdges = useCallback(
    (
      edges: IToeLinesEdge[],
      result: FetchResult<IVerifyToeLinesResultAttr>,
      toeLine: IToeLinesData
    ): IToeLinesEdge[] | undefined => {
      if (
        !_.isNil(result.data) &&
        result.data.updateToeLinesAttackedLines.success
      ) {
        const updatedToeLine = result.data.updateToeLinesAttackedLines.toeLines;
        if (_.isUndefined(updatedToeLine)) {
          return undefined;
        }
        const isChanged: boolean = edges.reduce(
          (previousValue: boolean, value: IToeLinesEdge): boolean =>
            value.node.root.id === toeLine.rootId &&
            value.node.filename === toeLine.filename
              ? true
              : previousValue,
          false
        );

        if (
          updatedToeLine.root.id !== toeLine.rootId ||
          updatedToeLine.filename !== toeLine.filename ||
          !isChanged
        ) {
          return undefined;
        }

        return edges.map(
          (value: IToeLinesEdge): IToeLinesEdge =>
            value.node.root.id === toeLine.rootId &&
            value.node.filename === toeLine.filename
              ? {
                  node: updatedToeLine,
                }
              : { node: value.node }
        );
      }

      return undefined;
    },
    []
  );

  const updateQuery = useCallback(
    (
      updatedEdges: IToeLinesEdge[],
      currentData:
        | {
            group: {
              toeLinesConnection: IToeLinesConnection;
            };
          }
        | undefined
    ): void => {
      client.writeQuery({
        data: {
          ...currentData,
          group: {
            ...currentData?.group,
            toeLinesConnection: {
              ...currentData?.group.toeLinesConnection,
              edges: updatedEdges,
            },
          },
        },
        query: GET_TOE_LINES,
        variables: {
          ...toeLinesVariables,
          first: 150,
        },
      });
    },
    [client, toeLinesVariables]
  );

  const handleOnVerifyCompleted = useCallback(
    async (
      results: FetchResult<IVerifyToeLinesResultAttr>[]
    ): Promise<void> => {
      const currentEdges: IToeLinesEdge[] =
        data?.group.toeLinesConnection.edges ?? [];
      const updatedEdges = results.reduce(
        (
          previousValue: IToeLinesEdge[],
          currentValue: FetchResult<IVerifyToeLinesResultAttr>
        ): IToeLinesEdge[] => {
          const currentUpdated = selectedToeLinesDatas.map(
            (toeLine): IToeLinesEdge[] | undefined =>
              getUpdatedEdges(previousValue, currentValue, toeLine)
          );
          const filteredUpdated = currentUpdated.filter(
            (value): boolean => value !== undefined
          );

          return _.last(filteredUpdated) ?? previousValue;
        },
        currentEdges
      );
      updateQuery(
        updatedEdges.length === currentEdges.length
          ? updatedEdges
          : currentEdges,
        data
      );
      if (
        !_.isNil(results[0].data) &&
        results[0].data.updateToeLinesAttackedLines.success
      ) {
        msgSuccess(
          t("group.toe.lines.alerts.verifyToeLines.success"),
          t("groupAlerts.updatedTitle")
        );
        if (selectedToeLinesDatas.length >= 10) {
          await refetch();
        }
        setSelectedToeLinesDatas([]);
      }
    },
    [data, getUpdatedEdges, refetch, selectedToeLinesDatas, t, updateQuery]
  );

  const handleVerify = useCallback(async (): Promise<void> => {
    setIsVerifying(true);
    const results = await Promise.all(
      selectedToeLinesDatas.map(
        async (
          toeInputData: IToeLinesData
        ): Promise<FetchResult<IVerifyToeLinesResultAttr>> =>
          handleVerifyToeLines({
            variables: {
              ...toeLinesPermissions,
              filename: toeInputData.filename,
              groupName,
              rootId: toeInputData.rootId,
              shouldGetNewToeLines: selectedToeLinesDatas.length < 10,
            },
          })
      )
    );
    const errors = getErrors<IVerifyToeLinesResultAttr>(results);

    if (!_.isEmpty(results) && _.isEmpty(errors)) {
      await handleOnVerifyCompleted(results);
    } else {
      await refetch();
    }
    setIsVerifying(false);
  }, [
    selectedToeLinesDatas,
    handleVerifyToeLines,
    toeLinesPermissions,
    groupName,
    handleOnVerifyCompleted,
    refetch,
  ]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <Table
        columnToggle={true}
        columnVisibilitySetter={setColumnVisibility}
        columnVisibilityState={columnVisibility}
        columns={tablecolumns}
        data={filteredToeLines}
        enableSorting={false}
        exportCsv={false}
        extraButtons={
          <Fragment>
            <SortDropdown
              id={"lines"}
              mappedOptions={dataSortOptions}
              onChange={setDataOrder}
            />
            <ActionButtons
              areToeLinesDatasSelected={selectedToeLinesDatas.length > 0}
              isAdding={isAdding}
              isEditing={isEditing}
              isInternal={isInternal}
              isVerifying={isVerifying}
              onAdd={toggleAdd}
              onEdit={toggleEdit}
              onVerify={handleVerify}
            />
          </Fragment>
        }
        filters={
          <Filters
            dataset={toeLines}
            filters={filters}
            setFilters={setFilters}
          />
        }
        id={"tblToeLines"}
        onNextPage={handleNextPage}
        rowSelectionSetter={
          isInternal && canUpdateAttackedLines
            ? setSelectedToeLinesDatas
            : undefined
        }
        rowSelectionState={selectedToeLinesDatas}
        size={size}
        sortingSetter={setSorting}
        sortingState={sorting}
      />
      <HandleAdditionModal
        groupName={groupName}
        handleCloseModal={toggleAdd}
        isAdding={isAdding}
        refetchData={refetch}
      />
      {isEditing ? (
        <HandleEditionModal
          groupName={groupName}
          handleCloseModal={toggleEdit}
          refetchData={refetch}
          selectedToeLinesDatas={selectedToeLinesDatas}
          setSelectedToeLinesDatas={setSelectedToeLinesDatas}
        />
      ) : undefined}
      <SortsSuggestionsModal
        closeSortsSuggestionsModal={closeSortsSuggestionsModal}
        isSortsSuggestionsOpen={isSortsSuggestionsModalOpen}
        selectedSortsSuggestions={selectedToeLinesSortsSuggestions}
      />
    </React.StrictMode>
  );
};

export { GroupToeLinesView };
