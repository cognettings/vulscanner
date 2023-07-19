import { readFileSync } from "fs";

import { getFutureMatches } from "@datasert/cronjs-matcher";
import { Batch } from "@aws-sdk/client-batch";
import {
  App,
  TerraformStack,
  TerraformVariable,
  Token,
  S3Backend,
  TerraformOutput,
  DataTerraformRemoteStateS3,
} from "cdktf";
import type { Construct } from "constructs";

import { BetteruptimeHeartbeat } from "./.gen/providers/better-uptime/betteruptime-heartbeat";
import { BetteruptimeHeartbeatGroup } from "./.gen/providers/better-uptime/betteruptime-heartbeat-group";
import { BetterUptimeProvider } from "./.gen/providers/better-uptime/provider";
import { BetteruptimeStatusPageResource } from "./.gen/providers/better-uptime/betteruptime-status-page-resource";
import { BetteruptimeStatusPageSection } from "./.gen/providers/better-uptime/betteruptime-status-page-section";

function intervalExecution(cronExpression: string): number {
  const currentDate = new Date();
  const currentUtcDate = new Date(
    currentDate.getUTCFullYear(),
    currentDate.getUTCMonth(),
    currentDate.getUTCDate(),
    currentDate.getUTCHours(),
    currentDate.getUTCMinutes(),
    currentDate.getUTCSeconds()
  );

  const utcDateStart = new Date(
    Date.UTC(
      currentDate.getUTCFullYear(),
      currentDate.getUTCMonth(),
      currentDate.getUTCDate(),
      0,
      0,
      0
    )
  );
  utcDateStart.setDate(utcDateStart.getDate() - 1);

  const futures = getFutureMatches(cronExpression, {
    hasSeconds: false,
    startAt: utcDateStart.toISOString(),
    timezone: "Etc/UTC",
    maxLoopCount: 200,
    matchCount: 48,
  });

  for (let index = 0; index < futures.length; index++) {
    const currentFuture = new Date(futures[index]);
    if (index > 0 && currentFuture.getTime() > currentUtcDate.getTime()) {
      const prevFuture = new Date(futures[index - 1]);
      return Math.abs(currentFuture.getTime() - prevFuture.getTime()) / 1000;
    }
  }

  return 84600;
}

const getAverageDuration = async (jobName: string, jobQueueName: string) => {
  const batch = new Batch({ region: "us-east-1" });

  try {
    // Get the list of jobs in the job queue
    const jobs = await batch.listJobs({
      jobQueue: jobQueueName,
      filters: [{ name: "JOB_NAME", values: [jobName] }],
    });
    if (!jobs.jobSummaryList) {
      return;
    }
    // Filter jobs by name and status
    const filteredJobs = jobs.jobSummaryList.filter(
      (job) => job.status === "SUCCEEDED"
    );

    if (filteredJobs.length === 0) {
      return null;
    }

    // Get the duration of each job and calculate the total sum
    const totalDuration = filteredJobs.reduce((accumulator, job) => {
      const durationInSeconds = (job.stoppedAt! - job.startedAt!) / 1000;
      return accumulator + durationInSeconds;
    }, 0);

    // Calculate the average duration
    const averageDuration = totalDuration / filteredJobs.length;

    return Math.floor(averageDuration);
  } catch (error) {
    console.error("Error while getting the average duration:", error);
  }
  return null;
};

class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);
  }
}

async function createStack(stack: TerraformStack) {
  new S3Backend(stack, {
    bucket: "fluidattacks-terraform-states-prod",
    key: "schedules-status.tfstate",
    region: "us-east-1",
    encrypt: true,
    dynamodbTable: "terraform_state_lock",
  });

  const remoteState = new DataTerraformRemoteStateS3(
    stack,
    "remote_state_status",
    {
      bucket: "fluidattacks-terraform-states-prod",
      key: "makes-status.tfstate",
      region: "us-east-1",
      encrypt: true,
      dynamodbTable: "terraform_state_lock",
    }
  );

  const betteruptimeProvider = new BetterUptimeProvider(stack, "betteruptime", {
    apiToken: new TerraformVariable(stack, "betterUptimeApiToken", {
      type: "string",
      description: "Betteruptime API Token",
    }).toString(),
    alias: "betteruptime",
  });

  const data = process.env.DATA;
  if (data === undefined) {
    return;
  }

  let section = new BetteruptimeStatusPageSection(stack, "schedules", {
    name: "Schedules",
    provider: betteruptimeProvider,
    statusPageId: remoteState.getString(
      "betteruptime_status_page_id_fluidattacks"
    ),
  });

  const schedules_group = new BetteruptimeHeartbeatGroup(
    stack,
    "heartbeat-group-schedules",
    { provider: betteruptimeProvider, name: "schedules" }
  );

  const schedules_data = JSON.parse(readFileSync(data, "utf-8"));
  const entries = Object.entries(schedules_data);

  for (let index = 0; index < entries.length; index++) {
    const [key, value] = entries[index];

    // @ts-expect-error
    let cron_expression: string = value.scheduleExpression.replace(
      /^cron\(|\)$/g,
      ""
    );
    // @ts-expect-error
    let averageDuration = (await getAverageDuration(key, value.size)) || 0;
    const currentHeartbeat = new BetteruptimeHeartbeat(stack, key, {
      // extend the grace period by 30% of the average duration
      grace: Math.floor(averageDuration + averageDuration * 0.3) || 1800,
      name: key,
      period: intervalExecution(cron_expression),
      provider: betteruptimeProvider,
      heartbeatGroupId: Token.asNumber(schedules_group.id),
      // @ts-expect-error
      paused: !value.enable,
    });

    // @ts-expect-error
    if (value.statusPage) {
      new BetteruptimeStatusPageResource(stack, `status-resource-${key}`, {
        statusPageSectionId: Token.asNumber(section.id),
        // @ts-expect-error
        publicName: value.resourceName ?? key,
        statusPageId: remoteState.getString(
          "betteruptime_status_page_id_fluidattacks"
        ),
        resourceType: "Heartbeat",
        resourceId: Token.asNumber(currentHeartbeat.id),
        provider: betteruptimeProvider,
        history: true,
      });
    }

    new TerraformOutput(stack, `heartbeat-url-${key}`, {
      value: currentHeartbeat.url,
    });
  }
}

const app = new App();
const infra = new MyStack(app, "schedules");
createStack(infra).then(() => {
  app.synth();
});
