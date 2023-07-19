import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { TreatmentTracking } from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/index";
import { GET_VULN_TREATMENT } from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/queries";
import type { IGetVulnTreatmentAttr } from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/types";
import { formatDropdownField } from "utils/formatHelpers";

describe("TrackingTreatment", (): void => {
  const vulnId: string = "af7a48b8-d8fc-41da-9282-d424fff563f0";

  const mockQueryVulnTreatment1: MockedResponse<IGetVulnTreatmentAttr> = {
    request: {
      query: GET_VULN_TREATMENT,
      variables: {
        vulnId,
      },
    },
    result: {
      data: {
        vulnerability: {
          __typename: "Vulnerability",
          historicTreatmentConnection: {
            edges: [
              {
                node: {
                  acceptanceDate: "",
                  acceptanceStatus: "",
                  assigned: "",
                  date: "2019-01-17 10:06:04",
                  justification: "",
                  treatment: "UNTREATED",
                  user: "",
                },
              },
              {
                node: {
                  acceptanceDate: "",
                  acceptanceStatus: "SUBMITTED",
                  assigned: "usermanager1@test.test",
                  date: "2020-02-17 18:36:24",
                  justification: "Some of the resources",
                  treatment: "ACCEPTED_UNDEFINED",
                  user: "usertreatment1@test.test",
                },
              },
              {
                node: {
                  acceptanceDate: "",
                  acceptanceStatus: "APPROVED",
                  assigned: "usermanager2@test.test",
                  date: "2020-02-18 18:36:24",
                  justification: "The headers must be",
                  treatment: "ACCEPTED_UNDEFINED",
                  user: "usertreatment2@test.test",
                },
              },
              {
                node: {
                  acceptanceDate: "2020-10-09 15:29:48",
                  acceptanceStatus: "",
                  assigned: "usermanager3@test.test",
                  date: "2020-10-02 15:29:48",
                  justification: "The headers must be",
                  treatment: "ACCEPTED",
                  user: "usertreatment3@test.test",
                },
              },
              {
                node: {
                  acceptanceDate: "",
                  acceptanceStatus: "",
                  assigned: "usermanager4@test.test",
                  date: "2020-10-08 15:29:48",
                  justification: "The headers must be",
                  treatment: "IN_PROGRESS",
                  user: "usertreatment4@test.test",
                },
              },
            ],
            pageInfo: {
              endCursor: "",
              hasNextPage: false,
            },
          },
          id: "af7a48b8-d8fc-41da-9282-d424fff563f0",
        },
      },
    },
  };

  const rejectedObservation: string = "The treatment was rejected";
  const mockQueryVulnTreatment2: MockedResponse<IGetVulnTreatmentAttr> = {
    request: {
      query: GET_VULN_TREATMENT,
      variables: {
        vulnId,
      },
    },
    result: {
      data: {
        vulnerability: {
          __typename: "Vulnerability",
          historicTreatmentConnection: {
            edges: [
              {
                node: {
                  acceptanceDate: "",
                  acceptanceStatus: "",
                  assigned: "",
                  date: "2019-01-17 10:06:04",
                  justification: "",
                  treatment: "UNTREATED",
                  user: "",
                },
              },
              {
                node: {
                  acceptanceDate: "",
                  acceptanceStatus: "SUBMITTED",
                  assigned: "usermanager1@test.test",
                  date: "2020-02-17 18:36:24",
                  justification: "Some of the resources",
                  treatment: "ACCEPTED_UNDEFINED",
                  user: "usertreatment1@test.test",
                },
              },
              {
                node: {
                  acceptanceDate: "",
                  acceptanceStatus: "REJECTED",
                  assigned: "usermanager2@test.test",
                  date: "2020-02-18 18:36:24",
                  justification: rejectedObservation,
                  treatment: "ACCEPTED_UNDEFINED",
                  user: "usertreatment2@test.test",
                },
              },
              {
                node: {
                  acceptanceDate: "",
                  acceptanceStatus: "",
                  assigned: "",
                  date: "2020-02-18 18:36:25",
                  justification: "",
                  treatment: "UNTREATED",
                  user: "",
                },
              },
            ],
            pageInfo: {
              endCursor: "",
              hasNextPage: false,
            },
          },
          id: "af7a48b8-d8fc-41da-9282-d424fff563f0",
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof TreatmentTracking).toBe("function");
  });

  it("should render in treatment tracking 1", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/locations"]}>
        <MockedProvider addTypename={false} mocks={[mockQueryVulnTreatment1]}>
          <TreatmentTracking vulnId={vulnId} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.getByText("searchFindings.tabDescription.treatment.inProgress")
      ).toBeInTheDocument();
    });
  });

  it("should render in treatment tracking 2", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/locations"]}>
        <MockedProvider addTypename={false} mocks={[mockQueryVulnTreatment2]}>
          <TreatmentTracking vulnId={vulnId} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryAllByText("searchFindings.tabDescription.treatment.new")
      ).toHaveLength(2);
    });

    expect(
      screen.getByText(
        `${formatDropdownField(
          "ACCEPTED_UNDEFINED"
        )}searchFindings.tabDescription.treatment.pendingApproval`
      )
    ).toBeInTheDocument();

    expect(
      screen.getByText(
        new RegExp(
          `${"searchFindings.tabTracking.justification"} ${rejectedObservation}`,
          "u"
        )
      )
    ).toBeInTheDocument();
  });
});
