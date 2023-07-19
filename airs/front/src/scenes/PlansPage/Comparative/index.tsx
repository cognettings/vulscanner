/* eslint react/forbid-component-props: 0 */
import React from "react";
import { useTranslation } from "react-i18next";
import { BsArrowRight } from "react-icons/bs";

import {
  Cell,
  ComparativeTable,
  DescriptionCell,
  HeadColumn,
  Row,
  TableContainer,
} from "./styledComponents";

import { AirsLink } from "../../../components/AirsLink";
import { CloudImage } from "../../../components/CloudImage";
import { Container } from "../../../components/Container";
import { Text, Title } from "../../../components/Typography";

interface IComparation {
  text: string;
  machine: boolean;
  squad: boolean;
}

const ComparativePlans: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const cells: IComparation[] = [
    {
      machine: true,
      squad: true,
      text: t("plansPage.comparativePlans.characteristics.characteristic1"),
    },
    {
      machine: true,
      squad: true,
      text: t("plansPage.comparativePlans.characteristics.characteristic2"),
    },
    {
      machine: true,
      squad: true,
      text: t("plansPage.comparativePlans.characteristics.characteristic3"),
    },
    {
      machine: true,
      squad: true,
      text: t("plansPage.comparativePlans.characteristics.characteristic4"),
    },
    {
      machine: true,
      squad: true,
      text: t("plansPage.comparativePlans.characteristics.characteristic5"),
    },
    {
      machine: true,
      squad: true,
      text: t("plansPage.comparativePlans.characteristics.characteristic6"),
    },
    {
      machine: false,
      squad: true,
      text: t("plansPage.comparativePlans.characteristics.characteristic7"),
    },
    {
      machine: false,
      squad: true,
      text: t("plansPage.comparativePlans.characteristics.characteristic8"),
    },
    {
      machine: false,
      squad: true,
      text: t("plansPage.comparativePlans.characteristics.characteristic9"),
    },
    {
      machine: false,
      squad: true,
      text: t("plansPage.comparativePlans.characteristics.characteristic10"),
    },
    {
      machine: false,
      squad: true,
      text: t("plansPage.comparativePlans.characteristics.characteristic11"),
    },
  ];

  return (
    <Container
      align={"center"}
      bgColor={"#ffffff"}
      display={"flex"}
      id={"comparative-plans-table"}
      justify={"center"}
      ph={4}
      pv={5}
      wrap={"wrap"}
    >
      <Title
        color={"#bf0b1a"}
        level={3}
        mb={3}
        size={"small"}
        textAlign={"center"}
      >
        {t("plansPage.comparativePlans.title")}
      </Title>
      <Container maxWidth={"951px"} ph={4}>
        <Title
          color={"#2e2e38"}
          level={1}
          mb={3}
          size={"medium"}
          textAlign={"center"}
        >
          {t("plansPage.comparativePlans.subtitle")}
        </Title>
      </Container>
      <Text color={"#535365"} mb={4} size={"medium"} textAlign={"center"}>
        {t("plansPage.comparativePlans.paragraph")}
      </Text>
      <TableContainer>
        <ComparativeTable>
          <HeadColumn />
          <HeadColumn>
            <Title color={"#2e2e38"} level={3} size={"xs"} textAlign={"center"}>
              {t("plansPage.comparativePlans.machineTitle")}
            </Title>
            <AirsLink
              decoration={"underline"}
              hovercolor={"#bf0b1a"}
              href={"https://app.fluidattacks.com/SignUp"}
            >
              <Text color={"#2e2e38"} mt={2}>
                {t("plansPage.header.button.machine")}
                <BsArrowRight size={13} style={{ marginLeft: "7px" }} />
              </Text>
            </AirsLink>
          </HeadColumn>
          <HeadColumn>
            <Title
              color={"#2e2e38"}
              level={3}
              mt={4}
              size={"xs"}
              textAlign={"center"}
            >
              {t("plansPage.comparativePlans.squadTitle")}
            </Title>
            <AirsLink
              decoration={"underline"}
              hovercolor={"#bf0b1a"}
              href={"/contact-us/"}
            >
              <Text color={"#2e2e38"} mt={2}>
                {t("plansPage.header.button.squad")}
                <BsArrowRight size={13} style={{ marginLeft: "7px" }} />
              </Text>
            </AirsLink>
          </HeadColumn>
          <tbody>
            {[...Array(11).keys()].map(
              (el: number): JSX.Element => (
                <Row key={`row-${el}`}>
                  <DescriptionCell key={`descriptionCell-${el}`}>
                    <Text color={"#535365"}>{cells[el].text}</Text>
                  </DescriptionCell>
                  <Cell key={`cell-${el}`}>
                    <CloudImage
                      alt={"plans-icon"}
                      key={`icon-image${el}`}
                      src={
                        cells[el].machine
                          ? "airs/plans/circle-check.png"
                          : "airs/plans/circle-xmark.png"
                      }
                    />
                  </Cell>
                  <Cell>
                    <CloudImage
                      alt={"plans-icon"}
                      key={`icon-image${el}`}
                      src={
                        cells[el].squad
                          ? "airs/plans/circle-check.png"
                          : "airs/plans/circle-xmark.png"
                      }
                    />
                  </Cell>
                </Row>
              )
            )}
          </tbody>
        </ComparativeTable>
      </TableContainer>
    </Container>
  );
};

export { ComparativePlans };
