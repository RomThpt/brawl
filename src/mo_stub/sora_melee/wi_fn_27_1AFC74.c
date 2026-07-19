void* fn_27_1AFC74(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 313) idx -= 313;
    return (char*)p + idx * 4 + 12;
}
