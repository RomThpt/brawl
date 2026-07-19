void* fn_48_B844(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 58) idx -= 58;
    return (char*)p + idx * 56 + 12;
}
