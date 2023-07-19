interface IStakeholderFormValues {
  email: string;
  responsibility?: string;
  role: string;
}

interface IAddStakeholderModalProps {
  action: "add" | "edit";
  editTitle: string;
  initialValues?: IStakeholderFormValues;
  open: boolean;
  organizationId?: string;
  groupName?: string;
  domainSuggestions: string[];
  suggestions: string[];
  title: string;
  type: "group" | "organization" | "user";
  onClose: () => void;
  onSubmit: (values: IStakeholderFormValues) => Promise<void>;
}

export type { IAddStakeholderModalProps, IStakeholderFormValues };
