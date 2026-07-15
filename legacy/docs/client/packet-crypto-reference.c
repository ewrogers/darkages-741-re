/*
 * Reference reconstruction from the version-741 client.
 *
 * This is not recovered source code. Names describe observed behavior.
 * The caller supplies a standard MD5 function so this file can focus on the
 * client-specific packet logic without embedding a second crypto library.
 */

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

#define NULL ((void *)0)

static void copy_bytes(u8 *destination, const u8 *source, u32 length)
{
    u32 i;

    for (i = 0; i < length; ++i) {
        destination[i] = source[i];
    }
}

typedef void (*packet_md5_fn)(
    const u8 *data,
    u32 length,
    u8 digest[16]);

enum packet_crypto_mode {
    PACKET_CRYPTO_RAW = 0,
    PACKET_CRYPTO_PRIMARY_KEY = 1,
    PACKET_CRYPTO_DERIVED_KEY = 2
};

enum packet_result {
    PACKET_OK = 0,
    PACKET_BAD_ARGUMENT = -1,
    PACKET_BUFFER_TOO_SMALL = -2,
    PACKET_BAD_DATA = -3
};

struct map_crc_record {
    u16 a;
    u16 b;
    u16 c;
};

const u8 packet_default_primary_key[9] = {
    'U', 'r', 'k', 'c', 'n', 'I', 't', 'n', 'I'
};

static void digest_to_hex(const u8 digest[16], u8 output[32])
{
    static const u8 hex[] = "0123456789abcdef";
    u32 i;

    for (i = 0; i < 16; ++i) {
        output[i * 2] = hex[digest[i] >> 4];
        output[i * 2 + 1] = hex[digest[i] & 0x0f];
    }
}

int packet_frame(
    const u8 *body,
    u32 body_length,
    u8 *output,
    u32 output_capacity,
    u32 *output_length)
{
    if (body == NULL || output == NULL || output_length == NULL) {
        return PACKET_BAD_ARGUMENT;
    }
    if (body_length > 0xffff) {
        return PACKET_BAD_DATA;
    }
    if (output_capacity < body_length + 3) {
        return PACKET_BUFFER_TOO_SMALL;
    }

    output[0] = 0xaa;
    output[1] = (u8)(body_length >> 8);
    output[2] = (u8)body_length;
    copy_bytes(output + 3, body, body_length);
    *output_length = body_length + 3;
    return PACKET_OK;
}

int packet_build_key_table(
    const u8 *seed,
    u32 seed_length,
    packet_md5_fn md5,
    u8 output[1024])
{
    u8 digest[16];
    u8 inner_hex[32];
    u32 length;
    int round;

    if (seed == NULL || md5 == NULL || output == NULL) {
        return PACKET_BAD_ARGUMENT;
    }

    md5(seed, seed_length, digest);
    digest_to_hex(digest, inner_hex);

    md5(inner_hex, sizeof(inner_hex), digest);
    digest_to_hex(digest, output);
    length = 32;

    for (round = 0; round < 31; ++round) {
        md5(output, length, digest);
        digest_to_hex(digest, output + length);
        length += 32;
    }

    return PACKET_OK;
}

void packet_derive_key(
    const u8 key_table[1024],
    u16 seed16,
    u8 seed8,
    u8 output[9])
{
    u32 seed8_squared;
    u32 i;

    seed8_squared = (u32)seed8 * seed8;
    for (i = 0; i < 9; ++i) {
        u32 index;

        index = seed16 + (seed8_squared + 9 * i) * i;
        output[i] = key_table[index & 0x3ff];
    }
}

void packet_generate_seeds(u32 random_value, u16 *seed16, u8 *seed8)
{
    *seed16 = (u16)(((random_value & 0xffff) % 0xfefd) + 0x0100);
    *seed8 = (u8)((((random_value & 0x00ff0000) >> 16) % 0x9b) + 0x64);
}

int packet_build_salt_table(u8 seed, u8 output[256])
{
    int i;

    if (output == NULL || seed > 9) {
        return PACKET_BAD_ARGUMENT;
    }

    for (i = 0; i < 256; ++i) {
        int value;

        switch (seed) {
        case 0:
            value = i;
            break;
        case 1:
            value = 0x80 + ((i + 1) / 2) * ((i & 1) == 0 ? 1 : -1);
            break;
        case 2:
            value = 0xff - i;
            break;
        case 3:
            value = 0x80 + ((0xff - i) / 2) * ((i & 1) == 0 ? 1 : -1);
            break;
        case 4:
            value = (i / 16) * (i / 16);
            break;
        case 5:
            value = (i * 2) & 0xff;
            break;
        case 6:
            value = 0xff - ((i * 2) & 0xff);
            break;
        case 7:
            value = i <= 0x7f ? 0xff - i * 2 : i * 2 - 0x100;
            break;
        case 8:
            value = i <= 0x7f ? i * 2 : 0x1ff - i * 2;
            break;
        default:
        {
            int quotient;

            quotient = (i - 0x80) / 8;
            value = 0xff - ((quotient * quotient) & 0xff);
            break;
        }
        }

        output[i] = (u8)value;
    }

    return PACKET_OK;
}

