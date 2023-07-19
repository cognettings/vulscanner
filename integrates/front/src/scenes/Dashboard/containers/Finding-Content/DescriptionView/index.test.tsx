/* eslint-disable camelcase */
import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { FetchMockStatic } from "fetch-mock";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import { DescriptionView } from "scenes/Dashboard/containers/Finding-Content/DescriptionView";
import {
  GET_FINDING_DESCRIPTION,
  GET_LANGUAGE,
} from "scenes/Dashboard/containers/Finding-Content/DescriptionView/queries";
import type {
  IFinding,
  IFindingDescriptionData,
  IFindingDescriptionVars,
  ILanguageData,
} from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";

const mockedFetch: FetchMockStatic = fetch as FetchMockStatic & typeof fetch;
const baseUrl: string =
  "https://gitlab.com/api/v4/projects/20741933/repository/files";
const branchRef: string = "trunk";
const vulnsFileId: string =
  "common%2Fcriteria%2Fsrc%2Fvulnerabilities%2Fdata.yaml";
mockedFetch.mock(`${baseUrl}/${vulnsFileId}/raw?ref=${branchRef}`, {
  body: {
    "004": {
      en: {
        description: "",
        impact: "",
        recommendation: "",
        threat: "",
        title: "Remote command execution",
      },
      requirements: [],
      score: {
        base: {
          attack_complexity: "",
          attack_vector: "",
          availability: "",
          confidentiality: "",
          integrity: "",
          privileges_required: "",
          scope: "",
          user_interaction: "",
        },
        temporal: {
          exploit_code_maturity: "",
          remediation_level: "",
          report_confidence: "",
        },
      },
    },
  },

  status: 200,
});
const requirementsFileId: string =
  "common%2Fcriteria%2Fsrc%2Frequirements%2Fdata.yaml";
mockedFetch.mock(`${baseUrl}/${requirementsFileId}/raw?ref=${branchRef}`, {
  body: {
    "029": {
      category: "",
      en: {
        description: "",
        summary: `
          The session cookies
          of web applications must have
          security attributes
          (HttpOnly, Secure, SameSite)
          and prefixes (e.g., __Host-).
        `,
        title: "Cookies with security attributes",
      },
      references: [],
    },
    "173": {
      category: "",
      en: {
        description: "",
        summary: `
          The system must discard
          all potentially harmful information
          received via data inputs.
        `,
        title: "Discard unsafe inputs",
      },
      references: [],
    },
  },

  status: 200,
});

describe("Finding Description", (): void => {
  const finding: IFinding = {
    attackVectorDescription: "Run a reverse shell",
    description: "It's possible to execute shell commands from the site",
    id: "413372600",
    openVulnerabilities: 0,
    recommendation: "Use good security practices and standards".repeat(13),
    releaseDate: null,
    sorts: "No",
    status: "VULNERABLE",
    threat: "External attack",
    title: "004. Remote command execution",
    unfulfilledRequirements: [
      {
        id: "0265",
        summary: "Requirement summary",
      },
    ],
  };
  const language: ILanguageData = {
    group: {
      language: "EN",
    },
  };
  const groupName = "TEST";
  const findingDescriptionData: IFindingDescriptionData = {
    finding,
  };
  const findingDescriptionVars: IFindingDescriptionVars = {
    canRetrieveHacker: false,
    canRetrieveSorts: false,
    findingId: "413372600",
  };
  const descriptionQuery: Readonly<MockedResponse> = {
    request: {
      query: GET_FINDING_DESCRIPTION,
      variables: findingDescriptionVars,
    },
    result: {
      data: findingDescriptionData,
    },
  };
  const languageQuery: Readonly<MockedResponse> = {
    request: {
      query: GET_LANGUAGE,
      variables: { groupName },
    },
    result: {
      data: language,
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof DescriptionView).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/description"]}>
        <MockedProvider
          addTypename={false}
          mocks={[languageQuery, descriptionQuery]}
        >
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <Route
              component={DescriptionView}
              path={"/:groupName/vulns/:findingId/description"}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByText("Run a reverse shell")).toBeInTheDocument();
    });
    jest.clearAllMocks();
  });

  it("should set the description as editable", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_finding_description_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/description"]}>
        <MockedProvider
          addTypename={false}
          mocks={[languageQuery, descriptionQuery]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider
              value={
                new PureAbility([{ action: "can_report_vulnerabilities" }])
              }
            >
              <Route
                component={DescriptionView}
                path={"/:groupName/vulns/:findingId/description"}
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const EXPECTED_LENGTH: number = 4;
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabDescription.editable.text")
      ).toBeInTheDocument();
    });

    expect(screen.queryAllByRole("textbox")).toHaveLength(0);

    await userEvent.click(
      screen.getByText("searchFindings.tabDescription.editable.text")
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("textbox")).toHaveLength(EXPECTED_LENGTH);
    });

    await userEvent.type(
      screen.getByRole("textbox", { name: "description" }),
      ". Edit field"
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("textbox", { name: "description" })
      ).toHaveFocus();
    });

    expect(
      screen.getByRole("textbox", { name: "recommendation" })
    ).not.toHaveFocus();

    await userEvent.click(
      screen.getByText("searchFindings.tabDescription.save.text")
    );

    await waitFor((): void => {
      expect(
        screen.getByText("Type 499 characters or less")
      ).toBeInTheDocument();
    });
    await waitFor((): void => {
      expect(
        screen.getByRole("textbox", { name: "recommendation" })
      ).toHaveFocus();
    });

    await userEvent.click(
      screen.getByText("searchFindings.tabDescription.editable.cancel")
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("textbox")).toHaveLength(0);
    });
    jest.clearAllMocks();
  });
});
