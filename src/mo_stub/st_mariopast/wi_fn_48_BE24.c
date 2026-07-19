void* fn_48_BE24(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 19) idx -= 19;
    return (char*)p + idx * 56 + 12;
}
