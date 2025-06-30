package enterprise.policy
default allow = false
default reason = "Not allowed"
allow {
    input.user == "admin"
}
allow {
    input.user == "service1"
    input.action == "fetch_data"
    startswith(input.metadata.trace_time, "2025-07-")
}
reason := "Forbidden dataset requested" {
    input.parameters.dataset == "secret"
}
