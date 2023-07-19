module.exports = {
  parserOpts: {
    headerPattern:
      /^(airs|all|common|docs|integrates|melts|observes|skims|sorts|teaches)\\(\w*)\((\w*)\):\s(#[1-9]\d*)\s(.*)$/,
    headerCorrespondence: ["product", "type", "scope", "ticket", "subject"],
  },
};
