import styled from "styled-components";

const PlanTag = styled.div`
  border-top: 5px solid #fbbac0;
  border-radius: 10px;
  box-shadow: 5px 10px 16px 0px rgba(0, 0, 0, 0.06);
  width: 100%;
  max-width: 714px;
`;

const Tag = styled.span`
  align-items: center;
  border-radius: 50px;
  display: inline-flex;
  font-weight: 400;
  max-height: 34px;
  padding: 0px 12px;
  font-size: 16px;
  text-align: center;
  background-color: #fdd8da;
  border: 1px solid #bf0b1a;
  color: #bf0b1a;
`;

const PlansGrid = styled.div`
  display: grid;
  gap: 1rem;
  padding-top: 16px;
  padding-bottom: 16px;
  padding-left: 16px;
  padding-right: 16px;
  max-width: 1500px;
  width: 1480px;
  @media screen and (min-width: 1200px) {
    grid-template-columns: 1fr 1fr;
    padding-left: 40px;
    padding-right: 40px;
  }

  @media screen and (min-width: 960px) and (max-width: 1200px) {
    grid-template-columns: 1fr 1fr;
    justify-content: center;
  }

  @media screen and (max-width: 960px) {
    flex-wrap: wrap;
    display: flex;
    justify-content: center;
    align-items: center;
  }
`;

export { PlanTag, PlansGrid, Tag };
