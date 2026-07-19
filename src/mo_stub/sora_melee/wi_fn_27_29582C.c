void* fn_27_29582C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 16) idx -= 16;
    return (char*)p + idx * 4 + 12;
}
