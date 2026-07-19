void* fn_27_1C855C(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 26) + i;
    if (idx >= 17) idx -= 17;
    return (char*)p + idx * 12 + 28;
}
