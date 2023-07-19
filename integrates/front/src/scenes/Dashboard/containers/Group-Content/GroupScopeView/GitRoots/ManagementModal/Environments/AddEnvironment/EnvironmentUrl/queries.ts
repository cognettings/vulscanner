import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FILES: DocumentNode = gql`
  query GetFilesQuery($groupName: String!) {
    resources(groupName: $groupName) {
      files {
        description
        fileName
        uploadDate
        uploader
      }
    }
  }
`;

export { GET_FILES };
