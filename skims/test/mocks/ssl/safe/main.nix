{
  inputs,
  makeScript,
  makeSslCertificate,
  makeTemplate,
  managePorts,
  ...
}:
makeScript {
  replace = {
    __argConfig__ = makeTemplate {
      replace = {
        __argHttpServerSslCert__ = makeSslCertificate {
          days = 365;
          name = "skims-test-mocks-ssl-safe";
          options = [["-subj" "/CN=localhost"]];
        };
        __argHttpServerRoot__ = ../http/server/root;
      };
      name = "nginx-conf";
      template = ''
        events {}
        daemon off;
        http {
          server {
            index index.html;
            listen localhost:4445 ssl;
            location / {
              root __argHttpServerRoot__;
            }
            server_name localhost;
            ssl_ciphers EECDH+AESGCM:EDH+AESGCM;
            ssl_certificate __argHttpServerSslCert__/cert.crt;
            ssl_certificate_key __argHttpServerSslCert__/cert.key;
            ssl_ecdh_curve secp384r1;
            ssl_prefer_server_ciphers on;
            ssl_protocols TLSv1.3;
          }
        }
        pid /dev/null;
      '';
    };
  };
  name = "skims-test-mocks-ssl-safe";
  searchPaths = {
    bin = [
      inputs.nixpkgs.nginxLocal
    ];
    source = [
      managePorts
    ];
    rpath = [inputs.nixpkgs.openssl.out];
  };
  entrypoint = ./entrypoint.sh;
}
