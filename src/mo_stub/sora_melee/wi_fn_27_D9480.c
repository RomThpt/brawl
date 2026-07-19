void* fn_27_D9480(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 28) idx -= 28;
    return (char*)p + idx * 48 + 12;
}
