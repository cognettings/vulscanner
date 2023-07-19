/* eslint react/forbid-component-props: 0 */
import React, { useCallback, useState } from "react";

import {
  MenuItem,
  RadioButton,
  RadioLabel,
} from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";

const ClientsMenuButtons: React.FC = (): JSX.Element => {
  const [filter, setFilter] = useState("all-clients");
  const filterCards = useCallback(
    ({ target }: React.ChangeEvent<HTMLInputElement>): void => {
      const targetId = (target as HTMLInputElement).id;
      setFilter(targetId);
      const cards = document.getElementsByClassName("all-clients-cards");
      const arrayCards = Array.from(cards);
      arrayCards.forEach((card): void => {
        const classes = Array.from(card.classList);
        if (classes.includes(`${targetId}-cards`)) {
          card.classList.remove("dn");
          card.classList.add("dt-ns");
        } else {
          card.classList.remove("dt-ns");
          card.classList.add("dn");
        }
      });
    },
    []
  );

  return (
    <React.Fragment>
      <MenuItem>
        <RadioButton
          checked={filter === "all-clients"}
          className={"all-clients"}
          id={"all-clients"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-all"} htmlFor={"all-clients"}>
          {translate.t("clients.buttons.all")}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "banking"}
          className={"banking"}
          id={"banking"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-banking"} htmlFor={"banking"}>
          {translate.t("clients.buttons.finance")}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "fintech"}
          className={"fintech"}
          id={"fintech"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-fintech"} htmlFor={"fintech"}>
          {translate.t("clients.buttons.fintech")}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "oil-energy"}
          className={"oil-energy"}
          id={"oil-energy"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-oil-energy"} htmlFor={"oil-energy"}>
          {translate.t("clients.buttons.energy")}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "healthcare"}
          className={"healthcare"}
          id={"healthcare"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-healthcare"} htmlFor={"healthcare"}>
          {translate.t("clients.buttons.health")}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "airlines"}
          className={"airlines"}
          id={"airlines"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-airlines"} htmlFor={"airlines"}>
          {translate.t("clients.buttons.airlines")}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "telecommunications"}
          className={"telecommunications"}
          id={"telecommunications"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel
          className={"tag-telecommunications"}
          htmlFor={"telecommunications"}
        >
          {translate.t("clients.buttons.telecommunications")}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "technology"}
          className={"technology"}
          id={"technology"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-technology"} htmlFor={"technology"}>
          {translate.t("clients.buttons.technology")}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "retail"}
          className={"retail"}
          id={"retail"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-retail"} htmlFor={"retail"}>
          {translate.t("clients.buttons.retail")}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "construction"}
          className={"construction"}
          id={"construction"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-construction"} htmlFor={"construction"}>
          {translate.t("clients.buttons.construction")}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "food-beverage"}
          className={"food-beverage"}
          id={"food-beverage"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-food-beverage"} htmlFor={"food-beverage"}>
          {translate.t("clients.buttons.food")}
        </RadioLabel>
      </MenuItem>
    </React.Fragment>
  );
};

export { ClientsMenuButtons };
