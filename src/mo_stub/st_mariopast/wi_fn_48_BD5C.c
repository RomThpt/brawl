void* fn_48_BD5C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 19) idx -= 19;
    return (char*)p + idx * 160 + 12;
}
