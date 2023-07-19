import styled from "styled-components";

const Card = styled.div`
  width: 45%;
  box-sizing: border-box;
  margin: 10px;
  display: flex;
  padding: 20px;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 10px;
  border-radius: 30px;
  background-color: #25252d;
  @media screen and (max-width: 480px) {
    width: 80%;
  }
`;

export { Card };
