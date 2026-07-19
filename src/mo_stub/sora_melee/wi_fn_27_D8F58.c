void* fn_27_D8F58(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 10) idx -= 10;
    return (char*)p + idx * 4 + 12;
}
