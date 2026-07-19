void* fn_27_D9458(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 29) idx -= 29;
    return (char*)p + idx * 48 + 12;
}
