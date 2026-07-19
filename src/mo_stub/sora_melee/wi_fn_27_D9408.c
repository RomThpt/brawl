void* fn_27_D9408(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 31) idx -= 31;
    return (char*)p + idx * 48 + 12;
}
