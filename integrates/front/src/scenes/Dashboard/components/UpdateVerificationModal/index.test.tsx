import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import {
  GET_ORGANIZATION_GROUP_NAMES,
  GET_USER_ORGANIZATIONS,
  GET_USER_TAGS,
} from "../../../../pages/home/dashboard/navbar/breadcrumb/queries";
import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import { ToDo } from "pages/home/dashboard/navbar/to-do";
import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "pages/home/dashboard/navbar/to-do/queries";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import {
  REQUEST_VULNERABILITIES_VERIFICATION,
  VERIFY_VULNERABILITIES,
} from "scenes/Dashboard/components/UpdateVerificationModal/queries";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/Finding-Content/queries";
import {
  GET_FINDING_INFO,
  GET_FINDING_NZR_VULNS,
  GET_FINDING_ZR_VULNS,
} from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/queries";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import { getCache } from "utils/apollo";
import { msgError } from "utils/notifications";

jest.mock("utils/notifications", (): Record<string, VoidFunction> => {
  const mocked = jest.requireActual<Record<string, VoidFunction>>(
    "utils/notifications"
  );
  jest.spyOn(mocked, "msgError").mockImplementation();

  return mocked;
});

describe("update verification component", (): void => {
  const btnConfirm = "components.modal.confirm";

  const mocksVulns: MockedResponse[] = [
    {
      request: {
        query: GET_FINDING_INFO,
        variables: {
          findingId: "",
        },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            id: "",
            releaseDate: "",
            remediated: true,
            status: "VULNERABLE",
            totalOpenCVSSF: 0.0,
            verified: false,
          },
        },
      },
    },
    {
      request: {
        query: GET_FINDING_ZR_VULNS,
        variables: {
          canRetrieveZeroRisk: false,
          findingId: "",
          first: 100,
        },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            zeroRiskConnection: undefined,
          },
        },
      },
    },
    {
      request: {
        query: GET_FINDING_NZR_VULNS,
        variables: {
          findingId: "",
          first: 100,
          state: "VULNERABLE",
        },
      },
      result: {
        data: {
          finding: {
            vulnerabilitiesConnection: {
              edges: [],
              pageInfo: {
                endCursor: "test-cursor=",
                hasNextPage: false,
              },
            },
          },
        },
      },
    },
    {
      request: {
        query: GET_ME_VULNERABILITIES_ASSIGNED_IDS,
        variables: {},
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            userEmail: "test@test.test",
            vulnerabilitiesAssigned: [],
          },
        },
      },
    },
    {
      request: {
        query: GET_USER_ORGANIZATIONS,
        variables: {},
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            organizations: [
              {
                __typename: "Organization",
                name: "okada",
              },
              {
                __typename: "Organization",
                name: "bulat",
              },
            ],
            userEmail: "test@fluidattacks.com",
          },
        },
      },
    },
    {
      request: {
        query: GET_ORGANIZATION_GROUP_NAMES,
        variables: {
          organizationId: "okada",
        },
      },
      result: {
        data: {
          organization: {
            __typename: "Organization",
            groups: [
              {
                name: "group1",
              },
              {
                name: "group2",
              },
            ],
            name: "org-test",
          },
        },
      },
    },
    {
      request: {
        query: GET_ORGANIZATION_ID,
        variables: {
          organizationName: "okada",
        },
      },
      result: {
        data: {
          organizationId: {
            __type: "Organization",
            id: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
            name: "okada",
          },
        },
      },
    },
    {
      request: {
        query: GET_USER_TAGS,
        variables: {
          organizationId: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
        },
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            tags: [{ __typename: "Tag", name: "another-tag" }],
            userEmail: "test@fluidattacks.com",
          },
        },
      },
    },
  ];

  it("should handle request verification", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const handleRefetchFindingAndGroup: jest.Mock = jest.fn();
    const handleRefetchFindingHeader: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      ...mocksVulns,
      {
        request: {
          query: REQUEST_VULNERABILITIES_VERIFICATION,
          variables: {
            findingId: "",
            justification:
              "This is a commenting test of a request verification in vulns",
            vulnerabilities: ["test"],
          },
        },
        result: {
          data: { requestVulnerabilitiesVerification: { success: true } },
        },
      },
      ...mocksVulns,
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[mocksMutation[3], ...mocksMutation, ...mocksVulns]}
        >
          <authzPermissionsContext.Provider value={new PureAbility([])}>
            <authzGroupContext.Provider value={new PureAbility([])}>
              <ToDo />
              <UpdateVerificationModal
                clearSelected={jest.fn()}
                handleCloseModal={handleOnClose}
                isReattacking={true}
                isVerifying={false}
                refetchData={handleRefetchData}
                refetchFindingAndGroup={handleRefetchFindingAndGroup}
                refetchFindingHeader={handleRefetchFindingHeader}
                setRequestState={handleRequestState}
                setVerifyState={jest.fn()}
                vulns={[
                  {
                    findingId: "",
                    groupName: "",
                    id: "test",
                    specific: "",
                    state: "VULNERABLE",
                    where: "",
                  },
                ]}
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "treatmentJustification" })
      ).toBeInTheDocument();
    });

    await userEvent.type(
      screen.getByRole("textbox", { name: "treatmentJustification" }),
      "This is a commenting test of a request verification in vulns"
    );

    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(handleOnClose).toHaveBeenCalledTimes(1);
    });

    expect(handleRequestState).toHaveBeenCalledTimes(1);
    expect(handleRefetchData).toHaveBeenCalledTimes(1);
  });

  it("should handle request verification error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const handleRefetchFindingAndGroup: jest.Mock = jest.fn();
    const handleRefetchFindingHeader: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      ...mocksVulns,
      {
        request: {
          query: REQUEST_VULNERABILITIES_VERIFICATION,
          variables: {
            findingId: "123",
            justification:
              "This is a commenting test of a request verification in vulns",
            vulnerabilities: ["test_error"],
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Request verification already requested"
            ),
            new GraphQLError("Exception - The git repository is outdated"),
            new GraphQLError(
              "Exception - The vulnerability has already been closed"
            ),
            new GraphQLError("Exception - Vulnerability not found"),
          ],
        },
      },
      ...mocksVulns,
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[mocksMutation[3], ...mocksMutation]}
        >
          <authzPermissionsContext.Provider value={new PureAbility([])}>
            <authzGroupContext.Provider value={new PureAbility([])}>
              <ToDo />
              <UpdateVerificationModal
                clearSelected={jest.fn()}
                handleCloseModal={handleOnClose}
                isReattacking={true}
                isVerifying={false}
                refetchData={handleRefetchData}
                refetchFindingAndGroup={handleRefetchFindingAndGroup}
                refetchFindingHeader={handleRefetchFindingHeader}
                setRequestState={handleRequestState}
                setVerifyState={jest.fn()}
                vulns={[
                  {
                    findingId: "123",
                    groupName: "",
                    id: "test_error",
                    specific: "",
                    state: "VULNERABLE",
                    where: "",
                  },
                ]}
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "treatmentJustification" }),
      "This is a commenting test of a request verification in vulns"
    );

    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(handleOnClose).toHaveBeenCalledTimes(1);
    });

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(4);
    });

    expect(handleRequestState).not.toHaveBeenCalled();
    expect(handleRefetchData).not.toHaveBeenCalled();
    expect(msgError).not.toHaveBeenCalledWith("There is an error :(");
  });

  it("should handle verify a request", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleVerifyState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const handleRefetchFindingAndGroup: jest.Mock = jest.fn();
    const handleRefetchFindingHeader: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      ...mocksVulns,
      {
        request: {
          query: VERIFY_VULNERABILITIES,
          variables: {
            closedVulns: ["test"],
            findingId: "",
            justification:
              "This is a commenting test of a verifying request verification in vulns",
            openVulns: [],
          },
        },
        result: { data: { verifyVulnerabilitiesRequest: { success: true } } },
      },
      {
        request: {
          query: GET_FINDING_HEADER,
          variables: {
            findingId: "",
          },
        },
        result: {
          data: {
            finding: {
              closedVulns: 0,
              currentState: "",
              id: "",
              maxOpenSeverityScore: 0.0,
              minTimeToRemediate: 60,
              openVulns: 0,
              releaseDate: null,
              reportDate: null,
              status: "VULNERABLE",
              title: "",
              totalOpenCVSSF: 0.0,
            },
          },
        },
      },
      ...mocksVulns,
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[mocksMutation[3], ...mocksMutation]}
        >
          <authzPermissionsContext.Provider value={new PureAbility([])}>
            <authzGroupContext.Provider value={new PureAbility([])}>
              <ToDo />
              <UpdateVerificationModal
                clearSelected={jest.fn()}
                handleCloseModal={handleOnClose}
                isReattacking={false}
                isVerifying={true}
                refetchData={handleRefetchData}
                refetchFindingAndGroup={handleRefetchFindingAndGroup}
                refetchFindingHeader={handleRefetchFindingHeader}
                setRequestState={jest.fn()}
                setVerifyState={handleVerifyState}
                vulns={[
                  {
                    findingId: "",
                    groupName: "",
                    id: "test",
                    specific: "",
                    state: "VULNERABLE",
                    where: "",
                  },
                ]}
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "treatmentJustification" }),
      "This is a commenting test of a verifying request verification in vulns"
    );
    await userEvent.click(
      within(screen.getByRole("table")).getByRole("checkbox")
    );

    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(handleOnClose).toHaveBeenCalledTimes(1);
    });

    expect(handleVerifyState).toHaveBeenCalledTimes(1);
    expect(handleRefetchData).toHaveBeenCalledTimes(1);
  });

  it("should handle verify a request error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleVerifyState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const handleRefetchFindingAndGroup: jest.Mock = jest.fn();
    const handleRefetchFindingHeader: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      ...mocksVulns,
      {
        request: {
          query: VERIFY_VULNERABILITIES,
          variables: {
            closedVulns: [],
            findingId: "",
            justification:
              "This is a commenting test of a verifying request verification in vulns",
            openVulns: ["test_error"],
          },
        },
        result: {
          errors: [
            new GraphQLError("Exception - Error verification not requested"),
            new GraphQLError("Exception - Vulnerability not found"),
            new GraphQLError("Unexpected error"),
          ],
        },
      },
      ...mocksVulns,
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[...mocksMutation, ...mocksMutation]}
        >
          <authzPermissionsContext.Provider value={new PureAbility([])}>
            <authzGroupContext.Provider value={new PureAbility([])}>
              <ToDo />
              <UpdateVerificationModal
                clearSelected={jest.fn()}
                handleCloseModal={handleOnClose}
                isReattacking={false}
                isVerifying={true}
                refetchData={handleRefetchData}
                refetchFindingAndGroup={handleRefetchFindingAndGroup}
                refetchFindingHeader={handleRefetchFindingHeader}
                setRequestState={jest.fn()}
                setVerifyState={handleVerifyState}
                vulns={[
                  {
                    findingId: "",
                    groupName: "",
                    id: "test_error",
                    specific: "",
                    state: "VULNERABLE",
                    where: "",
                  },
                ]}
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "treatmentJustification" }),
      "This is a commenting test of a verifying request verification in vulns"
    );
    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(handleOnClose).toHaveBeenCalledTimes(1);
    });

    expect(handleVerifyState).not.toHaveBeenCalled();
    expect(handleRefetchData).not.toHaveBeenCalled();
  });
});