void packet_apply_common_xor(
    u8 *data,
    u32 data_length,
    const u8 *selected_key,
    u32 selected_key_length,
    u32 block_size,
    u8 ordinal,
    const u8 salt_table[256])
{
    u32 block_count;
    u32 block;
    u32 i;

    for (i = 0; i < data_length; ++i) {
        data[i] ^= selected_key[i % selected_key_length];
    }

    block_count = (data_length + block_size - 1) / block_size;
    for (block = 0; block < block_count; ++block) {
        u8 block_byte;
        u32 start;
        u32 end;

        block_byte = (u8)block;
        if (block_byte == ordinal) {
            continue;
        }

        start = block * block_size;
        end = start + block_size;
        if (end > data_length) {
            end = data_length;
        }

        for (i = start; i < end; ++i) {
            data[i] ^= salt_table[block_byte];
        }
    }

    for (i = 0; i < data_length; ++i) {
        data[i] ^= salt_table[ordinal];
    }
}

void packet_build_crc_table(u16 output[256])
{
    int i;

    for (i = 0; i < 256; ++i) {
        u32 crc;
        int bit;

        crc = (u32)i << 8;
        for (bit = 0; bit < 8; ++bit) {
            if ((crc & 0x8000) != 0) {
                crc = ((crc << 1) ^ 0x1021) & 0xffff;
            } else {
                crc = (crc << 1) & 0xffff;
            }
        }
        output[i] = (u16)crc;
    }
}

u16 packet_crc16_update(const u16 table[256], u8 value, u16 crc)
{
    return (u16)(table[crc >> 8] ^ (u16)(crc << 8) ^ value);
}

u16 packet_crc16(const u16 table[256], const u8 *data, u32 length)
{
    u16 crc;
    u32 i;

    crc = 0;
    for (i = 0; i < length; ++i) {
        crc = packet_crc16_update(table, data[i], crc);
    }
    return crc;
}

u16 packet_reply_crc16(const u16 table[256], u16 server_challenge)
{
    u16 crc;

    crc = packet_crc16_update(table, (u8)server_challenge, 0);
    return packet_crc16_update(table, (u8)(server_challenge >> 8), crc);
}

static u16 feed_little_endian_word(
    const u16 table[256],
    u16 crc,
    u16 value)
{
    crc = packet_crc16_update(table, (u8)value, crc);
    return packet_crc16_update(table, (u8)(value >> 8), crc);
}

u16 packet_map_crc16(
    const u16 table[256],
    const struct map_crc_record *records,
    u32 record_count)
{
    u16 crc;
    u32 i;

    crc = 0;
    for (i = 0; i < record_count; ++i) {
        crc = feed_little_endian_word(table, crc, records[i].a);
        crc = feed_little_endian_word(table, crc, records[i].b);
        crc = feed_little_endian_word(table, crc, records[i].c);
    }
    return crc;
}

int packet_wrap_dialog(
    const u16 crc_table[256],
    const u8 *builder_body,
    u32 builder_length,
    u8 random1,
    u8 random2,
    u8 *output,
    u32 output_capacity,
    u32 *output_length)
{
    u32 protected_length;
    u16 crc;
    u32 i;

    if (crc_table == NULL || builder_body == NULL || output == NULL ||
        output_length == NULL || builder_length < 1) {
        return PACKET_BAD_ARGUMENT;
    }

    protected_length = builder_length + 1;
    if (protected_length > 0xffff) {
        return PACKET_BAD_DATA;
    }
    if (output_capacity < builder_length + 7) {
        return PACKET_BUFFER_TOO_SMALL;
    }

    output[0] = builder_body[0];
    output[1] = random1;
    output[2] = (u8)((random1 + 0xd3) ^ random2);
    output[3] = (u8)((protected_length >> 8) ^ (u8)(random2 + 0x72));
    output[4] = (u8)(protected_length ^ (u8)(random2 + 0x73));

    crc = packet_crc16(crc_table, builder_body + 1, builder_length - 1);
    output[5] = (u8)(crc >> 8);
    output[6] = (u8)crc;
    copy_bytes(output + 7, builder_body + 1, builder_length - 1);

    for (i = 0; i < protected_length; ++i) {
        output[5 + i] ^= (u8)(random2 + 0x28 + i);
    }

    output[builder_length + 6] = 0;
    *output_length = builder_length + 7;
    return PACKET_OK;
}

