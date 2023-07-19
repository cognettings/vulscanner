import React from "react";
import { FiChevronLeft, FiChevronRight } from "react-icons/fi";
import ReactPaginate from "react-paginate";

interface IPaginator {
  forcePage: number;
  onChange: (prop: { selected: number }) => void;
  pageCount: number;
}

export const Pagination: React.FC<IPaginator> = ({
  forcePage,
  onChange,
  pageCount,
}: IPaginator): JSX.Element => (
  <ReactPaginate
    activeLinkClassName={"active"}
    breakClassName={"break-item"}
    containerClassName={"pagination-container"}
    forcePage={forcePage}
    marginPagesDisplayed={1}
    nextClassName={"page-item"}
    nextLabel={<FiChevronRight />}
    nextLinkClassName={"page-link"}
    onPageChange={onChange}
    pageClassName={"page-item"}
    pageCount={pageCount}
    pageLinkClassName={"page-link"}
    pageRangeDisplayed={3}
    previousClassName={"page-item"}
    previousLabel={<FiChevronLeft />}
    previousLinkClassName={"page-link"}
  />
);
