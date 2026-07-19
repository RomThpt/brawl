void* fn_48_BF84(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 19) idx -= 19;
    return (char*)p + idx * 104 + 12;
}