int packet_unwrap_dialog(
    const u16 crc_table[256],
    const u8 *wrapped_body,
    u32 wrapped_length,
    u8 *output,
    u32 output_capacity,
    u32 *output_length,
    int *crc_valid)
{
    u8 random1;
    u8 random2;
    u32 protected_length;
    u32 payload_length;
    u16 expected_crc;
    u32 i;

    if (crc_table == NULL || wrapped_body == NULL || output == NULL ||
        output_length == NULL || crc_valid == NULL) {
        return PACKET_BAD_ARGUMENT;
    }
    if (wrapped_length < 8) {
        return PACKET_BAD_DATA;
    }

    random1 = wrapped_body[1];
    random2 = (u8)(wrapped_body[2] ^ (u8)(random1 + 0xd3));
    protected_length =
        ((u32)(wrapped_body[3] ^ (u8)(random2 + 0x72)) << 8) |
        (wrapped_body[4] ^ (u8)(random2 + 0x73));

    if (protected_length < 2 || 5 + protected_length > wrapped_length) {
        return PACKET_BAD_DATA;
    }

    payload_length = protected_length - 2;
    if (output_capacity < payload_length + 1) {
        return PACKET_BUFFER_TOO_SMALL;
    }

    expected_crc = (u16)(
        ((u16)(wrapped_body[5] ^ (u8)(random2 + 0x28)) << 8) |
        (wrapped_body[6] ^ (u8)(random2 + 0x29)));

    output[0] = wrapped_body[0];
    for (i = 0; i < payload_length; ++i) {
        output[1 + i] =
            wrapped_body[7 + i] ^ (u8)(random2 + 0x2a + i);
    }

    *output_length = payload_length + 1;
    *crc_valid =
        packet_crc16(crc_table, output + 1, payload_length) == expected_crc;
    return PACKET_OK;
}

int packet_prepare_submitted_body(
    const u16 crc_table[256],
    const u8 *builder_body,
    u32 builder_length,
    u8 dialog_random1,
    u8 dialog_random2,
    u8 *output,
    u32 output_capacity,
    u32 *output_length)
{
    if (builder_body == NULL || builder_length < 1 || output == NULL ||
        output_length == NULL) {
        return PACKET_BAD_ARGUMENT;
    }

    if (builder_body[0] == 0x39 || builder_body[0] == 0x3a) {
        return packet_wrap_dialog(
            crc_table,
            builder_body,
            builder_length,
            dialog_random1,
            dialog_random2,
            output,
            output_capacity,
            output_length);
    }

    if (output_capacity < builder_length + 1) {
        return PACKET_BUFFER_TOO_SMALL;
    }
    copy_bytes(output, builder_body, builder_length);
    output[builder_length] = 0;
    *output_length = builder_length + 1;
    return PACKET_OK;
}

