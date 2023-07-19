import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { authzPermissionsContext } from "context/authz/config";
import { EvidenceView } from "scenes/Dashboard/containers/Finding-Content/EvidenceView";
import {
  GET_FINDING_EVIDENCES,
  REMOVE_EVIDENCE_MUTATION,
} from "scenes/Dashboard/containers/Finding-Content/EvidenceView/queries";

describe("FindingEvidenceView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FINDING_EVIDENCES,
        variables: { findingId: "413372600" },
      },
      result: {
        data: {
          finding: {
            evidence: {
              __typename: "FindingEvidence",
              animation: {
                date: "",
                description: "Test description",
                isDraft: false,
                url: "some_file.png",
              },
              evidence1: { date: "", description: "", isDraft: false, url: "" },
              evidence2: { date: "", description: "", isDraft: false, url: "" },
              evidence3: { date: "", description: "", isDraft: false, url: "" },
              evidence4: { date: "", description: "", isDraft: false, url: "" },
              evidence5: { date: "", description: "", isDraft: false, url: "" },
              exploitation: {
                date: "",
                description: "",
                isDraft: false,
                url: "",
              },
            },
            id: "413372600",
          },
        },
      },
    },
  ];

  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof EvidenceView).toBe("function");
  });

  it("should render empty UI", async (): Promise<void> => {
    expect.hasAssertions();

    const emptyMocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_FINDING_EVIDENCES,
          variables: { findingId: "413372600" },
        },
        result: {
          data: {
            finding: {
              evidence: {
                __typename: "FindingEvidence",
                animation: {
                  date: "",
                  description: "",
                  isDraft: false,
                  url: "",
                },
                evidence1: {
                  date: "",
                  description: "",
                  isDraft: false,
                  url: "",
                },
                evidence2: {
                  date: "",
                  description: "",
                  isDraft: false,
                  url: "",
                },
                evidence3: {
                  date: "",
                  description: "",
                  isDraft: false,
                  url: "",
                },
                evidence4: {
                  date: "",
                  description: "",
                  isDraft: false,
                  url: "",
                },
                evidence5: {
                  date: "",
                  description: "",
                  isDraft: false,
                  url: "",
                },
                exploitation: {
                  date: "",
                  description: "",
                  isDraft: false,
                  url: "",
                },
              },
              id: "413372600",
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider mocks={emptyMocks}>
          <Route
            component={EvidenceView}
            path={"/:groupName/events/:findingId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("group.findings.evidence.noData")
      ).toBeInTheDocument();
    });
    jest.clearAllMocks();
  });

  it("should render remove image", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_evidence_mutate" },
    ]);
    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_EVIDENCE_MUTATION,
          variables: {
            evidenceId: "ANIMATION",
            findingId: "413372600",
          },
        },
        result: {
          data: { removeEvidence: { success: true } },
        },
      },
      {
        request: {
          query: GET_FINDING_EVIDENCES,
          variables: { findingId: "413372600" },
        },
        result: {
          data: {
            finding: {
              evidence: {
                __typename: "FindingEvidence",
                animation: {
                  date: "",
                  description: "",
                  isDraft: false,
                  url: "",
                },
                evidence1: {
                  date: "",
                  description: "",
                  isDraft: false,
                  url: "",
                },
                evidence2: {
                  date: "",
                  description: "",
                  isDraft: false,
                  url: "",
                },
                evidence3: {
                  date: "",
                  description: "",
                  isDraft: false,
                  url: "",
                },
                evidence4: {
                  date: "",
                  description: "",
                  isDraft: false,
                  url: "",
                },
                evidence5: {
                  date: "",
                  description: "",
                  isDraft: false,
                  url: "",
                },
                exploitation: {
                  date: "",
                  description: "",
                  isDraft: false,
                  url: "",
                },
              },
              id: "413372600",
            },
          },
        },
      },
    ];

    render(
      <MemoryRouter
        initialEntries={["orgs/okada/groups/test/vulns/413372600/evidence"]}
      >
        <MockedProvider mocks={[...mocks, ...mocksMutation]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={EvidenceView}
              path={
                "orgs/:organizationName/groups/:groupName/vulns/:findingId/evidence"
              }
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("img")).toHaveLength(1);
    });

    expect(screen.queryAllByRole("textbox")).toHaveLength(0);
    expect(
      screen.queryByText("group.findings.evidence.noData")
    ).not.toBeInTheDocument();

    expect(screen.getAllByRole("img")[0]).toHaveAttribute("alt", "animation");
    expect(
      screen.queryByText("searchFindings.tabEvidence.editable")
    ).toBeInTheDocument();

    await userEvent.click(
      screen.getByText("searchFindings.tabEvidence.editable")
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabEvidence.remove")
      ).toBeInTheDocument();
    });

    expect(screen.queryAllByRole("textbox")).toHaveLength(7);

    await userEvent.click(
      screen.getByText("searchFindings.tabEvidence.remove")
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("group.findings.evidence.noData")
      ).toBeInTheDocument();
    });

    expect(screen.queryAllByRole("img")).toHaveLength(0);

    jest.clearAllMocks();
  });

  it("should render image", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider mocks={mocks}>
          <Route
            component={EvidenceView}
            path={"/:groupName/events/:findingId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("img")).toHaveLength(1);
    });

    expect(screen.getAllByRole("img")[0]).toHaveAttribute("alt", "animation");

    jest.clearAllMocks();
  });

  it("should render image viewer", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider mocks={mocks}>
          <Route
            component={EvidenceView}
            path={"/:groupName/events/:findingId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("Exploitation animation: Test description")
      ).toBeInTheDocument();
    });

    expect(screen.queryAllByRole("span", { hidden: true })).toHaveLength(0);

    await userEvent.click(screen.getAllByRole("img")[0]);
    await userEvent.hover(
      screen.getByRole("dialog", {
        hidden: true,
        name: "ImageViewer",
      })
    );

    const ReactImageViewerButtons: number = 3;
    await waitFor((): void => {
      expect(screen.queryAllByRole("img", { hidden: true })).toHaveLength(
        ReactImageViewerButtons
      );
    });

    jest.clearAllMocks();
  });
});
