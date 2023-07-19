import {
  faArrowDownShortWide,
  faArrowDownWideShort,
  faCheck,
} from "@fortawesome/free-solid-svg-icons";
import React, { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import type { ISortDropdown } from "./types";

import { Button } from "components/Button";
import { Dropdown } from "components/Dropdown";
import { Col, Row } from "components/Layout";

const SortDropdown: React.FC<ISortDropdown> = ({
  id,
  mappedOptions = [{ header: "", value: "" }],
  onChange,
}: ISortDropdown): JSX.Element => {
  const { t } = useTranslation();
  const [sortDirection, setSortDirection] = useState<"ASC" | "DESC">("DESC");
  const [sortValue, setSortValue] = useState(mappedOptions[0]);

  const handleSortDirectionChange = useCallback((): void => {
    setSortDirection(sortDirection === "ASC" ? "DESC" : "ASC");
  }, [sortDirection]);

  const handleSortValueChange =
    (newSortValue: string, newSortHeader: string): (() => void) =>
    (): void => {
      setSortValue({ header: newSortHeader, value: newSortValue });
    };

  useEffect((): void => {
    onChange(sortValue.value, sortDirection);
  }, [sortValue, sortDirection, onChange]);

  return (
    <Row key={id}>
      <Col>
        <Dropdown
          button={
            <Button
              icon={
                sortDirection === "ASC"
                  ? faArrowDownWideShort
                  : faArrowDownShortWide
              }
              id={`sort-button-${id}`}
              onClick={handleSortDirectionChange}
              tooltip={t("group.toe.sortButton.direction")}
              tooltipPlace={"top"}
              variant={"ghost"}
            >
              {sortValue.header}
            </Button>
          }
          key={id}
        >
          {mappedOptions.map((option): JSX.Element => {
            return (
              <Button
                disp={"block"}
                icon={sortValue.value === option.value ? faCheck : undefined}
                iconSide={"right"}
                key={option.value}
                onClick={handleSortValueChange(option.value, option.header)}
                value={option.value}
              >
                {option.header}
              </Button>
            );
          })}
        </Dropdown>
      </Col>
    </Row>
  );
};

export { SortDropdown };
