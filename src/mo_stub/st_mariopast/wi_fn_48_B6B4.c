void* fn_48_B6B4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 23) + i;
    if (idx >= 205) idx -= 205;
    return (char*)p + idx * 104 + 12;
}
