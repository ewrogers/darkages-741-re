# CPU affinity

The matching client does not restrict itself to one CPU core. The single-core mask seen in the local installation comes from the optional `cnc-ddraw` compatibility wrapper beside the executable.

This distinction matters because changing `Darkages.exe` is unnecessary. The wrapper already has a setting that selects between CPU 0 and the available system mask.

## Source of the mask

`Darkages.exe` imports `DDRAW.dll`, but it does not import `SetProcessAffinityMask`, `GetProcessAffinityMask`, `SetThreadAffinityMask`, or another affinity setter. It also has no PE load-configuration directory that could supply an affinity mask before its entry point.

The local `ddraw.dll` identifies itself as [cnc-ddraw](https://github.com/FunkyFr3sh/cnc-ddraw). It imports both process-affinity functions. Its global `[ddraw]` configuration contains:

```ini
singlecpu=true
```

The wrapper describes this as a compatibility option that forces CPU 0. The local wrapper has SHA-256 `85e0f7d530dfda134793a57cb3e76b0287dcc96892ee57162dd68f47283b03a9`. This hash is installation context, not part of the version-741 client fingerprint.

## Startup order

The affinity change happens later than DLL loading but still during application startup:

```text
Windows loads the application-directory ddraw.dll
  |
  +-- cnc-ddraw DllMain reads ddraw.ini
  |
Darkages app_initialize
  |
  +-- open the Miles digital audio driver
  +-- create the sound-effect and music players
  +-- create the video system
        |
        +-- DirectDrawCreate
              |
              +-- cnc-ddraw creates its first DirectDraw object
              +-- apply the configured process affinity
```

`audio_miles_driver_ctor` starts Miles and opens the 22,050 Hz, 16-bit, stereo driver before `render_video_system_initialize` reaches `DirectDrawCreate`.

The local wrapper machine code calls `SetProcessAffinityMask` from its first-object initialization. Source from the matching build period shows the decision plainly:

```c
if (singlecpu) {
    SetProcessAffinityMask(process, 1);
} else if (GetProcessAffinityMask(process, &current, &system)) {
    SetProcessAffinityMask(process, system);
}
```

The source comparison is supporting context from cnc-ddraw commit [`2090c390`](https://github.com/FunkyFr3sh/cnc-ddraw/blob/2090c390b9f86782514c82d6e53949503c5f5a56/src/dd.c#L1821-L1836). The call and constants were checked independently in the local wrapper.

## Why early changes appear to fail

An external affinity change made immediately after process creation occurs before `DirectDrawCreate`. With `singlecpu=true`, cnc-ddraw later overwrites that choice with mask `1`. Changing the mask after video initialization appears to work because the wrapper applies this setting only while creating its first DirectDraw object.

Set `singlecpu=false` under the global `[ddraw]` section instead of racing startup. In this wrapper version, false does more than leave the inherited mask unchanged. It reads the system mask and applies that full mask when DirectDraw starts.

Per-game sections later in `ddraw.ini` do not apply to `Darkages.exe` unless a matching executable-name section exists. The local file has no Dark Ages override, so the global value is active.

## Expected effects

Allowing all available cores does not make the main game loop parallel. Most client state, input, packet handling, and rendering still run on the main thread. It does allow Windows to schedule the wrapper, Miles, and other helper threads on different processors.

No checked client path requires process mask `1`, and the client does not read the current affinity mask. Running on all cores is therefore compatible with the client behavior recovered so far. The practical risks come from old middleware or compatibility code with timing-sensitive cross-thread behavior, not from an explicit client requirement. Watch for rendering stalls, audio breakup, unusually fast or slow pacing, and shutdown hangs when testing a different mask.

## Audio observations

The normal cnc-ddraw affinity change occurs after the Miles driver opens. It cannot explain an initial Miles open failure in the ordinary startup order. Widening the mask later also does not reopen a failed driver.

If silent audio begins immediately after widening the mask, that instead suggests an already-open Miles worker was not receiving enough scheduling time on CPU 0. This remains a runtime hypothesis. Check whether the Miles driver pointer is non-null before and after the change to distinguish a failed open from a stalled playback path.

Audio levels are an independent cause. `Darkages.cfg` values of `0` mute their corresponding music or sound path. Verify both saved levels are nonzero before comparing affinity runs.

## Known limit

This page explains the local compatibility wrapper and the target client's interaction with it. A client installation that uses the Windows system `ddraw.dll`, a different wrapper build, or different wrapper settings may not change affinity at all.
