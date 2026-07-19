void* fn_27_295F94(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 29) + i;
    if (idx >= 2) idx -= 2;
    return (char*)p + idx * 12 + 12;
}
