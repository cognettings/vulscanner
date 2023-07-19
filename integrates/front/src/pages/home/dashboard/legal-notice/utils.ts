const comesFromLogin = (): boolean => {
  const loginReferrers = [
    "https://app.fluidattacks.com/",
    "https://account.live.com/",
    "https://login.live.com/",
    "https://bitbucket.org/",
  ];
  const isGoogleLogin = document.referrer.startsWith("https://accounts.google");

  return loginReferrers.includes(document.referrer) || isGoogleLogin;
};

export { comesFromLogin };
