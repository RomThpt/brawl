extern int fn_110_1F21C();
extern int fn_110_1F400();
extern int fn_110_1F278();

int fn_110_20FD0(void* p) {
    return fn_110_1F21C((char*)p + (-100));
}

int fn_110_20FD8(void* p) {
    return fn_110_1F400((char*)p + (-184));
}

int fn_110_20FE0(void* p) {
    return fn_110_1F278((char*)p + (-232));
}
