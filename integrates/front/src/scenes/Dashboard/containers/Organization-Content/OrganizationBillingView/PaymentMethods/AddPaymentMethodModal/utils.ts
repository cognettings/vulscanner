const MAX_CARD_NUMBER_LENGTH = 17;
const MAX_DATE_NUMBER_LENGTH = 3;
const MAX_CVC_NUMBER_LENGTH = 5;

const maxDateLengthAllowed = (value: number | undefined): boolean => {
  if (value === undefined) {
    return false;
  }

  return value.toString().length < MAX_DATE_NUMBER_LENGTH;
};

const maxCardLengthAllowed = (value: number | undefined): boolean => {
  if (value === undefined) {
    return false;
  }

  return value.toString().length < MAX_CARD_NUMBER_LENGTH;
};

const maxCvcLengthAllowed = (value: number | undefined): boolean => {
  if (value === undefined) {
    return false;
  }

  return value.toString().length < MAX_CVC_NUMBER_LENGTH;
};

export { maxCardLengthAllowed, maxCvcLengthAllowed, maxDateLengthAllowed };
