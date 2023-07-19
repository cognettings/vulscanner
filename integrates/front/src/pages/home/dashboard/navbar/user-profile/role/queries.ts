import { gql } from "@apollo/client";

interface IUserRole {
  group?: { name: string; userRole: string };
  me?: { role: string; userEmail: string };
  organizationId?: { name: string; userRole: string };
}

const GET_USER_ROLE = gql`
  query GetUserRole(
    $groupLevel: Boolean!
    $groupName: String!
    $organizationLevel: Boolean!
    $organizationName: String!
    $userLevel: Boolean!
  ) {
    group(groupName: $groupName) @include(if: $groupLevel) {
      name
      userRole
    }
    me @include(if: $userLevel) {
      role
      userEmail
    }
    organizationId(organizationName: $organizationName)
      @include(if: $organizationLevel) {
      name
      userRole
    }
  }
`;

export type { IUserRole };
export { GET_USER_ROLE };
