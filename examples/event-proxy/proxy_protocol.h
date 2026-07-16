#ifndef DARKAGES_EVENT_PROXY_PROTOCOL_H
#define DARKAGES_EVENT_PROXY_PROTOCOL_H

#include <stdint.h>

#define PROXY_PROTOCOL_MAGIC 0x58504544u
#define PROXY_PROTOCOL_VERSION 1u
#define PROXY_MAX_PAYLOAD 1024u
#define PROXY_TEXT_CAPACITY 127u
#define PROXY_CAPTURE_CAPACITY 64u

enum proxy_message_kind {
    PROXY_COMMAND_POINTER = 1,
    PROXY_COMMAND_KEY = 2,
    PROXY_COMMAND_TEXT = 3,
    PROXY_COMMAND_APPLICATION = 4,
    PROXY_COMMAND_CLIENT_PACKET = 5,
    PROXY_COMMAND_SERVER_PACKET = 6,
    PROXY_COMMAND_SET_RULE = 7,
    PROXY_COMMAND_RESET_RULES = 8,
    PROXY_MESSAGE_TELEMETRY = 0x8001,
    PROXY_MESSAGE_STATUS = 0x8002
};

enum proxy_message_flag {
    PROXY_FLAG_BYPASS_RULES = 0x00000001u
};

enum proxy_pointer_action {
    PROXY_POINTER_MOVE = 0,
    PROXY_POINTER_LEFT_DOWN = 1,
    PROXY_POINTER_LEFT_UP = 2,
    PROXY_POINTER_RIGHT_DOWN = 3,
    PROXY_POINTER_RIGHT_UP = 4,
    PROXY_POINTER_WHEEL = 5
};

enum proxy_key_action {
    PROXY_KEY_DOWN = 0,
    PROXY_KEY_UP = 1
};

enum proxy_text_action {
    PROXY_TEXT_CHARACTER = 0,
    PROXY_TEXT_COMMITTED = 1
};

enum proxy_application_action {
    PROXY_APPLICATION_IME_OPEN_STATUS = 0,
    PROXY_APPLICATION_IME_COMPOSITION_START = 1,
    PROXY_APPLICATION_IME_COMPOSITION_END = 2,
    PROXY_APPLICATION_IME_CANDIDATE_CLOSE = 3
};

enum proxy_rule_domain {
    PROXY_RULE_EVENT_TYPE = 0,
    PROXY_RULE_CLIENT_OPCODE = 1,
    PROXY_RULE_SERVER_OPCODE = 2
};

enum proxy_rule_action {
    PROXY_RULE_ALLOW = 0,
    PROXY_RULE_OBSERVE = 1,
    PROXY_RULE_BLOCK = 2
};

enum proxy_telemetry_source {
    PROXY_SOURCE_CLIENT = 0,
    PROXY_SOURCE_INJECTED = 1
};

#pragma pack(push, 1)

typedef struct proxy_message_header {
    uint32_t magic;
    uint16_t version;
    uint16_t kind;
    uint32_t flags;
    uint32_t payload_size;
    uint32_t request_id;
} proxy_message_header;

typedef struct proxy_pointer_payload {
    uint8_t action;
    uint8_t reserved[3];
    int32_t x;
    int32_t y;
    int32_t wheel_delta;
    uint32_t message_time;
} proxy_pointer_payload;

typedef struct proxy_key_payload {
    uint8_t action;
    uint8_t scan_code;
    uint8_t composition_active;
    uint8_t reserved;
    uint32_t virtual_key;
    uint32_t message_time;
} proxy_key_payload;

typedef struct proxy_text_payload {
    uint8_t action;
    uint8_t reserved;
    uint16_t byte_length;
    uint32_t message_time;
    uint8_t bytes[PROXY_TEXT_CAPACITY];
} proxy_text_payload;

typedef struct proxy_application_payload {
    uint8_t action;
    uint8_t value;
    uint16_t reserved;
    uint32_t message_time;
} proxy_application_payload;

typedef struct proxy_rule_payload {
    uint8_t domain;
    uint8_t selector;
    uint8_t action;
    uint8_t reserved;
} proxy_rule_payload;

typedef struct proxy_telemetry_payload {
    uint8_t domain;
    uint8_t selector;
    uint8_t action;
    uint8_t source;
    uint32_t value0;
    uint32_t value1;
    uint32_t value2;
    uint32_t value3;
    uint16_t original_size;
    uint16_t captured_size;
    uint8_t captured[PROXY_CAPTURE_CAPACITY];
} proxy_telemetry_payload;

typedef struct proxy_wire_message {
    proxy_message_header header;
    uint8_t payload[PROXY_MAX_PAYLOAD];
} proxy_wire_message;

#pragma pack(pop)

typedef char proxy_assert_header_size[
    sizeof(proxy_message_header) == 20 ? 1 : -1];
typedef char proxy_assert_pointer_size[
    sizeof(proxy_pointer_payload) == 20 ? 1 : -1];
typedef char proxy_assert_key_size[
    sizeof(proxy_key_payload) == 12 ? 1 : -1];
typedef char proxy_assert_text_size[
    sizeof(proxy_text_payload) == 135 ? 1 : -1];
typedef char proxy_assert_application_size[
    sizeof(proxy_application_payload) == 8 ? 1 : -1];
typedef char proxy_assert_rule_size[
    sizeof(proxy_rule_payload) == 4 ? 1 : -1];
typedef char proxy_assert_telemetry_size[
    sizeof(proxy_telemetry_payload) == 88 ? 1 : -1];

#endif
