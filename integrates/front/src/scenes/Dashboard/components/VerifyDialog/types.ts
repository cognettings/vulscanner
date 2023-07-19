interface IVerifyStakeholderResultAttr {
  verifyStakeholder: {
    success: boolean;
  };
}

interface IPhoneAttr {
  callingCountryCode: string;
  countryCode: string;
  nationalNumber: string;
}

interface IGetStakeholderPhoneAttr {
  me: {
    phone: IPhoneAttr | null;
  };
}

interface IVerifyFn {
  (
    verifyCallback: (verificationCode: string) => void,
    cancelCallback: () => void
  ): void;
}

interface IVerifyFormValues {
  verificationCode: string;
}

interface IVerifyDialogProps {
  disable?: boolean;
  isOpen: boolean;
  message?: React.ReactNode;
  children: (verify: IVerifyFn) => React.ReactNode;
}

export type {
  IPhoneAttr,
  IGetStakeholderPhoneAttr,
  IVerifyDialogProps,
  IVerifyFormValues,
  IVerifyFn,
  IVerifyStakeholderResultAttr,
};
