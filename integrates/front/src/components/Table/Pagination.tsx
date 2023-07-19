import {
  faAngleLeft,
  faAngleRight,
  faAnglesLeft,
  faAnglesRight,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { RowData, Table } from "@tanstack/react-table";
import _ from "lodash";
import React, { useCallback, useEffect } from "react";
import styled from "styled-components";

import type { ITableProps } from "./types";

import { Button } from "components/Button";
import { Text } from "components/Text";

interface IPaginationProps<TData extends RowData>
  extends Pick<ITableProps<TData>, "onNextPage"> {
  hasNextPage?: boolean;
  size: number;
  table: Table<TData>;
}

const PaginationBox = styled.div.attrs({
  className: "comp-table-pagination",
})`
  align-items: center;
  background-color: #2e2e38;
  border-radius: 4px;
  display: flex;
  margin-top: 4px;
  padding: 4px;
`;

const Pagination = <TData extends RowData>({
  hasNextPage = false,
  onNextPage = undefined,
  size,
  table,
}: Readonly<IPaginationProps<TData>>): JSX.Element => {
  const pageCount = table.getPageCount();
  const { pageIndex, pageSize } = table.getState().pagination;
  const isInLast = pageCount - pageIndex <= 2;
  const lastPage = Math.min(100, size);
  const textSize = size >= 10000 ? `+${size}` : size;

  useEffect((): void => {
    if (pageIndex + 1 > pageCount) {
      table.setPageIndex(0);
    }
  }, [pageCount, pageIndex, table]);

  const goToNext = useCallback((): void => {
    if (isInLast && onNextPage) {
      void onNextPage().finally((): void => {
        table.setPageIndex(pageIndex + 1);
      });
    } else {
      table.setPageIndex(pageIndex + 1);
    }
  }, [isInLast, onNextPage, pageIndex, table]);

  const needLoadMore = hasNextPage && isInLast;
  const indexes = _.range(
    Math.max(pageIndex - 2, 0),
    Math.min(pageIndex + 2, pageCount - 1) + 1
  );

  const handlePreviousPage = useCallback((): void => {
    table.previousPage();
  }, [table]);

  const handleClickFilter = useCallback(
    (el: number): (() => void) =>
      (): void => {
        if (el === lastPage && onNextPage) {
          void onNextPage().finally((): void => {
            table.setPageSize(el);
          });
        } else {
          table.setPageSize(el);
        }
      },
    [lastPage, onNextPage, table]
  );

  const handleClickIndexes = useCallback(
    (el: number): (() => void) =>
      (): void => {
        if (el === pageCount - 1 && onNextPage) {
          void onNextPage().finally((): void => {
            table.setPageIndex(el);
          });
        } else {
          table.setPageIndex(el);
        }
      },
    [onNextPage, pageCount, table]
  );

  const handleFirstPage = useCallback((): void => {
    table.setPageIndex(0);
  }, [table]);

  const handleLastPage = useCallback((): void => {
    if (needLoadMore && onNextPage) {
      void onNextPage().finally((): void => {
        const lastIndex = indexes[indexes.length - 1];
        table.setPageIndex(Math.max(lastIndex, pageCount - 1));
      });
    } else {
      table.setPageIndex(pageCount - 1);
    }
  }, [indexes, needLoadMore, onNextPage, pageCount, table]);

  return (
    <PaginationBox>
      {[10, 20, 50, lastPage]
        .filter((el): boolean => el <= size)
        .map(
          (el: number): JSX.Element => (
            <Button
              key={el}
              onClick={handleClickFilter(el)}
              size={"sm"}
              variant={el === pageSize ? "selected" : "secondary"}
            >
              <div style={{ textAlign: "center", width: "25px" }}>{el}</div>
            </Button>
          )
        )}
      <Text ml={3} size={"xs"} tone={"light"}>
        {`${pageSize * pageIndex + 1} - ${Math.min(
          pageSize * (pageIndex + 1),
          size
        )} of ${textSize} items`}
      </Text>
      <Button
        disabled={!table.getCanPreviousPage()}
        onClick={handleFirstPage}
        size={"sm"}
        variant={"secondary"}
      >
        <FontAwesomeIcon icon={faAnglesLeft} />
      </Button>
      <Button
        disabled={!table.getCanPreviousPage()}
        onClick={handlePreviousPage}
        size={"sm"}
        variant={"secondary"}
      >
        <FontAwesomeIcon icon={faAngleLeft} />
      </Button>
      {indexes.map(
        (el: number): JSX.Element => (
          <Button
            key={el}
            onClick={handleClickIndexes(el)}
            size={"sm"}
            variant={el === pageIndex ? "selected" : "secondary"}
          >
            <div style={{ textAlign: "center", width: "15px" }}>{el + 1}</div>
          </Button>
        )
      )}
      <Button
        disabled={!table.getCanNextPage() && !needLoadMore}
        onClick={goToNext}
        size={"sm"}
        variant={"secondary"}
      >
        <FontAwesomeIcon icon={faAngleRight} />
      </Button>
      <Button
        disabled={!table.getCanNextPage() && !needLoadMore}
        onClick={handleLastPage}
        size={"sm"}
        variant={"secondary"}
      >
        <FontAwesomeIcon icon={faAnglesRight} />
      </Button>
    </PaginationBox>
  );
};

export { Pagination };
