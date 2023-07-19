import type { IStakeholderFormValues } from "./types";

const getInitialValues = (
  initialValues: IStakeholderFormValues | undefined,
  action: string
): IStakeholderFormValues => {
  if (action === "edit" && initialValues !== undefined) {
    return {
      email: initialValues.email,
      responsibility: initialValues.responsibility,
      role: initialValues.role.toUpperCase(),
    };
  }

  return {
    email: "",
    responsibility: "",
    role: "",
  };
};

const getSuggestions = (
  email: string,
  emailSuggestions: string[],
  domainSuggestions: string[]
): string[] => {
  if (email.length > 1 && email.endsWith("@")) {
    const emailWithDomainSuggestions = domainSuggestions.map(
      (domain): string => `${email}${domain}`
    );

    return Array.from(
      new Set([...emailSuggestions, ...emailWithDomainSuggestions])
    );
  }

  return Array.from(new Set(emailSuggestions));
};

export { getInitialValues, getSuggestions };
