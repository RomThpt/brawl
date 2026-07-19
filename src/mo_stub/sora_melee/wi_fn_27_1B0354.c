void* fn_27_1B0354(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 17) idx -= 17;
    return (char*)p + idx * 96 + 12;
}
