import { gql } from "@apollo/client";

interface IStakeholder {
  stakeholder: {
    email: string;
    responsibility: string | null;
  };
}

const GET_STAKEHOLDER = gql`
  query GetStakeholder(
    $entity: StakeholderEntity!
    $organizationId: String
    $groupName: String
    $userEmail: String!
  ) {
    stakeholder(
      entity: $entity
      organizationId: $organizationId
      groupName: $groupName
      userEmail: $userEmail
    ) {
      email
      responsibility
    }
  }
`;

export { GET_STAKEHOLDER };
export type { IStakeholder };
