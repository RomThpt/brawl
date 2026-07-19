void* fn_27_1AFF1C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 26) idx -= 26;
    return (char*)p + idx * 4 + 12;
}
