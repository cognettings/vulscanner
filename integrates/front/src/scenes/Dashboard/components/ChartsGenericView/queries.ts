import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_VULNERABILITIES_URL: DocumentNode = gql`
  query GetOrgVulnerabilitiesUrl(
    $identifier: String!
    $verificationCode: String
  ) {
    organization(organizationId: $identifier) {
      name
      vulnerabilitiesUrl(verificationCode: $verificationCode)
    }
  }
`;

export { GET_VULNERABILITIES_URL };
