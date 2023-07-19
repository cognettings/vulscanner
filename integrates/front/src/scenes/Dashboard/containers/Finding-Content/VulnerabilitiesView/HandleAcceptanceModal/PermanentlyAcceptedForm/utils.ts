import _ from "lodash";

import type { NotificationResult } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/types";
import type { IVulnDataAttr } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal/types";

const getAllNotifications = async (
  sendNotification: (
    variables: Record<string, unknown>
  ) => Promise<NotificationResult>,
  vulnerabilities: IVulnDataAttr[]
): Promise<NotificationResult[]> => {
  const vulnerabilitiesByFinding = _.groupBy(
    vulnerabilities,
    (vuln: IVulnDataAttr): string => vuln.findingId
  );
  const requestedChunks = Object.entries(vulnerabilitiesByFinding).map(
    ([findingId, chunkedVulnerabilities]: [
        string,
        IVulnDataAttr[]
      ]): (() => Promise<NotificationResult[]>) =>
      async (): Promise<NotificationResult[]> => {
        return Promise.all([
          await sendNotification({
            variables: {
              findingId,
              vulnerabilities: chunkedVulnerabilities.map(
                ({ id }): string => id
              ),
            },
          }),
        ]);
      }
  );

  return requestedChunks.reduce(
    async (previousValue, currentValue): Promise<NotificationResult[]> => [
      ...(await previousValue),
      ...(await currentValue()),
    ],
    Promise.resolve<NotificationResult[]>([])
  );
};

export { getAllNotifications };
