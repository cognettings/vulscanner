/* eslint-disable camelcase */

import { argv } from "node:process";

import { danger, fail } from "danger";

interface IDangerConfig {
  tests: string[];
}

interface IGitlabPipeline {
  status: string;
  web_url: string;
}

async function branchEqualsToUsername(): Promise<void> {
  const branch = danger.gitlab.mr.source_branch;
  const { username } = danger.gitlab.mr.author;

  if (branch !== username) {
    fail(
      [
        "Branch must be equal to Username\n",
        `Branch: ${branch}`,
        `Username: ${username}`,
      ].join("\n")
    );
  }

  return Promise.resolve();
}

async function mrMessageEqualsCommitMessage(): Promise<void> {
  const mrTitle = `${danger.gitlab.mr.title}\n`;
  const mrBody = `${danger.gitlab.mr.description}\n`;
  const mrMessage = mrBody === "\n" ? mrTitle : `${mrTitle}\n${mrBody}`;
  const commitMessage = danger.git.commits[0].message;

  if (mrMessage !== commitMessage) {
    fail(
      [
        "MR message must be equal to Commit message\n",
        "MR message:",
        `${mrMessage}\n`,
        "Commit message:",
        `${commitMessage}`,
      ].join("\n")
    );
  }

  return Promise.resolve();
}

async function getFirstPipeline(): Promise<IGitlabPipeline> {
  const pipelines = (await danger.gitlab.api.MergeRequests.pipelines(
    danger.gitlab.mr.project_id,
    danger.gitlab.mr.iid
  )) as IGitlabPipeline[];

  return pipelines.at(-1) ?? { status: "", web_url: "Pipeline not found?" };
}

async function firstPipelineSuccessful(): Promise<void> {
  const firstPipeline = await getFirstPipeline();

  if (firstPipeline.status !== "success") {
    fail(
      [
        "First MR pipeline must be successful\n",
        "First pipeline:",
        `${firstPipeline.web_url}`,
      ].join("\n")
    );
  }
}

async function mrAuthorSyntax(): Promise<void> {
  const re = /^[A-Z][a-z]+ [A-Z][a-z]+$/u;
  const author = danger.gitlab.mr.author.name;

  if (!re.test(author)) {
    fail(
      [
        `Your GitLab user name is ${author}.`,
        "Please make sure to use the following syntax:\n",
        "Capitalized name, space and capitalized last name.",
        "(avoid accents and ñ).",
        "For example: Aureliano Buendia.\n",
        "You can change your GitLab user name here:",
        "https://gitlab.com/-/profile",
      ].join("\n")
    );
  }

  return Promise.resolve();
}

async function main(): Promise<void> {
  const functions = new Map<string, () => Promise<void>>([
    ["branchEqualsToUsername", branchEqualsToUsername],
    ["mrMessageEqualsCommitMessage", mrMessageEqualsCommitMessage],
    ["firstPipelineSuccessful", firstPipelineSuccessful],
    ["mrAuthorSyntax", mrAuthorSyntax],
  ]);
  const config: IDangerConfig = JSON.parse(argv.at(-1) ?? '{ "tests": [] }');

  const toTest = config.tests.map((testName): (() => Promise<void>) => {
    return functions.get(testName) ?? Promise.resolve;
  });

  await Promise.all(
    toTest.map(async (testName): Promise<void> => {
      return testName();
    })
  );
}

void main();
