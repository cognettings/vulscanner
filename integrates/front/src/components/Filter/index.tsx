import { faFilter } from "@fortawesome/free-solid-svg-icons";
import React, { useCallback, useEffect, useState } from "react";

import { AppliedFilters } from "./AppliedFilters";
import { Filter } from "./filters";
import type {
  IFilter,
  IFiltersProps,
  IPermanentData,
  ISwitchOptions,
} from "./types";
import { getMappedOptions } from "./utils";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Col, Row } from "components/Layout";
import { SidePanel } from "components/SidePanel";
import { useFilters } from "hooks";

const Filters = <IData extends object>({
  dataset = undefined,
  permaset = undefined,
  filters,
  setFilters,
}: IFiltersProps<IData>): JSX.Element => {
  const [open, setOpen] = useState(false);

  const openPanel = useCallback((): void => {
    setOpen(true);
  }, []);
  const closePanel = useCallback((): void => {
    setOpen(false);
  }, []);

  const [permaValues, setPermaValues] = permaset ?? [undefined, undefined];

  const setPermanentValues = useCallback(
    ({
      id,
      value,
      rangeValues,
      numberRangeValues,
      switchValues,
      checkValues,
    }: IPermanentData): void => {
      setPermaValues?.(
        permaValues.map((permadata): IPermanentData => {
          if (permadata.id === id) {
            return {
              ...permadata,
              checkValues,
              numberRangeValues,
              rangeValues,
              switchValues,
              value,
            };
          }

          return permadata;
        })
      );
    },
    [permaValues, setPermaValues]
  );

  const removeFilter = useCallback(
    (filterToReset: IFilter<IData>): (() => void) => {
      return (): void => {
        setFilters(
          filters.map((filter: IFilter<IData>): IFilter<IData> => {
            if (filter.id === filterToReset.id) {
              const switchValues = filter.switchValues?.map(
                (checkedValue: ISwitchOptions): ISwitchOptions => {
                  return { ...checkedValue, checked: false };
                }
              );

              return {
                ...filter,
                checkValues: [],
                numberRangeValues: [undefined, undefined],
                rangeValues: ["", ""],
                switchValues,
                value: "",
              };
            }

            return {
              ...filter,
            };
          })
        );
        setPermaValues?.(
          permaValues.map((permadata): IPermanentData => {
            if (permadata.id === filterToReset.id) {
              const switchValues = permadata.switchValues?.map(
                (checkedValue: ISwitchOptions): ISwitchOptions => {
                  return { ...checkedValue, checked: false };
                }
              );

              return {
                ...permadata,
                checkValues: [],
                numberRangeValues: [undefined, undefined],
                rangeValues: ["", ""],
                switchValues,
                value: "",
              };
            }

            return {
              ...permadata,
            };
          })
        );
      };
    },
    [filters, permaValues, setFilters, setPermaValues]
  );

  function resetFiltersHandler(): (event: React.FormEvent) => void {
    return (event: React.FormEvent): void => {
      setFilters(
        filters.map((filter: IFilter<IData>): IFilter<IData> => {
          const switchValues = filter.switchValues?.map(
            (checkedValue: ISwitchOptions): ISwitchOptions => {
              return { ...checkedValue, checked: false };
            }
          );

          return {
            ...filter,
            checkValues: [],
            numberRangeValues: [undefined, undefined],
            rangeValues: ["", ""],
            switchValues,
            value: "",
          };
        })
      );
      setPermaValues?.(
        permaValues.map((permadata): IPermanentData => {
          const switchValues = permadata.switchValues?.map(
            (checkedValue: ISwitchOptions): ISwitchOptions => {
              return { ...checkedValue, checked: false };
            }
          );

          return {
            ...permadata,
            checkValues: [],
            numberRangeValues: [undefined, undefined],
            rangeValues: ["", ""],
            switchValues,
            value: "",
          };
        })
      );
      event.stopPropagation();
    };
  }

  const onChangeHandler = useCallback(
    (permanentData: IPermanentData): void => {
      setFilters(
        filters.map((filter): IFilter<IData> => {
          if (filter.id === permanentData.id) {
            setPermanentValues(permanentData);

            return {
              ...filter,
              ...permanentData,
            };
          }

          return filter;
        })
      );
    },
    [filters, setFilters, setPermanentValues]
  );

  useEffect((): void => {
    if (permaset === undefined) return;
    setFilters(
      filters.map((filter): IFilter<IData> => {
        const permaValue = permaValues?.find(
          (permadata): boolean => permadata.id === filter.id
        );

        return {
          ...filter,
          checkValues: permaValue?.checkValues ?? filter.checkValues,
          numberRangeValues:
            permaValue?.numberRangeValues ?? filter.numberRangeValues,
          rangeValues: permaValue?.rangeValues ?? filter.rangeValues,
          switchValues: permaValue?.switchValues ?? filter.switchValues,
          value: permaValue?.value ?? filter.value,
        };
      })
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <React.Fragment>
      <Container align={"center"} display={"flex"} pb={"4px"} wrap={"wrap"}>
        <Container pr={"4px"}>
          <Button
            icon={faFilter}
            id={"filter-config"}
            onClick={openPanel}
            variant={"ghost"}
          >
            {"Add filter"}
          </Button>
        </Container>
        <AppliedFilters
          dataset={dataset}
          filters={filters as IFilter<object>[]}
          onClose={removeFilter}
        />
      </Container>
      <SidePanel onClose={closePanel} open={open}>
        <React.Fragment>
          {filters.map((filter: IFilter<IData>): JSX.Element => {
            const mappedOptions = getMappedOptions(
              filter as IFilter<object>,
              dataset
            );

            return (
              <Filter
                checkValues={filter.checkValues}
                id={filter.id}
                key={filter.id}
                label={filter.label}
                mappedOptions={mappedOptions}
                minMaxRangeValues={filter.minMaxRangeValues}
                numberRangeValues={filter.numberRangeValues}
                onChange={onChangeHandler}
                rangeValues={filter.rangeValues}
                switchValues={filter.switchValues}
                type={filter.type}
                value={filter.value}
              />
            );
          })}
          <Row>
            <Col>
              <Button onClick={resetFiltersHandler()} variant={"secondary"}>
                {"Clear filters"}
              </Button>
            </Col>
          </Row>
        </React.Fragment>
      </SidePanel>
    </React.Fragment>
  );
};

export type { IFilter, IPermanentData };
export { Filters, useFilters };
