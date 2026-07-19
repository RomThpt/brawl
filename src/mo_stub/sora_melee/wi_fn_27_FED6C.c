void* fn_27_FED6C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 22) idx -= 22;
    return (char*)p + idx * 12 + 12;
}
