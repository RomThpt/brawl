void* fn_27_1BF0D8(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 26) + i;
    if (idx >= 17) idx -= 17;
    return (char*)p + idx * 12 + 28;
}
