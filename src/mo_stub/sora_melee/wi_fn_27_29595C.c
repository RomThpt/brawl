void* fn_27_29595C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 31) idx -= 31;
    return (char*)p + idx * 4 + 12;
}
