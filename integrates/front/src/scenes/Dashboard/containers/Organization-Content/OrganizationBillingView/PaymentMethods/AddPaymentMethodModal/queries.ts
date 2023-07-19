import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_CREDIT_CARD_PAYMENT_METHOD: DocumentNode = gql`
  mutation addCreditCardPaymentMethod(
    $makeDefault: Boolean!
    $organizationId: String!
    $paymentMethodId: String!
  ) {
    addCreditCardPaymentMethod(
      makeDefault: $makeDefault
      organizationId: $organizationId
      paymentMethodId: $paymentMethodId
    ) {
      success
    }
  }
`;

const ADD_OTHER_PAYMENT_METHOD: DocumentNode = gql`
  mutation addOtherPaymentMethod(
    $organizationId: String!
    $businessName: String!
    $email: String!
    $country: String!
    $state: String!
    $city: String!
    $rut: Upload
    $taxId: Upload
  ) {
    addOtherPaymentMethod(
      organizationId: $organizationId
      businessName: $businessName
      email: $email
      country: $country
      state: $state
      city: $city
      rut: $rut
      taxId: $taxId
    ) {
      success
    }
  }
`;

export { ADD_CREDIT_CARD_PAYMENT_METHOD, ADD_OTHER_PAYMENT_METHOD };
