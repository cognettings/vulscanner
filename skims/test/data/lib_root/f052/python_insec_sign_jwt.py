# pylint: skip-file
import jwt

payload = {"user_id": 123}
secret_key = "my_secret_key"

safe_alg = "HS512"
dang_alg = "HS256"

safe_headers = {"alg": "HS512"}
dang_headers = {"alg": "HS256"}

# Must fail no alg specified, default is HS256
# See https://pyjwt.readthedocs.io/en/stable/api.html
# Line 16 must be marked
jwt_token = jwt.encode(payload, secret_key)

# Must fail unsafe alg explicitly used
# Line 20 must be marked
jwt_token_ii = jwt.encode(payload, secret_key, algorithm="HS256")

# Must fail unsafe alg explicitly used (using variable)
# Line 24 must be marked
jwt_token_iii = jwt.encode(payload, secret_key, algorithm=dang_alg)

# Must fail dangerous algorithm set through headers
# Line 28 must be marked
jwt_token_iv = jwt.encode(payload, secret_key, headers=dang_headers)


# Safe usage: NO ONE OF FOLLOWING SHOULD BE MARKED
jwt_token_v = jwt.encode(payload, secret_key, algorithm="HS512")
jwt_token_vi = jwt.encode(payload, secret_key, algorithm=safe_alg)
jwt_token_vii = jwt.encode(payload, secret_key, headers=safe_headers)
