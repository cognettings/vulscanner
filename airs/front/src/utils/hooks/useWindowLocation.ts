const getWindowLocation = (): string => {
  if (typeof window !== "undefined") {
    return window.location.href;
  }

  return "https://fluidattacks.com/";
};

const getCurrentEnvironment = (): string => {
  const prefix = getWindowLocation().split("/");
  if (prefix[2].startsWith("localhost")) {
    return "local";
  } else if (prefix[2].startsWith("web.eph")) {
    return "eph";
  }

  return "prod";
};

const useWindowLocation = (): string => {
  const isEph = getCurrentEnvironment() === "eph";
  const location = getWindowLocation()
    .split("/")
    .slice(isEph ? 4 : 3)
    .join("/");

  return location;
};

export { useWindowLocation };
