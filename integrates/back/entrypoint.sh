# shellcheck shell=bash

function serve {
  local env="${1-}"

  local workers_per_core=1
  local cores
  cores=$(nproc --all)
  local recommended_workers=$((workers_per_core * cores))

  # The current value of alb.ingress.kubernetes.io/load-balancer-attributes
  local load_balancer_timeout=60
  # We must wait a little longer to let the load balancer close the connection first
  # https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#connection-idle-timeout
  local keep_alive_timeout=$((load_balancer_timeout + 5))

  local config
  local common_config=(
    # The TCP host/address to bind to
    --bind "${HOST}:${PORT}"
    # Path to the hypercorn config file
    --config 'python:settings.hypercorn'
    # Time to wait after SIGTERM or Ctrl-C for any remaining requests
    --graceful-timeout 45
    # Seconds to keep inactive connections alive before closing. [5]
    --keep-alive "${keep_alive_timeout}"
    # The type of workers to use. [asyncio]
    --worker-class 'uvloop'
  )

  local local_config=(
    "${common_config[@]}"
    # SSL certificate file
    --certfile=__argCertsDevelopment__/cert.crt
    # Enable debug mode, i.e. extra logging and checks
    --debug
    # SSL key file
    --keyfile=__argCertsDevelopment__/cert.key
    # Enable automatic reloads on code changes
    --reload
    # The number of worker processes for handling requests
    --workers 1
  )

  local k8s_config=(
    "${common_config[@]}"
    # The host:port of the statsd server
    --statsd-host "adot-collector.kube-system:8125"
    # The number of worker processes for handling requests
    --workers "${recommended_workers}"
  )

  source __argIntegratesBackEnv__/template "${env}" \
    && case "${DAEMON-}" in
      # The granularity of Error log outputs. [info]
      true) export LOG_LEVEL_CONSOLE="ERROR" ;;
      *) export LOG_LEVEL_CONSOLE="INFO" ;;
    esac \
    && case "${env}" in
      dev | prod-local)
        config=("${local_config[@]}")
        ;;
      eph | prod)
        export prometheus_multiproc_dir \
          && prometheus_multiproc_dir="$(mktemp -d)" \
          && config=("${k8s_config[@]}")
        ;;
      *)
        error 'First argument must be one of: dev, eph, prod, prod-local'
        ;;
    esac \
    && pushd integrates/back/src \
    && kill_port "${PORT}" \
    && { hypercorn "${config[@]}" 'app.app:APP' & } \
    && wait_port 20 "${HOST}:${PORT}" \
    && done_port "${HOST}" 28001 \
    && info Back is ready \
    && wait \
    && popd \
    || return 1
}

function serve_daemon {
  kill_port 28001 \
    && { serve "${@}" & } \
    && wait_port 300 localhost:28001
}

function main {
  export HOST="${HOST:-0.0.0.0}"
  export PORT="${PORT:-8001}"
  export DAEMON="${DAEMON:-false}"

  case "${DAEMON-}" in
    true) serve_daemon "${@}" ;;
    *) serve "${@}" ;;
  esac
}

main "${@}"
