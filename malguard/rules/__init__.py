from .ast_rules import (
    detect,
    detect_command_injection_style_spawn,
    detect_dynamic_import_system,
    detect_env_exfiltration_via_http_post,
    detect_exec_on_decoded_payload,
    detect_exec_on_reconstructed_string,
    detect_high_entropy_code_execution,
    detect_pickle_loads_from_network_or_socket,
)

RULES = [
    detect_exec_on_decoded_payload,
    detect_high_entropy_code_execution,
    detect_dynamic_import_system,
    detect_pickle_loads_from_network_or_socket,
    detect_exec_on_reconstructed_string,
    detect_command_injection_style_spawn,
    detect_env_exfiltration_via_http_post,
]

__all__ = [
    "RULES",
    "detect",
    "detect_exec_on_decoded_payload",
    "detect_high_entropy_code_execution",
    "detect_dynamic_import_system",
    "detect_pickle_loads_from_network_or_socket",
    "detect_exec_on_reconstructed_string",
    "detect_command_injection_style_spawn",
    "detect_env_exfiltration_via_http_post",
]
