import styled from "styled-components";

const Radio = styled.input.attrs({
  className: `
    op7
    dn
    transparent
  `,
  type: `radio`,
})``;

const RadioLabel = styled.div.attrs(
  (props: {
    theme: { on: boolean; color: string };
  }): {
    className: string;
  } => ({
    className: `ba br0 db overflow-hidden ph3 pointer pv2 relative switch-mh tc w-100 ${
      props.theme.on ? props.theme.color : "b--moon-gray"
    }`,
  })
)``;

const SwitchItem = styled.li.attrs({
  className: `
  br0 db overflow-hidden pointer pa0 ma0 relative switch-mh tc w-100
  `,
})``;

export { Radio, RadioLabel, SwitchItem };
