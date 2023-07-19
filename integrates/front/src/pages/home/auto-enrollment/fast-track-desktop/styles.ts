import { Field } from "formik";
import styled from "styled-components";

const RepoButton = styled.div`
  position: relative;
  border: 1px solid #e9e9ed;
  border-radius: 4px;
  align-items: center;
  background-color: #fff;
  display: flex;
  height: 100px;
  justify-content: center;
  width: 276px;
  margin: 18px;

  :hover {
    box-shadow: 0 0 15px 0 #dddde3;
  }
`;

const Radio = styled(Field)`
  position: absolute;
  top: 10%;
  left: 3%;

  border: 2px solid white;
  box-shadow: 0 0 0 1px #dddde3;
  appearance: none;
  border-radius: 50%;
  width: 12px;
  height: 12px;
  background-color: #fff;
  transition: all ease-in 0.2s;

  :checked {
    background-color: #bf0b1a;
    box-shadow: 0 0 0 1px #bf0b1a;
  }
`;

const Label = styled.label`
  align-items: center;
  cursor: pointer;
  display: flex;
  height: 100%;
  justify-content: center;
  width: 100%;
`;

const ManualLink = styled.a`
  color: #bf0b1a;
  cursor: pointer;
  font-size: 14px;
  margin: 0 0 0 4px;
  text-decoration: underline;
`;

export { Label, ManualLink, Radio, RepoButton };
