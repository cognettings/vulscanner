import React from "react";

const Vector: React.FC = (): JSX.Element => {
  return (
    <svg
      fill={"none"}
      height={"2053"}
      viewBox={"0 0 56 2053"}
      width={"100"}
      xmlns={"http://www.w3.org/2000/svg"}
    >
      <path
        d={
          "M52.4995 0.761719V589.636C52.4995 596.263 47.1269 601.636 40.4995 601.636H22.3957C15.7683 601.636 10.3957 607.009 10.3957 613.636V1178.49C10.3957 1185.12 15.7683 1190.49 22.3957 1190.49H34.6031C41.2305 1190.49 46.6031 1195.86 46.6031 1202.49V1314.9V1684.41C46.6031 1691.04 41.2305 1696.41 34.6031 1696.41H15.5005C8.87309 1696.41 3.50049 1701.78 3.5005 1708.41L3.50069 2052.03"
        }
        id={"vector"}
        stroke={"url(#paint0_linear_639_4777)"}
        strokeWidth={"6"}
      />
      <defs>
        <linearGradient
          gradientUnits={"userSpaceOnUse"}
          id={"paint0_linear_639_4777"}
          x1={"52.5018"}
          x2={"-78.5236"}
          y1={"-22.0626"}
          y2={"-16.9348"}
        >
          <stop stopColor={"#E5142F"} stopOpacity={"0"} />
          <stop offset={"0.307292"} stopColor={"#FB1427"} />
          <stop
            offset={"0.482292"}
            stopColor={"#DC4440"}
            stopOpacity={"0.82"}
          />
          <stop offset={"1"} stopColor={"#DA352C"} stopOpacity={"0.07"} />
        </linearGradient>
      </defs>
      <circle cx={"0"} cy={"0"} fill={"#da352c"} id={"dot"} r={"8"} />
    </svg>
  );
};

export { Vector };
