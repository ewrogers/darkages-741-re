"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const { searchFunctions } = require("../../theme/function-lookup.js");

function record(name, address, extra = {}) {
    return {
        name, address, rva: "0x00001234", group: "Events", conflict: false,
        url: "functions/events.html#" + name + "-" + address,
        ...extra,
    };
}

test("exact names rank before prefixes and substrings, without losing duplicate names", () => {
    const records = [
        record("ui_event_dispatch", "0x00401234"),
        record("event_dispatch_now", "0x00401235"),
        record("event_dispatch", "0x00401237", { conflict: true }),
        record("event_dispatch", "0x00401236", { conflict: true }),
    ];
    const found = searchFunctions(records, "EVENT_DISPATCH");
    assert.deepEqual(found.results.map(row => row.address), ["0x00401236", "0x00401237", "0x00401235", "0x00401234"]);
    assert.equal(found.total, 4);
    assert.equal(found.results[0].conflict, true);
});

test("static address normalization retains every name at that address", () => {
    const records = [record("second_name", "0x00401234"), record("first_name", "0x00401234")];
    for (const query of ["0x00401234", "401234", "000000401234", "0X401234"]) {
        const found = searchFunctions(records, query);
        assert.deepEqual(found.results.map(row => row.name), ["first_name", "second_name"]);
    }
});

test("RVA matching is explicit and never silently treats a static address as an RVA", () => {
    const records = [record("event_dispatch", "0x00401234")];
    assert.equal(searchFunctions(records, "1234").total, 0);
    assert.equal(searchFunctions(records, "RVA: 0X00001234").total, 1);
    assert.equal(searchFunctions(records, "rva:1234").total, 1);
    assert.equal(searchFunctions(records, "rva:401234").total, 0);
    assert.equal(searchFunctions(records, "rva:bogus").invalidRva, true);
});

test("exact static addresses rank before a partial name that contains those digits", () => {
    const records = [record("401234_helper", "0x00405678"), record("target", "0x00401234")];
    assert.equal(searchFunctions(records, "401234").results[0].name, "target");
});

test("the displayed limit does not hide the total and exact matches survive truncation", () => {
    const records = Array.from({ length: 80 }, (_, index) => record("event_" + index, "0x00401234"));
    records.push(record("event", "0x00401235"));
    const found = searchFunctions(records, "event");
    assert.equal(found.total, 81);
    assert.equal(found.results.length, 50);
    assert.equal(found.results[0].name, "event");
    assert.equal(searchFunctions(records, "event", 3).results.length, 3);
    assert.equal(searchFunctions(records, "event", 100).results.length, 50);
});

test("empty, unmatched, and oversized address queries return no accidental matches", () => {
    const records = [record("event_dispatch", "0x00401234")];
    for (const query of ["", "   ", "missing_function", "rva:0x100000000"]) {
        assert.equal(searchFunctions(records, query).total, 0);
    }
});

test("search treats punctuation as literal text and does not mutate source records", () => {
    const records = Object.freeze([Object.freeze(record("event[one]", "0x00401234"))]);
    assert.equal(searchFunctions(records, "[one]").total, 1);
    assert.equal(searchFunctions(records, ".*").total, 0);
    assert.equal(searchFunctions(records, "event").results[0], records[0]);
});
