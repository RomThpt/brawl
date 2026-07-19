void* fn_27_D94A8(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 27) idx -= 27;
    return (char*)p + idx * 48 + 12;
}
