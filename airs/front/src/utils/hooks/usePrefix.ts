import { useWindowLocation } from "./useWindowLocation";

const getPrefix = (location: string): string => {
  if (location.split("/")[2] === "web.eph.fluidattacks.com") {
    return location.split("/")[4];
  }

  return location.split("/")[3];
};

const usePrefix = (): string => {
  const location = useWindowLocation();
  const prefix = getPrefix(location);
  const lng = prefix === "" ? "en" : "es";

  return lng;
};

export { usePrefix };
