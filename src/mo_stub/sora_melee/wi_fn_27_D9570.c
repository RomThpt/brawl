void* fn_27_D9570(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 22) idx -= 22;
    return (char*)p + idx * 48 + 12;
}
