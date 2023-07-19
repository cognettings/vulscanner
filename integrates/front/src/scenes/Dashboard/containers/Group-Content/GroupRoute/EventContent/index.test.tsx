import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_ORG_EVENTS } from "scenes/Dashboard/components/EventBar/queries";
import { EventContent } from "scenes/Dashboard/containers/Group-Content/GroupRoute/EventContent";
import { GET_EVENT_DESCRIPTION } from "scenes/Dashboard/containers/Group-Content/GroupRoute/EventContent/EventDescriptionView/queries";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/Group-Content/GroupRoute/EventContent/queries";
import { getCache } from "utils/apollo";
import { msgError } from "utils/notifications";

jest.mock(
  "../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();

    return mockedNotifications;
  }
);

describe("EventContent", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_EVENT_HEADER,
        variables: { eventId: "413372600", groupName: "TEST" },
      },
      result: {
        data: {
          event: {
            __typename: "Event",
            eventDate: "2019-12-09 12:00",
            eventStatus: "SOLVED",
            eventType: "OTHER",
            id: "413372600",
          },
        },
      },
    },
    {
      request: {
        query: GET_EVENT_DESCRIPTION,
        variables: {
          canRetrieveHacker: false,
          eventId: "413372600",
          groupName: "TEST",
        },
      },
      result: {
        data: {
          event: {
            __typename: "Event",
            affectedReattacks: [],
            client: "Test",
            closingDate: "2019-12-26 13:37:00",
            detail: "Something happened",
            eventStatus: "SOLVED",
            eventType: "OTHER",
            hacker: "unittest@fluidattacks.com",
            id: "413372600",
            otherSolvingReason: null,
            solvingReason: null,
          },
        },
      },
    },
    {
      request: {
        query: GET_ORG_EVENTS,
        variables: {
          organizationName: "okada",
        },
      },
      result: {
        data: {
          organizationId: {
            __typename: "Organization",
            groups: [
              {
                __typename: "Group",
                events: [],
                name: "TEST",
              },
            ],
            name: "okada",
          },
        },
      },
    },
  ];
  const mocksError: MockedResponse[] = [
    {
      request: {
        query: GET_EVENT_HEADER,
        variables: { eventId: "413372600", groupName: "TEST" },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof EventContent).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <MemoryRouter
        initialEntries={[
          "/orgs/okada/groups/TEST/events/413372600/description",
        ]}
      >
        <MockedProvider cache={getCache()} mocks={mocks}>
          <Route
            component={EventContent}
            path={
              "/orgs/:organizationName/groups/:groupName/events/:eventId/description"
            }
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByText("group.events.type.other")).toBeInTheDocument();
    });
    await waitFor((): void => {
      expect(screen.queryByText("Something happened")).toBeInTheDocument();
    });
  });

  it("should render error in component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const { container } = render(
      <MemoryRouter
        initialEntries={[
          "/orgs/okada/groups/TEST/events/413372600/description",
        ]}
      >
        <MockedProvider cache={getCache()} mocks={mocksError}>
          <Route
            component={EventContent}
            path={"/orgs/:organizationName/groups/:groupName/events/:eventId"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });
    await waitFor(
      (): void => {
        expect(container.textContent).toBe("");
      },
      { timeout: 5000 }
    );
  });

  it("should render header component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <MemoryRouter
        initialEntries={[
          "/orgs/okada/groups/TEST/events/413372600/description",
        ]}
      >
        <MockedProvider cache={getCache()} mocks={mocks}>
          <Route
            component={EventContent}
            path={
              "/orgs/:organizationName/groups/:groupName/events/:eventId/description"
            }
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabEvents.statusValues.solve")
      ).toBeInTheDocument();
    });

    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabEvents.client")
      ).toBeInTheDocument();
    });
  });

  it("should not display consulting in tab", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <MemoryRouter
        initialEntries={[
          "/orgs/okada/groups/TEST/events/413372600/description",
        ]}
      >
        <MockedProvider mocks={mocks}>
          <Route
            component={EventContent}
            path={
              "/orgs/:organizationName/groups/:groupName/events/:eventId/description"
            }
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("group.tabs.comments.text")
      ).not.toBeInTheDocument();
    });
  });
});
