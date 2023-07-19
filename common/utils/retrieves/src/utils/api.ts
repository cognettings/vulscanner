import {
  ApolloClient,
  InMemoryCache,
  createHttpLink,
  resetCaches,
} from "@apollo/client/core";
import type { NormalizedCacheObject } from "@apollo/client/core";
import { setContext } from "@apollo/client/link/context";
import fetch from "cross-fetch";

const getClient = (token: string): ApolloClient<NormalizedCacheObject> => {
  resetCaches();
  const authLink = setContext(
    (): {
      headers: {
        authorization: string;
      };
    } => {
      return {
        headers: {
          authorization: `Bearer ${token}`,
        },
      };
    }
  );
  const httpLink = createHttpLink({
    fetch,
    uri: "https://app.fluidattacks.com/api",
  });

  return new ApolloClient({
    cache: new InMemoryCache({}),
    link: authLink.concat(httpLink),
  });
};

export { getClient };
