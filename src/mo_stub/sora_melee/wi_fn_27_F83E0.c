void* fn_27_F83E0(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 26) + i;
    if (idx >= 22) idx -= 22;
    return (char*)p + idx * 12 + 28;
}
