import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_ME_VULNERABILITIES_ASSIGNED } from "./queries";

import { authzPermissionsContext } from "context/authz/config";
import { GET_GROUP_USERS } from "scenes/Dashboard/components/Vulnerabilities/queries";
import { TasksVulnerabilities } from "scenes/Dashboard/containers/Tasks-Content/Vulnerabilities";
import { GET_USER_ORGANIZATIONS_GROUPS } from "scenes/Dashboard/queries";
import { getCache } from "utils/apollo";

describe("todoVulnerabilitiesView", (): void => {
  const mocksVulnerabilities: MockedResponse = {
    request: {
      query: GET_ME_VULNERABILITIES_ASSIGNED,
    },
    result: {
      data: {
        me: {
          __typename: "Me",
          userEmail: "test@test.test",
          vulnerabilitiesAssigned: [
            {
              __typename: "Vulnerability",
              advisories: null,
              externalBugTrackingSystem: null,
              finding: {
                __typename: "Finding",
                id: "",
                title: "",
              },
              findingId: "422286126",
              groupName: "group1",
              id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
              lastStateDate: "2019-07-05 09:56:40",
              lastTreatmentDate: "2019-07-05 09:56:40",
              lastVerificationDate: null,
              remediated: false,
              reportDate: "2019-07-05 09:56:40",
              rootNickname: "https:",
              severity: "",
              severityTemporalScore: 3.9,
              source: "asm",
              specific: "specific-1",
              state: "VULNERABLE",
              stream: "home > blog > articulo",
              tag: "tag-1, tag-2",
              technique: "DAST",
              treatmentAcceptanceDate: "",
              treatmentAcceptanceStatus: "",
              treatmentAssigned: "assigned-user-1",
              treatmentDate: "2019-07-05 09:56:40",
              treatmentJustification: "test progress justification",
              treatmentStatus: "ACCEPTED",
              treatmentUser: "test@test.test",
              verification: null,
              vulnerabilityType: "inputs",
              where: "https://example.com/inputs",
              zeroRisk: null,
            },
            {
              __typename: "Vulnerability",
              advisories: null,
              externalBugTrackingSystem: null,
              finding: {
                __typename: "Finding",
                id: "",
                title: "",
              },
              findingId: "422286126",
              groupName: "group2",
              id: "6903f3e4-a8ee-4a5d-ac38-fb738ec7e540",
              lastStateDate: "2019-07-05 09:56:40",
              lastTreatmentDate: "2019-07-05 09:56:40",
              lastVerificationDate: null,
              remediated: false,
              reportDate: "2020-07-05 09:56:40",
              rootNickname: "https:",
              severity: "",
              severityTemporalScore: 3.4,
              source: "asm",
              specific: "specific-3",
              state: "VULNERABLE",
              stream: null,
              tag: "tag-3",
              technique: "SAST",
              treatmentAcceptanceDate: "",
              treatmentAcceptanceStatus: "",
              treatmentAssigned: "assigned-user-1",
              treatmentDate: "2019-07-05 09:56:40",
              treatmentJustification: "test progress justification",
              treatmentStatus: "IN_PROGRESS",
              treatmentUser: "test@test.test",
              verification: null,
              vulnerabilityType: "lines",
              where: "https://example.com/tests",
              zeroRisk: null,
            },
          ],
        },
      },
    },
  };

  const mocksUserGroups: MockedResponse = {
    request: {
      query: GET_USER_ORGANIZATIONS_GROUPS,
    },
    result: {
      data: {
        me: {
          __typename: "Me",
          organizations: [
            {
              groups: [
                {
                  name: "group1",
                  permissions: [
                    "api_mutations_request_vulnerabilities_verification_mutate",
                    "api_mutations_update_vulnerabilities_treatment_mutate",
                    "api_resolvers_group_stakeholders_resolve",
                  ],
                  serviceAttributes: ["is_continuous"],
                },
                {
                  name: "group2",
                  permissions: [
                    "api_mutations_request_vulnerabilities_verification_mutate",
                    "api_mutations_update_vulnerabilities_treatment_mutate",
                  ],
                  serviceAttributes: [],
                },
              ],
              name: "orgtest",
            },
          ],
          userEmail: "test@test.test",
        },
      },
    },
  };

  const mocksGroupStakeholder: MockedResponse[] = [
    {
      request: {
        query: GET_GROUP_USERS,
        variables: {
          groupName: "group2",
        },
      },
      result: {
        data: {
          group: {
            name: "group2",
            stakeholders: [
              {
                email: "manager2_test@test.test",
                invitationState: "REGISTERED",
              },
            ],
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_USERS,
        variables: {
          groupName: "group1",
        },
      },
      result: {
        data: {
          group: {
            name: "group1",
            stakeholders: [
              {
                email: "manager1_test@test.test",
                invitationState: "REGISTERED",
              },
            ],
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof TasksVulnerabilities).toBe("function");
  });

  it("should handle reattack button basic", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_vulnerability_hacker_resolve" },
    ]);

    const { container } = render(
      <MemoryRouter initialEntries={["/todos"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Route path={"/todos"}>
            <MockedProvider
              addTypename={true}
              cache={getCache()}
              mocks={[
                mocksUserGroups,
                mocksVulnerabilities,
                mocksVulnerabilities,
                ...mocksGroupStakeholder,
                mocksUserGroups,
              ]}
            >
              <TasksVulnerabilities />
            </MockedProvider>
          </Route>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.getByRole("cell", { name: "https://example.com/inputs" })
      ).toBeInTheDocument();
    });

    await userEvent.click(
      container.querySelector("#refresh-assigned") as Element
    );

    expect(screen.getAllByRole("checkbox")[1]).not.toBeChecked();

    await userEvent.click(screen.getAllByRole("checkbox")[1]);
    await userEvent.click(screen.getAllByRole("checkbox")[2]);

    expect(screen.getAllByRole("checkbox")[1]).toBeChecked();

    await waitFor((): void => {
      expect(
        screen.getByText("searchFindings.tabDescription.requestVerify.text")
      ).not.toBeDisabled();
    });

    expect(
      screen.queryByText(
        "searchFindings.tabDescription.remediationModal.justification"
      )
    ).not.toBeInTheDocument();

    await userEvent.click(
      screen.getByText("searchFindings.tabDescription.requestVerify.text")
    );

    await waitFor((): void => {
      expect(
        screen.queryByText(
          "searchFindings.tabDescription.remediationModal.justification"
        )
      ).toBeInTheDocument();
    });
  });

  it("should handle edit button basic", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_vulnerability_hacker_resolve" },
    ]);

    render(
      <MemoryRouter initialEntries={["/todos"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MockedProvider addTypename={false} mocks={[]}>
            <Route path={"/todos"}>
              <MockedProvider
                addTypename={true}
                cache={getCache()}
                mocks={[
                  mocksUserGroups,
                  mocksVulnerabilities,
                  ...mocksGroupStakeholder,
                  mocksUserGroups,
                ]}
              >
                <TasksVulnerabilities />
              </MockedProvider>
            </Route>
          </MockedProvider>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    await userEvent.click(screen.getAllByRole("checkbox")[1]);
    await userEvent.click(screen.getAllByRole("checkbox")[2]);

    await waitFor((): void => {
      expect(screen.getAllByRole("checkbox")[2]).toBeChecked();
    });

    await userEvent.click(
      screen.getByText("searchFindings.tabVuln.buttons.edit")
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabDescription.editVuln")
      ).toBeInTheDocument();
    });

    expect(screen.getByRole("combobox", { name: "treatment" })).toHaveValue(
      "ACCEPTED"
    );

    await userEvent.click(screen.getByText("group.findings.report.modalClose"));

    await waitFor((): void => {
      expect(screen.getByRole("combobox", { name: "treatment" })).toHaveValue(
        "IN_PROGRESS"
      );
    });

    await userEvent.click(screen.getByText("group.findings.report.modalClose"));

    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabDescription.editVuln")
      ).not.toBeInTheDocument();
    });
  });
});
