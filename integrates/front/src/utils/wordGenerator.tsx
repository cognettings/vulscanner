const consonants: string[] = [
  "b",
  "c",
  "d",
  "f",
  "g",
  "h",
  "j",
  "k",
  "l",
  "m",
  "n",
  "p",
  "r",
  "s",
  "t",
  "v",
  "w",
  "x",
  "y",
  "z",
];

const vowels: string[] = ["a", "e", "i", "o", "u"];

const generateWord = (length: number): string => {
  const iterateChar = (
    actualCharIsConsonant: boolean,
    remainingChars: number,
    word: string
  ): string => {
    if (remainingChars === 0) {
      return word;
    }
    if (actualCharIsConsonant) {
      return iterateChar(
        false,
        remainingChars - 1,
        `${word}${consonants[Math.floor(Math.random() * consonants.length)]}`
      );
    }

    return iterateChar(
      true,
      remainingChars - 1,
      `${word}${vowels[Math.floor(Math.random() * vowels.length)]}`
    );
  };
  const startCharIsConsonant = Math.random() > 0.5;

  return iterateChar(startCharIsConsonant, length, "");
};

export { generateWord };
