import styled from "styled-components";

const Container = styled.div`
  /* stylelint-disable selector-class-pattern */
  .StripeElement {
    align-items: center;
    background-color: #fff;
    border: 1px solid #d2d2da;
    border-radius: 4px;
    box-sizing: border-box;
    color: #b0b0bf;
    line-height: 1.25;
    padding: 8px 12px;
    transition: all 0.3s ease;

    ::placeholder {
      color: #b0b0bf;
    }
  }

  .StripeElement--focus {
    box-shadow: 0 1px 3px 0 #cfd7df;
  }

  .StripeElement--invalid {
    border-color: #da1e28;
  }

  .StripeElement--webkit-autofill {
    background-color: #fefde5 !important;
  }
`;

export { Container };
