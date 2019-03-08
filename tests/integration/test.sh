#!/usr/bin/env bats

# Integration tests for Job API Engine

token=$(curl -s -X GET --header 'Accept: application/json' "http://$API_HOST/v1/system/token" | jq -r '.token')

if [ ! -f .ran ]; then
  psql -h "$PSQL_HOST" -U postgres circle_test < structure.sql
  touch .ran
fi

curl -s -X PUT --header 'Accept: application/json' --header "Authorization: Bearer $token"  "http://$API_HOST/v1/jobs/" 2>&1 > /dev/null
psql -h "$PSQL_HOST" -U postgres circle_test < populate.sql 2>&1> /dev/null

@test "test metrics endpoint" {
  curl -s -X GET --header 'Accept: application/json' "http://$API_HOST/v1/system/metrics"
  [ "$?" -eq 0 ]
}

@test "test status endpoint" {
  health=$(curl -s -X GET --header 'Accept: application/json' "http://$API_HOST/v1/system/health" | jq -r '.message')
  [ "$health" == "System is healthy" ]
}

@test "test peek job endpoint" {
  expected_job='{"created_at":"2018-10-23T00:05:30+00:00","id":1,"priority":20,"state":"new"}'
  actual_job=$(curl -s -X GET --header 'Accept: application/json' --header "Authorization: Bearer $token"  "http://$API_HOST/v1/jobs/")
  printf 'Expected: %s\n' "$expected_job"
  printf 'Actual: %s\n' "$actual_job"
  [ "$expected_job" == "$actual_job" ]
}

@test "test pop job endpoint" {
  expected_job='{"created_at":"2018-10-23T00:05:30+00:00","id":1,"priority":20,"state":"new"}'
  actual_job=$(curl -s -X DELETE --header 'Accept: application/json' --header "Authorization: Bearer $token"  "http://$API_HOST/v1/jobs/")
  printf 'Expected: %s\n' "$expected_job"
  printf 'Actual: %s\n' "$actual_job"
  [ "$expected_job" == "$actual_job" ]
}

@test "test get job endpoint" {
  expected_job='{"created_at":"2018-10-23T00:05:30+00:00","id":1,"priority":20,"state":"new"}'
  actual_job=$(curl -s -X GET --header 'Accept: application/json' --header "Authorization: Bearer $token"  "http://$API_HOST/v1/jobs/1")
  printf 'Expected: %s\n' "$expected_job"
  printf 'Actual: %s\n' "$actual_job"
  [ "$expected_job" == "$actual_job" ]
}

@test "test get job endpoint" {
  code=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE --header 'Accept: application/json' --header "Authorization: Bearer $token"  "http://$API_HOST/v1/jobs/1")
  [ "$code" -eq 204 ]
}

@test "test put priority job endpoint" {
  code=$(curl -s -o /dev/null -w "%{http_code}" -X PUT --header 'Accept: application/json' --header "Authorization: Bearer $token"  "http://$API_HOST/v1/jobs/3/priority/10")
  printf 'Expected: %s\n' "200"
  printf 'Actual: %s\n' "$code"
  [ "$code" -eq 200 ]

  expected_job='{"created_at":"2018-10-23T00:05:31+00:00","id":3,"priority":10,"state":"new"}'
  actual_job=$(curl -s -X GET --header 'Accept: application/json' --header "Authorization: Bearer $token"  "http://$API_HOST/v1/jobs/")
  printf 'Expected: %s\n' "$expected_job"
  printf 'Actual: %s\n' "$actual_job"
  [ "$expected_job" == "$actual_job" ]
}
