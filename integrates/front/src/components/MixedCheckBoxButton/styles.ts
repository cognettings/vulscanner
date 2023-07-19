import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const CheckBox: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `br0 relative checkbox-mh w-100 flex b--moon-gray`,
})``;

const CheckBoxOption: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs(
  (props: {
    theme: {
      selected: boolean;
      type: string;
    };
  }): {
    className: string;
  } => ({
    className: `absolute ba bottom-0 top-0 tc pv2 white ${
      props.theme.type === "yes"
        ? "green-checkbox left-0"
        : "red-checkbox right-0"
    } ${props.theme.selected ? "w-100" : "w-50"} `,
  })
)``;

export { CheckBox, CheckBoxOption };
