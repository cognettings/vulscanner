import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { NotificationsView } from "scenes/Dashboard/containers/NotificationsView";
import {
  GET_SUBSCRIPTIONS,
  UPDATE_NOTIFICATIONS_PREFERENCES,
} from "scenes/Dashboard/containers/NotificationsView/queries";

describe("notification matrix shows active and inactive subscriptions", (): void => {
  const mocks: MockedResponse[] = [
    {
      request: {
        query: GET_SUBSCRIPTIONS,
      },
      result: {
        data: {
          Notifications: {
            enumValues: [
              {
                name: "ACCESS_GRANTED",
              },
              {
                name: "AGENT_TOKEN",
              },
              {
                name: "EVENT_REPORT",
              },
              {
                name: "FILE_UPDATE",
              },
              {
                name: "GROUP_INFORMATION",
              },
              {
                name: "GROUP_REPORT",
              },
              {
                name: "NEW_COMMENT",
              },
              {
                name: "NEW_DRAFT",
              },
              {
                name: "PORTFOLIO_UPDATE",
              },
              {
                name: "REMEDIATE_FINDING",
              },
              {
                name: "REMINDER_NOTIFICATION",
              },
              {
                name: "ROOT_UPDATE",
              },
              {
                name: "SERVICE_UPDATE",
              },
              {
                name: "UNSUBSCRIPTION_ALERT",
              },
              {
                name: "UPDATED_TREATMENT",
              },
              {
                name: "VULNERABILITY_ASSIGNED",
              },
              {
                name: "VULNERABILITY_REPORT",
              },
            ],
          },
          me: {
            notificationsPreferences: {
              email: [
                "NEW_COMMENT",
                "SERVICE_UPDATE",
                "ROOT_UPDATE",
                "UPDATED_TREATMENT",
                "VULNERABILITY_REPORT",
              ],
              parameters: {
                minSeverity: 3,
              },
              sms: ["VULNERABILITY_ASSIGNED"],
            },
            userEmail: "unitesting@fluidattacks.com",
          },
        },
      },
    },
    {
      request: {
        query: UPDATE_NOTIFICATIONS_PREFERENCES,
        variables: {
          email: [],
          severity: 2.0,
          sms: [],
        },
      },
      result: {
        data: {
          updateNotificationsPreferences: { success: true },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof NotificationsView).toBe("function");
  });

  it("should render notification matrix showing active and inactive subscriptions", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/user/config"]}>
        <MockedProvider addTypename={true} mocks={mocks}>
          <Route component={NotificationsView} path={"/user/config"} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("DevSecOps agent token alert")
      ).toBeInTheDocument();
    });

    await waitFor((): void => {
      const checkedCheckboxes = screen.getAllByRole("checkbox", {
        checked: true,
      });

      expect(checkedCheckboxes).toHaveLength(6);
    });

    await waitFor((): void => {
      expect(screen.queryByText("Minimum severity")).toBeInTheDocument();
    });

    await waitFor((): void => {
      expect(screen.getAllByText("Email")).toHaveLength(15);
    });
  });
});
