# shellcheck shell=bash

export AWS_DEFAULT_REGION="us-east-1"
export DYNAMO_PHASE_1=__argDynamoPhase1__
export DYNAMO_PHASE_3=__argDynamoPhase3__
export DYNAMO_PREPARE_LOADING=__argPrepareLoading__
export DYNAMO_DETERMINE_SCHEMA=__argDynamoSchema__

dynamo-etl "${@}"
