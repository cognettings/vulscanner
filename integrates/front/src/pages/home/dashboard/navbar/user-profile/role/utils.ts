const getLevel = (
  groupName: string | undefined,
  organizationName: string | undefined
): "group" | "organization" | "user" => {
  if (groupName !== undefined) {
    return "group";
  }

  if (organizationName !== undefined) {
    return "organization";
  }

  return "user";
};

export { getLevel };
