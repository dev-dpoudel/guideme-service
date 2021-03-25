The Database instance can be configured for security before production.
Use the following command to save a admin user.

use admin (Switches to database admin)

db.createUser({
  user: "guide",
  pwd: "GuideAdmin",
  roles: [
  {role: "userAdminAnyDatabase",
  db: "admin"},
  "readWriteAnyDatabase"
  ]
  })

https://github.com/tiangolo/fastapi/tree/master/fastapi/security
https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/#security-in-decorator-dependencies
