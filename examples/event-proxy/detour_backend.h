#ifndef DARKAGES_EVENT_PROXY_DETOUR_BACKEND_H
#define DARKAGES_EVENT_PROXY_DETOUR_BACKEND_H

/*
 * Supply these functions with a tested 32-bit x86 trampoline library.
 * The backend must relocate complete instructions and return a callable
 * trampoline through original_function.
 */
int proxy_detour_attach(
    void *target,
    void *replacement,
    void **original_function);

int proxy_detour_detach(
    void *target,
    void *replacement);

#endif
