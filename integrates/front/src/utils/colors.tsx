import type { ITagProps } from "components/Tag";

const statusBlueColor: string[] = ["App", "Code", "Infra"];
const statusGreenColor: string[] = [
  "Active",
  "Closed",
  "Confirmed",
  "Enabled",
  "Ok",
  "Registered",
  "Safe",
  "Secure",
  "Solved",
  "Submitted",
  "Success",
  "Verified (closed)",
];
const statusOrangeColor: string[] = [
  "Accepted",
  "Cloning",
  "Created",
  "Draft",
  "In progress",
  "Masked",
  "New",
  "On_hold",
  "Pending",
  "Pending verification",
  "Partially closed",
  "Permanently accepted",
  "Requested",
  "Temporarily accepted",
  "Untreated",
];
const statusRedColor: string[] = [
  "Disabled",
  "Failed",
  "Inactive",
  "Open",
  "Rejected",
  "Unregistered",
  "Unsolved",
  "Verified (open)",
  "Vulnerable",
  "Vulnerable",
];

const getBgColor = (value: string): ITagProps["variant"] => {
  if (statusGreenColor.includes(value)) return "green";
  if (statusOrangeColor.includes(value)) return "orange";
  if (statusRedColor.includes(value)) return "red";

  return statusBlueColor.includes(value) ? "blue" : "gray";
};

const getBgColorTech = (value: string): ITagProps["variant"] => {
  if (value.toLowerCase() === "cspm") return "techCspm";
  if (value.toLowerCase() === "dast") return "techDast";
  if (value.toLowerCase() === "mpt") return "techMpt";
  if (value.toLowerCase() === "re") return "techRe";
  if (value.toLowerCase() === "sast") return "techSast";
  if (value.toLowerCase() === "sca") return "techSca";

  return value.toLocaleLowerCase() === "scr" ? "techScr" : "gray";
};

export { getBgColor, getBgColorTech };
