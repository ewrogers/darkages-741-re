# Bulletin abuse warning list

Privileged bulletin tools keep a small local history of abuse warnings issued to users. The client uses this history to decide whether a selected user can receive another queued warning and to choose the next warning level.

The file is local to the current character:

```text
banglist<character>.txt
```

`<character>` is the current character name with ASCII spaces removed. The removal loop is DBCS-aware, so a trail byte whose value happens to be `0x20` is preserved. The client opens the file for read/write and creates it when it does not exist.

## Records

The file has no header or record count. Each record is 45 bytes:

```text
record BulletinBangUser {
    bytes marker[1]          // ASCII "-"
    bytes user_name[32]     // text followed by ASCII "-" padding
    bytes warning_count[1]  // one ASCII decimal digit
    bytes warning_date[9]   // zero-padded ASCII decimal YYYYMMDD
    bytes newline[2]        // CR LF
}
```

The first record begins at offset zero and later records follow immediately. A new record starts as:

```text
-<32-byte padded user name>0000000000\r\n
```

The ten zeros are one warning-count digit followed by the nine-byte date field. A normal eight-digit date therefore has one leading zero in storage.

## Lookup and update

`file_bulletin_bang_find_or_append_user_record` scans for the marker, reads the next 32 bytes, and compares the complete padded name. A missing user is appended and the file position is moved back to the numeric fields.

When a warning job runs, the client:

1. increments the count and caps it at `8`;
2. writes the single count digit in place;
3. writes the current UTC date as nine decimal bytes;
4. sends the warning commands selected for that level.

`BulletinBangUserBatchSession` also keeps an in-memory map from user name to date while one multi-selection batch runs. This prevents duplicate selected rows from producing duplicate work.

## Known limits

- Character and user names are treated as client text bytes, not Unicode.
- The stored user field is exactly 32 bytes and is compared including its `-` padding.
- The reader accepts the first count byte without validating that it is an ASCII digit.
- The date comes from `GetSystemTime`, so it follows UTC rather than local time.
- No code here proves that another client version uses the same file layout.
