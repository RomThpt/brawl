void* fn_27_1AF7C4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 301) idx -= 301;
    return (char*)p + idx * 4 + 12;
}
