#!/bin/sh
opa run --server --set=decision_logs.console=true --watch ./enterprise_policy.rego
