void* fn_48_B48C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 23) + i;
    if (idx >= 205) idx -= 205;
    return (char*)p + idx * 160 + 12;
}
