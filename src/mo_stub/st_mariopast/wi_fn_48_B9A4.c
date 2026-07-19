void* fn_48_B9A4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 58) idx -= 58;
    return (char*)p + idx * 104 + 12;
}
