# Motion effect table

`meffect.tbl` defines how a moving visual effect travels between two points. A motion row can use fixed numeric parameters or compile small expressions that are evaluated while the effect is created.

The file is structured text, not a generic TBL layout. The loader reads the table as a sequence of records and stores at most 256 motion definitions.

## Motion modes

Each record selects one of two named modes:

| Mode token | Client behavior |
| --- | --- |
| `distance` | Uses numeric distance-related fields directly. |
| `time` | Compiles expression fields and evaluates them from the current distance and time values. |

The complete meaning of every numeric column is not yet established. Preserve unknown columns and record order when editing this file.

## Expression fields

An expression field begins with `%`. The loader passes its tokens to `expression_context_compile` and stores the returned handle in the motion record. A record has four expression groups, with room for five handles in each group.

The compiler supports these tokens:

| Kind | Tokens |
| --- | --- |
| Arithmetic | `+`, `-`, `*`, `/` |
| Comparison | `=`, `<`, `>` |
| Boolean | `!`, `&`, `|` |
| Conditional | `? :` |
| Grouping | `( )` |
| Numeric literal | Decimal digits with at most one period |
| Numeric variable | One byte |
| Boolean variable | `_` followed by one byte |

`=` is equality, not assignment. Boolean AND and OR short-circuit. The conditional operator evaluates only its selected branch.

The motion-effect contexts register three numeric variables:

| Variable | Observed value |
| --- | --- |
| `d` | Source-to-target distance before the total-time expression is evaluated |
| `T` | Evaluated total motion time |
| `t` | Current sample time while the path points are generated |

No Boolean variables are registered for the motion table, even though the reusable expression compiler supports them.

## Compile and evaluation flow

```text
meffect.tbl expression text
        |
        v
token callback -> expression_context_compile
        |
        v
typed expression tree -> integer handle stored in motion record
        |
        v
set d, T, or t -> expression_context_evaluate(handle)
```

The context owns every expression node. A failed compile keeps new nodes on pending lists so they can be destroyed without disturbing previously compiled expressions. A successful compile moves them into the retained ownership lists.

## Known limits

- The context stores up to 1,024 compiled expression roots.
- Variable lookup is indexed by one byte.
- The operator table contains exactly 14 tokens.
- The loader reserves 256 motion-definition records.
- The full row grammar and all numeric field meanings remain incomplete.

## Evidence

- `file_load_motion_effect_table` compiles the four expression groups from `meffect.tbl`.
- `expression_context_compile` builds the typed expression tree.
- `expression_context_set_numeric_variable` receives `d`, `T`, and `t` from the motion-effect creation path.
- `expression_context_evaluate` evaluates the stored root by handle.
- The deterministic function map is in [`analysis/exports/expressions.yaml`](../../analysis/exports/expressions.yaml).