int packet_encrypt_client_body(
    const u8 *prepared_body,
    u32 prepared_length,
    enum packet_crypto_mode mode,
    u8 *sequence,
    const u8 *primary_key,
    u32 primary_key_length,
    const u8 key_table[1024],
    u32 random_value,
    u8 salt_table_seed,
    packet_md5_fn md5,
    u8 *output,
    u32 output_capacity,
    u32 *output_length)
{
    u8 salt_table[256];
    u8 derived_key[9];
    const u8 *selected_key;
    u32 selected_key_length;
    u32 cipher_length;
    u32 required_length;
    u16 seed16;
    u8 seed8;
    u8 ordinal;
    u8 digest[16];
    u32 digest_offset;
    u32 trailer_offset;

    if (prepared_body == NULL || prepared_length < 1 || output == NULL ||
        output_length == NULL) {
        return PACKET_BAD_ARGUMENT;
    }

    if (mode == PACKET_CRYPTO_RAW) {
        if (output_capacity < prepared_length) {
            return PACKET_BUFFER_TOO_SMALL;
        }
        copy_bytes(output, prepared_body, prepared_length);
        *output_length = prepared_length;
        return PACKET_OK;
    }

    if (sequence == NULL || primary_key == NULL || primary_key_length == 0 ||
        md5 == NULL || salt_table_seed > 9) {
        return PACKET_BAD_ARGUMENT;
    }
    if (mode != PACKET_CRYPTO_PRIMARY_KEY &&
        mode != PACKET_CRYPTO_DERIVED_KEY) {
        return PACKET_BAD_ARGUMENT;
    }
    if (mode == PACKET_CRYPTO_DERIVED_KEY && key_table == NULL) {
        return PACKET_BAD_ARGUMENT;
    }

    cipher_length = prepared_length - 1;
    required_length = 2 + cipher_length + 4 + 3;
    if (output_capacity < required_length) {
        return PACKET_BUFFER_TOO_SMALL;
    }

    packet_generate_seeds(random_value, &seed16, &seed8);
    packet_build_salt_table(salt_table_seed, salt_table);

    if (mode == PACKET_CRYPTO_DERIVED_KEY) {
        packet_derive_key(key_table, seed16, seed8, derived_key);
        selected_key = derived_key;
        selected_key_length = sizeof(derived_key);
    } else {
        selected_key = primary_key;
        selected_key_length = primary_key_length;
    }

    ordinal = *sequence;
    *sequence = (u8)(ordinal + 1);

    output[0] = prepared_body[0];
    output[1] = ordinal;
    copy_bytes(output + 2, prepared_body + 1, cipher_length);
    packet_apply_common_xor(
        output + 2,
        cipher_length,
        selected_key,
        selected_key_length,
        primary_key_length,
        ordinal,
        salt_table);

    digest_offset = 2 + cipher_length;
    md5(output, digest_offset, digest);
    output[digest_offset] = digest[13];
    output[digest_offset + 1] = digest[3];
    output[digest_offset + 2] = digest[11];
    output[digest_offset + 3] = digest[7];

    trailer_offset = digest_offset + 4;
    output[trailer_offset] = (u8)((seed16 & 0xff) ^ 0x70);
    output[trailer_offset + 1] = (u8)(seed8 ^ 0x23);
    output[trailer_offset + 2] = (u8)((seed16 >> 8) ^ 0x74);

    *output_length = required_length;
    return PACKET_OK;
}

int packet_decrypt_server_body(
    const u8 *encrypted_body,
    u32 encrypted_length,
    enum packet_crypto_mode mode,
    const u8 *primary_key,
    u32 primary_key_length,
    const u8 key_table[1024],
    u8 salt_table_seed,
    u8 *output,
    u32 output_capacity,
    u32 *output_length)
{
    u8 salt_table[256];
    u8 derived_key[9];
    const u8 *selected_key;
    u32 selected_key_length;
    u32 cipher_length;
    u8 ordinal;
    u8 seed_low;
    u8 seed8;
    u8 seed_high;
    u16 seed16;

    if (encrypted_body == NULL || encrypted_length < 1 || output == NULL ||
        output_length == NULL) {
        return PACKET_BAD_ARGUMENT;
    }

    if (mode == PACKET_CRYPTO_RAW) {
        if (output_capacity < encrypted_length) {
            return PACKET_BUFFER_TOO_SMALL;
        }
        copy_bytes(output, encrypted_body, encrypted_length);
        *output_length = encrypted_length;
        return PACKET_OK;
    }

    if (encrypted_length < 5 || primary_key == NULL ||
        primary_key_length == 0 || salt_table_seed > 9) {
        return PACKET_BAD_DATA;
    }
    if (mode != PACKET_CRYPTO_PRIMARY_KEY &&
        mode != PACKET_CRYPTO_DERIVED_KEY) {
        return PACKET_BAD_ARGUMENT;
    }
    if (mode == PACKET_CRYPTO_DERIVED_KEY && key_table == NULL) {
        return PACKET_BAD_ARGUMENT;
    }

    cipher_length = encrypted_length - 5;
    if (output_capacity < cipher_length + 1) {
        return PACKET_BUFFER_TOO_SMALL;
    }

    ordinal = encrypted_body[1];
    seed_low = encrypted_body[encrypted_length - 3] ^ 0x74;
    seed8 = encrypted_body[encrypted_length - 2] ^ 0x24;
    seed_high = encrypted_body[encrypted_length - 1] ^ 0x64;
    seed16 = (u16)(((u16)seed_high << 8) | seed_low);

    packet_build_salt_table(salt_table_seed, salt_table);
    if (mode == PACKET_CRYPTO_DERIVED_KEY) {
        packet_derive_key(key_table, seed16, seed8, derived_key);
        selected_key = derived_key;
        selected_key_length = sizeof(derived_key);
    } else {
        selected_key = primary_key;
        selected_key_length = primary_key_length;
    }

    output[0] = encrypted_body[0];
    copy_bytes(output + 1, encrypted_body + 2, cipher_length);
    packet_apply_common_xor(
        output + 1,
        cipher_length,
        selected_key,
        selected_key_length,
        primary_key_length,
        ordinal,
        salt_table);

    *output_length = cipher_length + 1;
    return PACKET_OK;
}
