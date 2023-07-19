import type { ApolloError } from "@apollo/client";

import {
  GET_GIT_ROOT,
  GET_GIT_ROOTS,
  GET_GIT_ROOTS_SIMPLE,
  GET_VULNERABILITIES,
  UPDATE_TOE_LINES_ATTACKED,
} from "../queries";
import type {
  IGetGitRoot,
  IGetGitRoots,
  IGetVulnerabilities,
  IUpdateAttackedFile,
} from "@retrieves/api/types";
import type { IAttackedFile, IGitRoot, IVulnerability } from "@retrieves/types";
import { API_CLIENT, handleGraphQlError } from "@retrieves/utils/apollo";
import { Logger } from "@retrieves/utils/logging";

const getGroupGitRoots = async (groupName: string): Promise<IGitRoot[]> => {
  const result: IGetGitRoots = await API_CLIENT.query({
    query: GET_GIT_ROOTS,
    variables: { groupName },
  }).catch(async (error): Promise<IGetGitRoots> => {
    await handleGraphQlError(error);
    Logger.error(`Failed to get GitRoots from ${groupName}:`, error);

    return { data: { group: { roots: [] } } };
  });

  return result.data.group.roots.map((root): IGitRoot => {
    return { ...root, groupName };
  });
};

const getGroupGitRootsSimple = async (
  groupName: string
): Promise<IGitRoot[]> => {
  const result: IGetGitRoots = await API_CLIENT.query({
    query: GET_GIT_ROOTS_SIMPLE,
    variables: { groupName },
  }).catch(async (error): Promise<IGetGitRoots> => {
    await handleGraphQlError(error);
    Logger.error(`Failed to get GitRoots from ${groupName}:`, error);

    return { data: { group: { roots: [] } } };
  });

  return result.data.group.roots.map((root): IGitRoot => {
    return { ...root, groupName };
  });
};

const getGitRootVulnerabilities = async (
  groupName: string,
  rootId: string
): Promise<IVulnerability[]> => {
  const result: IGetVulnerabilities = await API_CLIENT.query({
    query: GET_VULNERABILITIES,
    variables: { groupName, rootId },
  }).catch(async (error): Promise<IGetVulnerabilities> => {
    await handleGraphQlError(error);
    Logger.error(
      `Failed to get GitRoot vulnerabilities from a root in ${groupName}:`,
      error
    );

    return { data: { root: { vulnerabilities: [] } } };
  });

  return result.data.root.vulnerabilities;
};

const getGitRoot = async (
  groupName: string,
  rootId: string
): Promise<IGitRoot> => {
  const result: IGetGitRoot = await API_CLIENT.query({
    query: GET_GIT_ROOT,
    variables: { groupName, rootId },
  }).catch(async (error): Promise<IGetGitRoot> => {
    await handleGraphQlError(error);
    Logger.error(`Failed to get a GitRoot from ${groupName}:`, error);

    return { data: { root: {} as IGitRoot } };
  });

  return result.data.root;
};

const markFileAsAttacked = async (
  groupName: string,
  rootId: string,
  fileName: string,
  comments?: string
): Promise<IAttackedFile> => {
  const result: {
    updateToeLinesAttackedLines: { success: boolean; message?: string };
  } = (
    await API_CLIENT.mutate({
      mutation: UPDATE_TOE_LINES_ATTACKED,
      variables: {
        comments,
        fileName,
        groupName,
        rootId,
      },
    }).catch(async (error: ApolloError): Promise<IUpdateAttackedFile> => {
      await handleGraphQlError(error);
      Logger.error(`Failed to mark file ${fileName}:`, error);

      return {
        data: {
          updateToeLinesAttackedLines: {
            message: error.message,
            success: false,
          },
        },
      };
    })
  ).data;

  return result.updateToeLinesAttackedLines;
};

export {
  getGitRootVulnerabilities,
  getGroupGitRoots,
  getGitRoot,
  getGroupGitRootsSimple,
  markFileAsAttacked,
};
