void* fn_27_1AFC4C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 314) idx -= 314;
    return (char*)p + idx * 4 + 12;
}
