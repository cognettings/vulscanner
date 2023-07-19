import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useContext, useMemo } from "react";
import { useParams } from "react-router-dom";

import { handleAddCommentErrorHelper } from "./helpers";

import type { IAuthContext } from "context/auth";
import { authContext } from "context/auth";
import { Comments } from "scenes/Dashboard/components/Comments";
import type {
  ICommentStructure,
  ILoadCallback,
  IPostCallback,
} from "scenes/Dashboard/components/Comments/types";
import {
  ADD_FINDING_CONSULT,
  GET_FINDING_CONSULTING,
  GET_FINDING_OBSERVATIONS,
} from "scenes/Dashboard/containers/Finding-Content/CommentsView/queries";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface ICommentsData {
  finding: {
    consulting: ICommentStructure[];
    observations: ICommentStructure[];
  };
}

const CommentsView: React.FC = (): JSX.Element => {
  const params: { findingId: string; type: string } = useParams();
  const { findingId } = params;
  const PARAM_NO_OBSERVATIONS: number = -3;
  const type: string =
    params.type === "observations"
      ? params.type.slice(0, -1)
      : params.type.slice(0, PARAM_NO_OBSERVATIONS);

  const { userEmail }: IAuthContext = useContext(authContext);
  const isObservation = useMemo(
    (): boolean => params.type === "observations",
    [params.type]
  );

  const handleErrors: (error: ApolloError) => void = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(`An error occurred loading finding ${type}`, error);
      });
    },
    [type]
  );

  const handleAddCommentError: (addCommentError: ApolloError) => void =
    useCallback(
      (addCommentError: ApolloError): void => {
        handleAddCommentErrorHelper(addCommentError, type);
      },
      [type]
    );

  const { data, loading } = useQuery<ICommentsData>(
    type === "consult" ? GET_FINDING_CONSULTING : GET_FINDING_OBSERVATIONS,
    {
      onError: handleErrors,
      variables: { findingId },
    }
  );

  const getData: (callback: ILoadCallback) => void = useCallback(
    (callbackFn: (cData: ICommentStructure[]) => void): void => {
      if (!_.isUndefined(data)) {
        const comments: ICommentStructure[] =
          type === "consult"
            ? data.finding.consulting
            : data.finding.observations;
        callbackFn(
          comments.map(
            (comment: ICommentStructure): ICommentStructure => ({
              ...comment,
              createdByCurrentUser: comment.email === userEmail,
              id: Number(comment.id),
              parentComment: Number(comment.parentComment),
            })
          )
        );
      }
    },
    [data, type, userEmail]
  );

  const [addComment] = useMutation(ADD_FINDING_CONSULT, {
    onError: handleAddCommentError,
  });

  const handlePost = useCallback(
    async (
      comment: ICommentStructure,
      callbackFn: IPostCallback
    ): Promise<void> => {
      interface IMutationResult {
        data: {
          addFindingConsult: {
            commentId: string;
            success: boolean;
          };
        };
      }
      mixpanel.track(`Add${_.capitalize(type)}`, { findingId });
      await addComment({
        variables: {
          content: comment.content,
          findingId,
          parentComment: comment.parentComment,
          type: type.toUpperCase(),
        },
        // Can also have the null type but unknown overrides it
      }).then((mtResult: unknown): void => {
        const result: IMutationResult["data"] = (mtResult as IMutationResult)
          .data;
        if (result.addFindingConsult.success) {
          callbackFn({
            ...comment,
            id: Number(result.addFindingConsult.commentId),
          });
        }
      });
    },
    [addComment, findingId, type]
  );

  if (_.isUndefined(data) || loading) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <div data-private={true}>
        <Comments
          isObservation={isObservation}
          onLoad={getData}
          onPostComment={handlePost}
        />
      </div>
    </React.StrictMode>
  );
};

export { CommentsView };
