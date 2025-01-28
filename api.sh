curl -X PUT -u "username:app_password" \
"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}" \
-H "Content-Type: application/json" \
-d '{"archived": true}'


curl -X PUT -u "username:app_password" \
"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}" \
-H "Content-Type: application/json" \
-d '{"archived": false}'

curl -X GET -u "username:app_password" \
"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}"
