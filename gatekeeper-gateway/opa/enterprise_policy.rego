package enterprise.policy

default allow := false
default deny_reason := "Not allowed"

# Use older syntax without 'if' keyword
allow {
    input.user == "admin"
}

allow {
    input.user == "service1"
    input.action == "fetch_data"
    input.metadata.trace_id  # Just check if trace_id exists
    input.parameters.dataset != "secret"
}
deny_reason := "Forbidden dataset requested" {
    not allow
    input.parameters.dataset == "secret"
}