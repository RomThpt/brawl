void* fn_48_B77C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 58) idx -= 58;
    return (char*)p + idx * 160 + 12;
}
